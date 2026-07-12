import streamlit as st
import sys
from pathlib import Path
import time

# Agregar el directorio raíz al path para poder importar src
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from src.config import APP_TITLE, APP_DESCRIPTION, logger
from src.retrieval.rag_chain import NexusRAG

# ==========================================
# CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# ESTILO CSS - TEMA TECH / DARK MODERN
# ==========================================
def inject_custom_css():
    st.markdown("""
        <style>
        /* Variables del tema Tech/Cyber */
        :root {
            --bg-color: #0b0f19;
            --bg-gradient: linear-gradient(135deg, #0b0f19 0%, #1a2235 100%);
            --sidebar-bg: rgba(11, 15, 25, 0.85);
            --accent-primary: #00f2fe; /* Cyan neon */
            --accent-secondary: #4facfe; /* Azul brillante */
            --accent-cohere: #FF7B00;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --card-bg: rgba(30, 41, 59, 0.5);
            --card-border: rgba(255, 255, 255, 0.08);
            --glass-blur: blur(12px);
        }

        /* Ocultar UI de Streamlit - Manteniendo el botón del sidebar visible */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header[data-testid="stHeader"] {background: transparent;}

        /* Fondo general */
        .stApp {
            background: var(--bg-gradient);
            background-attachment: fixed;
            color: var(--text-main);
            font-family: 'Inter', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }

        /* Fix para el input del chat para que el texto sea visible */
        .stChatInputContainer {
            background-color: #1e293b !important;
            border: 1px solid var(--accent-secondary) !important;
            border-radius: 16px !important;
            box-shadow: 0 0 15px rgba(79, 172, 254, 0.15) !important;
        }
        .stChatInputContainer textarea {
            color: #ffffff !important;
            caret-color: var(--accent-primary) !important;
        }
        /* Para cambiar el color del placeholder */
        .stChatInputContainer textarea::placeholder {
            color: #94a3b8 !important;
        }

        /* Panel lateral (Sidebar) con Glassmorphism */
        [data-testid="stSidebar"] {
            background-color: var(--sidebar-bg) !important;
            backdrop-filter: var(--glass-blur);
            border-right: 1px solid var(--card-border);
        }
        [data-testid="stSidebar"] * {
            color: var(--text-main) !important;
        }
        
        /* Botón de limpiar historial */
        [data-testid="stSidebar"] button {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid var(--card-border) !important;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        [data-testid="stSidebar"] button:hover {
            border-color: var(--accent-cohere) !important;
            box-shadow: 0 0 10px rgba(255, 123, 0, 0.3) !important;
        }

        /* Encabezados principales */
        .tech-header {
            font-weight: 900;
            font-size: 3rem;
            background: -webkit-linear-gradient(45deg, var(--accent-primary), var(--accent-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.2rem;
            letter-spacing: -1px;
        }
        
        .tech-subheader {
            font-weight: 300;
            font-size: 1.1rem;
            color: var(--text-muted);
            margin-bottom: 2.5rem;
            border-bottom: 1px solid var(--card-border);
            padding-bottom: 1rem;
        }

        /* Mensajes de chat */
        .stChatMessage {
            background: var(--card-bg) !important;
            backdrop-filter: var(--glass-blur);
            border: 1px solid var(--card-border) !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
            margin-bottom: 1.2rem !important;
            color: var(--text-main) !important;
        }
        
        /* Avatares tech */
        [data-testid="stChatMessageAvatarUser"] {
            background: linear-gradient(135deg, #FF7B00, #ff4000) !important;
        }
        [data-testid="stChatMessageAvatarAssistant"] {
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)) !important;
        }

        /* Fuentes / Expanders */
        .streamlit-expanderHeader {
            background-color: rgba(255,255,255,0.02) !important;
            border-radius: 8px !important;
            color: var(--accent-primary) !important;
            font-family: monospace;
            border: 1px dashed var(--card-border) !important;
        }
        
        .source-card {
            background: rgba(0, 0, 0, 0.2);
            border-left: 2px solid var(--accent-cohere);
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 0 8px 8px 0;
            font-size: 0.85rem;
            color: #cbd5e1;
            font-family: 'Consolas', 'Courier New', monospace;
        }
        
        .source-meta {
            font-weight: 800;
            color: var(--accent-cohere);
            margin-bottom: 0.5rem;
            font-size: 0.75rem;
            letter-spacing: 1px;
        }
        </style>
    """, unsafe_allow_html=True)

