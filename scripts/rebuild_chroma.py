"""
Script para re-indexar TODOS los documentos de NexusEcom en ChromaDB.
Borra la colección anterior y la reconstruye desde cero con los 5 PDFs.
"""
import sys
import os
from pathlib import Path

# Asegurar que el directorio raíz esté en el path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.config import (
    COHERE_API_KEY, EMBEDDING_MODEL,
    CHROMA_DB_PATH, CHROMA_COLLECTION_NAME,
    CHUNK_SIZE, CHUNK_OVERLAP, DOCS_DIR,
    logger
)
from langchain_cohere import CohereEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb

def rebuild_chroma():
    logger.info("=== INICIO: Re-indexación completa de ChromaDB ===")
    
    # 1. Encontrar todos los PDFs en docs/
    pdf_files = list(DOCS_DIR.rglob("*.pdf"))
    if not pdf_files:
        logger.error(f"No se encontraron PDFs en {DOCS_DIR}")
        return
    
    logger.info(f"PDFs encontrados ({len(pdf_files)}):")
    for f in pdf_files:
        logger.info(f"  - {f.relative_to(BASE_DIR)}")
    
    # 2. Cargar y chunkar documentos
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    
    all_chunks = []
    for pdf_path in pdf_files:
        categoria = pdf_path.parent.name  # Nombre de la carpeta = categoría
        logger.info(f"Cargando: {pdf_path.name} | Categoría: {categoria}")
        try:
            loader = PyMuPDFLoader(str(pdf_path))
            docs = loader.load()
            chunks = text_splitter.split_documents(docs)
            
            # Enriquecer metadatos
            for chunk in chunks:
                chunk.metadata.update({
                    "categoria": categoria,
                    "archivo": pdf_path.name,
                    "empresa": "NexusEcom",
                    "ruta": str(pdf_path),
                    "extension": ".pdf"
                })
            all_chunks.extend(chunks)
            logger.info(f"  -> {len(chunks)} chunks generados")
        except Exception as e:
            logger.error(f"Error cargando {pdf_path.name}: {e}")
    
    logger.info(f"Total chunks a indexar: {len(all_chunks)}")
    
    # 3. Borrar colección existente
    logger.info("Borrando colección existente en ChromaDB...")
    try:
        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        try:
            client.delete_collection(CHROMA_COLLECTION_NAME)
            logger.info("Colección borrada exitosamente.")
        except Exception:
            logger.info("Colección no existía previamente.")
    except Exception as e:
        logger.warning(f"Advertencia al conectar con ChromaDB: {e}")
    
    # 4. Crear embeddings e indexar
    logger.info("Creando embeddings con Cohere e indexando en ChromaDB...")
    embeddings = CohereEmbeddings(
        cohere_api_key=COHERE_API_KEY,
        model=EMBEDDING_MODEL
    )
    
    # Indexar en lotes para evitar rate limiting
    BATCH_SIZE = 50
    vectorstore = None
    for i in range(0, len(all_chunks), BATCH_SIZE):
        batch = all_chunks[i:i + BATCH_SIZE]
        logger.info(f"Indexando lote {i//BATCH_SIZE + 1}/{(len(all_chunks)-1)//BATCH_SIZE + 1} ({len(batch)} chunks)...")
        try:
            if vectorstore is None:
                vectorstore = Chroma.from_documents(
                    documents=batch,
                    embedding=embeddings,
                    collection_name=CHROMA_COLLECTION_NAME,
                    persist_directory=CHROMA_DB_PATH
                )
            else:
                vectorstore.add_documents(batch)
        except Exception as e:
            logger.error(f"Error en lote {i//BATCH_SIZE + 1}: {e}")
            import time
            time.sleep(5)
            continue
    
    # 5. Verificar resultado
    if vectorstore:
        total = vectorstore._collection.count()
        logger.info(f"=== ÉXITO: {total} documentos indexados en ChromaDB ===")
        
        # Verificar categorías
        all_docs = vectorstore._collection.get(limit=total, include=['metadatas'])
        cats = set(m.get('categoria', '?') for m in all_docs['metadatas'])
        logger.info(f"Categorías indexadas: {cats}")
    else:
        logger.error("Error: No se pudo crear el vectorstore")

if __name__ == "__main__":
    rebuild_chroma()
