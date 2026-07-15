"""
Modulo de configuracion central del proyecto — NexusEcom RAG Agent
Proveedor LLM: Cohere (command-r-plus)
"""

import os
import sys

# Parche para Streamlit Cloud (SQLite compatibility para ChromaDB)
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

# Fix encoding UTF-8 en Windows
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

# ── Cargar variables de entorno ──────────────────────────────────────────────
load_dotenv()

# ── Rutas base del proyecto ──────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
CHROMA_DIR = BASE_DIR / "chroma_db"
LOGS_DIR = BASE_DIR / "logs"

CHROMA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# ── Configuracion de Cohere ───────────────────────────────────────────────────
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# Soporte para Streamlit Cloud Secrets
if not COHERE_API_KEY:
    try:
        import streamlit as st
        COHERE_API_KEY = st.secrets.get("COHERE_API_KEY")
    except Exception:
        pass

if not COHERE_API_KEY:
    raise ValueError(
        "COHERE_API_KEY no encontrada. "
        "Edita el archivo .env o configura los Secrets en Streamlit Cloud."
    )

LLM_MODEL = os.getenv("LLM_MODEL", "command-r-plus-08-2024")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "embed-multilingual-v3.0")

# ── Configuracion de ChromaDB ─────────────────────────────────────────────────
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", str(CHROMA_DIR))
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "nexusecom_documents")

# ── Configuracion de procesamiento ────────────────────────────────────────────
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))
MAX_RETRIEVAL_DOCS = int(os.getenv("MAX_RETRIEVAL_DOCS", 10))

# ── Configuracion de la interfaz ─────────────────────────────────────────────
APP_TITLE = os.getenv("APP_TITLE", "Agente NexusEcom")
APP_DESCRIPTION = os.getenv(
    "APP_DESCRIPTION",
    "Asistente virtual de NexusEcom - Tienda online | Reembolsos, Envios, Pagos, Garantias y Afiliados"
)

# ── Configuracion de logging ──────────────────────────────────────────────────
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_PATH = os.getenv("LOG_PATH", str(LOGS_DIR / "agent.log"))

logger.add(
    LOG_PATH,
    level=LOG_LEVEL,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
    rotation="10 MB",
    retention="30 days",
    encoding="utf-8"
)

# ── Formatos de documento soportados ─────────────────────────────────────────
SUPPORTED_EXTENSIONS = {
    ".pdf", ".docx", ".xlsx", ".pptx",
    ".md", ".csv", ".json", ".html", ".htm", ".txt",
}

logger.info(f"Configuracion cargada | LLM: {LLM_MODEL} | Embedding: {EMBEDDING_MODEL}")



