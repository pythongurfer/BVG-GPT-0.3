# main.py

from models.document import Documento
from evaluator import EvaluadorPipeline # Importa la nueva clase
from typing import List
from _data_loader import cargar_documentos_desde_pdf

def cargar_documentos():
    """Carga los datos y los convierte en objetos Documento."""
    datos_brutos = [
        # Documento 0
        {"texto": "La VBB-Umweltkarte en la zona tarifaria Berlin AB cuesta 68 EUR en una suscripción anual.", "metadata": {"zona": "AB", "validez": "anual", "tipo": "suscripcion"}},
        # Documento 1
        {"texto": "Un ticket mensual para la zona tarifaria Berlin AB tiene un precio de 86 EUR.", "metadata": {"zona": "AB", "validez": "mensual", "tipo": "ticket"}},
        # Documento 2
        {"texto": "Para los viajeros ocasionales, un billete sencillo para la zona BC cuesta 3.50 EUR.", "metadata": {"zona": "BC", "validez": "sencillo", "tipo": "ticket"}},
        # Documento 3
        {"texto": "Los tickets mensuales para la zona ABC tienen un coste de 107 EUR.", "metadata": {"zona": "ABC", "validez": "mensual", "tipo": "ticket"}},
        # Documento 4
        {"texto": "La suscripción anual para la zona ABC se puede pagar mensualmente por 89 EUR.", "metadata": {"zona": "ABC", "validez": "anual", "tipo": "suscripcion"}},
    ]
    return [Documento(texto=d["texto"], metadata=d["metadata"]) for d in datos_brutos]


"""    documentos = cargar_documentos_desde_pdf("data")
    return documentos"""

if __name__ == "__main__":
    # 1. Cargar los datos
    documentos = cargar_documentos()

    # 2. Inicializar el evaluador
    evaluador = EvaluadorPipeline(documentos)

    # 3. Definir las preguntas de prueba y el "ground truth" (el documento correcto)
    pruebas = [
        {
            "pregunta": "How much is a monthly ticket for AB?",
            "doc_correcto": documentos[1] # "Un ticket mensual para la zona tarifaria Berlin AB..."
        },
        {
            # Esta pregunta usa sinónimos, lo que debería confundir a la búsqueda lexical
            "pregunta": "I need a yearly pass for the AB area",
            "doc_correcto": documentos[0] # "La VBB-Umweltkarte en la zona tarifaria Berlin AB..."
        },
        {
            # Esta pregunta es muy específica y debería beneficiar a la búsqueda lexical
            "pregunta": "single ticket BC",
            "doc_correcto": documentos[2] # "Para los viajeros ocasionales, un billete sencillo para la zona BC..."
        }
    ]

    # 4. Ejecutar la evaluación para cada prueba
    for prueba in pruebas:
        evaluador.evaluar_pregunta(prueba["pregunta"], prueba["doc_correcto"])