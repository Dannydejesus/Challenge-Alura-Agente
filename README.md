# 🤖 Challenge Alura Agente — NexusEcom RAG Agent

> Agente de Inteligencia Artificial corporativo basado en RAG (Retrieval-Augmented Generation) para responder preguntas de colaboradores a partir de documentos internos de NexusEcom.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Cohere](https://img.shields.io/badge/LLM-Cohere_command--r--plus-orange)
![LangChain](https://img.shields.io/badge/Framework-LangChain-green)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-purple)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![OCI](https://img.shields.io/badge/Deploy-Oracle_Cloud-blue)

---

## Descripcion del Proyecto

**NexusEcom** es una tienda online de e-commerce multiplataforma. Este agente permite a los colaboradores consultar documentos corporativos internos de forma inteligente, obteniendo respuestas precisas y con fuentes citadas.

### Documentos indexados
| Categoria | Documento |
|-----------|-----------|
| Politicas | Politica de Reembolsos y Devoluciones |
| Logistica | Guia de Tiempos y Costos de Envio |
| Pagos | Preguntas Frecuentes sobre Metodos de Pago |
| Afiliados | Programa de Afiliados |
| Garantias | Manual de Garantia de Productos |

---

## Stack Tecnologico

| Componente | Tecnologia |
|------------|-----------|
| LLM | Cohere `command-r-plus-08-2024` |
| Embeddings | Cohere `embed-multilingual-v3.0` |
| Base Vectorial | ChromaDB |
| Orquestacion RAG | LangChain >= 0.2 |
| Interfaz | Streamlit |
| Deploy | Oracle Cloud Infrastructure (OCI) |
| Lenguaje | Python 3.13 |

---

## Estructura del Proyecto

```
Challenge-Alura-Agente/
├── Challenge_Alura_Agente.ipynb  # Cuaderno principal del pipeline
├── requirements.txt              # Dependencias del proyecto
├── .env.example                  # Plantilla de variables de entorno
├── .gitignore                    # Archivos excluidos del repo
├── src/
│   ├── __init__.py
│   ├── config.py                 # Configuracion centralizada
│   ├── ingestion/                # Modulo de ingesta de documentos
│   ├── retrieval/                # Modulo de recuperacion RAG
│   └── interface/                # Interfaz Streamlit
├── docs/                         # Documentos internos (excluidos del repo)
│   ├── politicas/
│   ├── logistica/
│   ├── pagos_y_facturacion/
│   ├── marketing_afiliados/
│   └── garantias_y_soporte/
├── tests/                        # Tests unitarios
└── config/                       # Configuraciones adicionales
```

---

## Instalacion y Configuracion

### 1. Clonar el repositorio
```bash
git clone https://github.com/Dannydejesus/Challenge-Alura-Agente.git
cd Challenge-Alura-Agente
```

### 2. Crear entorno virtual
```bash
python -m venv "Alura Agente"
# Windows
& ".\Alura Agente\Scripts\Activate.ps1"
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
```bash
copy .env.example .env
# Editar .env y agregar tu COHERE_API_KEY
```

Obtener API Key gratuita en: https://dashboard.cohere.com/api-keys

### 5. Agregar documentos
Coloca tus documentos en las carpetas correspondientes dentro de `docs/`.

### 6. Ejecutar el cuaderno
Abre `Challenge_Alura_Agente.ipynb` y ejecuta las celdas en orden.

---

## Pipeline RAG

```
PDFs → Extraccion (PyMuPDF) → Chunking (LangChain) → Embeddings (Cohere)
                                                              ↓
Pregunta del usuario → Retriever (ChromaDB) → LLM (Cohere) → Respuesta + Fuentes
```

---

## Roadmap

- [x] Fase 0 — Setup y configuracion del entorno
- [x] Fase 1 — Colecta y organizacion de documentos
- [ ] Fase 2 — Procesamiento y extraccion de contenido
- [ ] Fase 3 — Indexacion vectorial en ChromaDB
- [ ] Fase 4 — Capa RAG de recuperacion
- [ ] Fase 5 — Generacion de respuestas con Cohere
- [ ] Fase 6 — Interfaz Streamlit
- [ ] Fase 7 — Deploy en Oracle Cloud Infrastructure
- [ ] Fase 8 — Registro y cierre del challenge

---

## Autor

**Danny De Jesus**  
Challenge Alura Agente — ONE Oracle Next Education + Alura Latam  

---

## Licencia

Proyecto educativo — Challenge Alura ONE.
