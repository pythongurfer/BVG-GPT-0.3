import numpy as np
from .base import EstrategiaRecuperacion, Documento
from .lexical import RecuperadorLexical
from .semantic import RecuperadorSemantico
from typing import List
from sentence_transformers import util

class RecuperadorHibrido(EstrategiaRecuperacion):
    """ Combina los resultados de la busqueda lexica y semantica. """
    def __init__(self, documentos: List[Documento], peso_lexical=0.5, peso_semantico=0.5):
        self.documentos = documentos
        self.recuperador_lexical = RecuperadorLexical(documentos)
        self.recuperador_semantico = RecuperadorSemantico(documentos)
        self.peso_semantico = peso_semantico
        self.peso_lexical = peso_lexical

    def recuperar(self, pregunta: str, top_k: int) -> List[Documento]: 
        """ Realiza una busqueda hybrida y devuelve una lista de Documentos. """
        # Obtener scores en lugar de solo indices
        tokenized_query = pregunta.lower().split()
        scores_lexical = self.recuperador_lexical.bm25.get_scores(tokenized_query)

        embedding_pregunta = self.recuperador_semantico.model.encode(pregunta, convert_to_tensor=True)
        scores_semanticos = util.cos_sim(embedding_pregunta, self.recuperador_semantico.embeddings_corpus)[0]

        # Normalizar scores (simple division por el max)
        scores_lexical_norm = scores_lexical / (np.max(scores_lexical) or 1)
        scores_semanticos_norm = scores_semanticos.cpu().numpy() / (np.max(scores_semanticos.cpu().numpy()) or 1)

        # Combinar scores
        scores_hibridos = self.peso_lexical * scores_lexical_norm + self.peso_semantico * scores_semanticos_norm

        indices = scores_hibridos.argsort()[::-1][:top_k]
        return [self.documentos[i] for i in indices]
    