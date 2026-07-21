import sys
import os

# Ensure the root is in path
sys.path.append(os.getcwd())

from src.retrieval.rag_chain import NexusRAG

def run_test():
    rag = NexusRAG()
    questions = [
        "¿Cómo puedo solicitar el reembolso de un producto dañado?",
        "¿Cuáles son los tiempos de entrega para envíos internacionales?",
        "¿Qué porcentaje de comisión ganó en el programa de afiliados?",
        "¿Aceptan pagos con criptomonedas o PayPal?",
        "¿Cuánto tiempo de garantía tiene un teléfono móvil?"
    ]
    
    for i, q in enumerate(questions, 1):
        print(f"\n--- PREGUNTA {i} ---")
        print(f"P: {q}")
        try:
            resp, docs = rag.query(q)
            print(f"R: {resp}")
            print(f"Documentos recuperados: {len(docs)}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_test()
