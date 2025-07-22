# data_loader.py
from typing import List
from models.document import Documento

def cargar_documentos() -> List[Documento]:
    """Loads the sample data and converts it into Document objects."""
    datos_brutos = [
        {"texto": "La VBB-Umweltkarte en la zona tarifaria Berlin AB cuesta 68 EUR en una suscripción anual.", "metadata": {"zona": "AB", "validez": "anual", "tipo": "suscripcion"}},
        {"texto": "Un ticket mensual para la zona tarifaria Berlin AB tiene un precio de 86 EUR.", "metadata": {"zona": "AB", "validez": "mensual", "tipo": "ticket"}},
        {"texto": "Para los viajeros ocasionales, un billete sencillo para la zona BC cuesta 3.50 EUR.", "metadata": {"zona": "BC", "validez": "sencillo", "tipo": "ticket"}},
        {"texto": "Los tickets mensuales para la zona ABC tienen un coste de 107 EUR.", "metadata": {"zona": "ABC", "validez": "mensual", "tipo": "ticket"}},
        {"texto": "La suscripción anual para la zona ABC se puede pagar mensualmente por 89 EUR.", "metadata": {"zona": "ABC", "validez": "anual", "tipo": "suscripcion"}},
    ]
    return [Documento(texto=d["texto"], metadata=d["metadata"]) for d in datos_brutos]