# ==========================================
# INICIALIZACIÓN DEL BACKEND RAG
# ==========================================
@st.cache_resource
def load_rag_backend():
    try:
        return NexusRAG()
    except Exception as e:
        logger.error(f"Error inicializando NexusRAG: {e}")
        st.error(f"Error crítico al iniciar el backend: {str(e)}")
        return None

# ==========================================
# INTERFAZ PRINCIPAL
# ==========================================
def main():
    inject_custom_css()
    
    # --- Panel Lateral ---
    with st.sidebar:
        st.markdown(f"## 🏢 NexusEcom Hub")
        st.markdown("---")
        
        # Expanders con Información Corporativa
        with st.expander("🎯 Misión Corporativa", expanded=False):
            st.info(
                "Transformar la experiencia de comercio electrónico ofreciendo "
                "procesos transparentes, rápidos y altamente eficientes para nuestros "
                "clientes y colaboradores a nivel global."
            )
            
        with st.expander("👁️ Visión 2027", expanded=False):
            st.success(
                "Ser la plataforma de e-commerce líder en innovación tecnológica, "
                "destacando por nuestra logística optimizada y nuestra atención al cliente "
                "impulsada por Inteligencia Artificial."
            )
            
        with st.expander("⭐ Nuestros Valores", expanded=False):
            st.markdown("""
            - **Innovación Continua**
            - **Transparencia Total**
            - **Obsesión por el Cliente**
            - **Sostenibilidad**
            """)

        st.markdown("---")
        st.markdown("### 🗄️ Matriz de Documentos")
        
        with st.expander("Ver documentos indexados", expanded=True):
            st.markdown("""
            * `sys.politicas.reembolsos`
            * `sys.logistica.envios`
            * `sys.finanzas.pagos`
            * `sys.socios.afiliados`
            * `sys.soporte.garantias`
            """)
        
        st.markdown("---")
        st.caption("⚡ Desarrollado por el **Tech AI Builder Danny Gonzalez**")
        
        if st.button("🔄 Reiniciar Terminal", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # --- Área Principal ---
    st.markdown(f"<div class='tech-header'>{APP_TITLE}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='tech-subheader'>{APP_DESCRIPTION}</div>", unsafe_allow_html=True)
    
    rag = load_rag_backend()
    if not rag:
        st.stop()

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Conexión exitosa. Hola, soy la IA de operaciones de NexusEcom. ¿Qué información requieres extraer hoy?"}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "sources" in msg and msg["sources"]:
                with st.expander("🔎 Analizar orígenes de datos (Fuentes)"):
                    for i, doc in enumerate(msg["sources"]):
                        source_name = doc.metadata.get('source', 'nodo_desconocido')
                        st.markdown(f"""
                        <div class="source-card">
                            <div class="source-meta">EXTRACCIÓN {i+1} | ORIGEN: {source_name}</div>
                            {doc.page_content[:350]}...
                        </div>
                        """, unsafe_allow_html=True)

    if prompt := st.chat_input("Ingresa tu consulta (Ej: ¿Cuál es el tiempo de envío?)..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Procesando consulta en la matriz de datos..."):
                try:
                    response, source_docs = rag.query(prompt)
                    
                    # Efecto de máquina de escribir simulado (opcional para look tech)
                    placeholder = st.empty()
                    full_response = ""
                    # Stream simulado
                    for chunk in response.split():
                        full_response += chunk + " "
                        time.sleep(0.015)
                        placeholder.markdown(full_response + "▌")
                    placeholder.markdown(full_response)
                    
                    if source_docs:
                        with st.expander("🔎 Analizar orígenes de datos (Fuentes)"):
                            for i, doc in enumerate(source_docs):
                                source_name = doc.metadata.get('source', 'nodo_desconocido')
                                st.markdown(f"""
                                <div class="source-card">
                                    <div class="source-meta">EXTRACCIÓN {i+1} | ORIGEN: {source_name}</div>
                                    {doc.page_content[:350]}...
                                </div>
                                """, unsafe_allow_html=True)
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response,
                        "sources": source_docs
                    })
                    
                except Exception as e:
                    logger.error(f"Error: {e}")
                    st.error("Fallo en la comunicación con el servidor LLM.")

if __name__ == "__main__":
    main()
