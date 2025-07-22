# pipeline.py
from typing import List
from models.document import Documento
from retrievers.hybrid import RecuperadorHibrido
from reranker import Reordenador

class BVG_RAG_Pipeline:
    """
    Orchestrates the full Advanced RAG pipeline:
    1. Hybrid retrieval of candidates.
    2. Re-ranking of candidates to find the best results.
    """
    def __init__(self, documentos: List[Documento], reordenador: Reordenador):
        """
        The constructor now accepts a 'reordenador' object, not an API key.
        """
        self.recuperador = RecuperadorHibrido(documentos)
        self.reordenador = reordenador

    def ejecutar(self, pregunta: str, candidatos_iniciales: int = 10, resultados_finales: int = 3) -> List[Documento]:
        """
        Executes the full pipeline.
        """
        # Step 1: Retrieve a broad set of candidates
        candidatos = self.recuperador.recuperar(pregunta, top_k=candidatos_iniciales)
        
        # Step 2: Re-rank the candidates for maximum precision
        documentos_reordenados = self.reordenador.reordenar(pregunta, candidatos, top_n=resultados_finales)
        
        return documentos_reordenados
