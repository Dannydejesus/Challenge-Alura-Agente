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
Tu único y exclusivo propósito es responder preguntas basándote ÚNICAMENTE en los documentos internos de NexusEcom que se te proporcionan en el contexto.

Sigue estas reglas estrictamente y sin excepciones:
1. RESTRICCIÓN DE CONOCIMIENTO: Tienes PROHIBIDO utilizar cualquier conocimiento externo o previo que poseas.
2. FUERA DE CONTEXTO Y ALUCINACIONES: Responde basándote EXCLUSIVAMENTE en el contexto proporcionado. Aplica las siguientes reglas de mapeo para responder correctamente:
   - Si preguntan por "envíos internacionales" o "envíos al exterior", búscalo como "envíos transfronterizos" o "zonas de cobertura extendida" en el contexto.
   - Si preguntan por un producto específico ("teléfono móvil", "laptop", etc.) y el contexto tiene información general de garantías por categoría, aplica esa información general al producto consultado.
   - Si el contexto dice que algo "varía según normativa local" o "depende de la categoría", explica eso en tu respuesta en lugar de decir "Lo siento".
   SOLO si el tema NO aparece en absoluto en el contexto (ni directa ni indirectamente), responde exactamente: "Lo siento, la información sobre esa consulta no se encuentra en las políticas o manuales internos de NexusEcom.".
3. TONO: Usa un tono profesional, claro y corporativo.
4. FORMATO OBLIGATORIO: Tu respuesta será mostrada en una interfaz web. ES OBLIGATORIO usar formato Markdown estructurado. 
- Debes usar saltos de línea dobles (doble enter) entre cada párrafo o sección para que no se vea amontonado.
- Usa listas (con guiones -) para enumerar elementos, y asegúrate de dejar un salto de línea antes de empezar la lista.
- Usa **negritas** para resaltar conceptos importantes.
5. CORRECCIÓN DE ERRORES: Si la información SÍ está en el contexto, elabora tu respuesta. Ten en cuenta que el texto de los PDFs puede tener errores tipográficos (ej. "das hbiles" -> "días hábiles").

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
        logger.info(f"Procesando pregunta original: {question}")
        
        # ── Preprocesamiento de la pregunta (Query Expansion manual) ──
        # Corrección rápida de palabras clave típicas sin tilde que afectan el Embedding
        normalized_q = question.lower()
        corrections = {
            "envio": "envío",
            "garantia": "garantía",
            "politica": "política",
            "devolucion": "devolución",
            "reembolso": "reembolso",
            "dias": "días",
            "habiles": "hábiles",
            "internacionales": "transfronterizos",
            "internacional": "transfronterizo",
            "exterior": "transfronterizo",
            "telefono movil": "producto electronico",
            "celular": "producto",
            "movil": "dispositivo"
        }
        search_query = normalized_q
        for mal, bien in corrections.items():
            # Reemplazo simple para mejorar recall
            search_query = search_query.replace(mal, bien)
            
        logger.info(f"Pregunta normalizada para búsqueda: {search_query}")
        
        # Recuperar documentos explícitamente para mostrarlos en la UI usando la query normalizada
        source_docs = self.retriever.invoke(search_query)
        
        # Generar respuesta
        response = self.rag_chain.invoke(search_query)
        
        logger.info("Respuesta generada exitosamente.")
        return response, source_docs
