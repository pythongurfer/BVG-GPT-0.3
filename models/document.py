from typing import Dict, Any

class Documento:
    """
    Una clase para representar un document con su texto y metadatos. 
    Encapsula los datos para un manejo mas limpio. 
    """

    def __init__(self, texto: str, metadata: Dict[str, Any]):
        self.texto = texto
        self.metadata = metadata

    def __repr__(self) -> str:
        return f"Documento(texto='{self.texto[:30]}...', metadata={self.metadata})"
    
