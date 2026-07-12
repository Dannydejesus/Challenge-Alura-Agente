"""
Módulo de Backend RAG para NexusEcom
Integra ChromaDB, CohereEmbeddings y ChatCohere con LangChain.
"""

from langchain_cohere import ChatCohere, CohereEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from src.config import (
    COHERE_API_KEY, 
    LLM_MODEL, 
    EMBEDDING_MODEL, 
    CHROMA_DB_PATH, 
    CHROMA_COLLECTION_NAME,
    MAX_RETRIEVAL_DOCS,
    logger
)

def format_docs(docs):
    """Formatea los documentos recuperados para incluirlos en el prompt."""
    return "\n\n".join(doc.page_content for doc in docs)

class NexusRAG:
    def __init__(self):
        logger.info("Inicializando NexusRAG Backend...")
        
        # 1. Inicializar Embeddings
        self.embeddings = CohereEmbeddings(
            cohere_api_key=COHERE_API_KEY,
            model=EMBEDDING_MODEL
        )
        
        # 2. Conectar a ChromaDB (asumimos que ya fue poblado)
        self.vectorstore = Chroma(
            collection_name=CHROMA_COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=CHROMA_DB_PATH
        )
        
        # 3. Configurar Retriever
        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": MAX_RETRIEVAL_DOCS}
        )
        
        # 4. Inicializar LLM
        self.llm = ChatCohere(
            cohere_api_key=COHERE_API_KEY,
            model=LLM_MODEL,
            temperature=0.3  # Baja temperatura para respuestas más deterministas y precisas
        )
        
        # 5. Definir Prompt Corporativo
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Eres el Asistente Virtual Corporativo de NexusEcom. 
Tu objetivo es ayudar a los colaboradores proporcionando información precisa basada ÚNICAMENTE en los documentos internos recuperados.

Sigue estas reglas estrictamente:
1. Usa un tono profesional, claro y corporativo.
2. Si la respuesta no está en el contexto proporcionado, responde "No tengo suficiente información en la base de conocimientos para responder a esa pregunta."
3. No inventes información (no alucines).
4. Sé conciso pero completo en tu respuesta.

Contexto recuperado:
{context}
"""),
            ("human", "{question}")
        ])
        
        # 6. Construir la cadena RAG con LCEL
        self.rag_chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        logger.info("NexusRAG inicializado correctamente.")

    def query(self, question: str):
        """
        Realiza una consulta al sistema RAG.
        Retorna una tupla: (respuesta_texto, documentos_fuente)
        """
        logger.info(f"Procesando pregunta: {question}")
        
        # Recuperar documentos explícitamente para mostrarlos en la UI
        source_docs = self.retriever.invoke(question)
        
        # Generar respuesta
        response = self.rag_chain.invoke(question)
        
        logger.info("Respuesta generada exitosamente.")
        return response, source_docs
