from sentence_transformers import SentenceTransformer, util
from .base import EstrategiaRecuperacion, Documento
from typing import List

class RecuperadorSemantico(EstrategiaRecuperacion):
    """ Recuper documentos usando busqueda semantica (vectores). """
    def __init__(self, documentos: List[Documento], model_name = 'all-MiniLM-L6-v2'):
        self.documentos = documentos
        self.model = SentenceTransformer(model_name)
        textos_corpus = [doc.texto for doc in documentos]
        self.embeddings_corpus = self.model.encode(textos_corpus, convert_to_tensor=True)

    def recuperar(self, pregunta: str, top_k: int) -> List[int]:
        """ Devuelve los indices de los documentos mas relevantes. """    
        embedding_pregunta = self.model.encode(pregunta, convert_to_tensor=True)
        scores = util.cos_sim(embedding_pregunta, self.embeddings_corpus)
        indices = scores[0].argsort(descending=True)[:top_k]

        return indices.tolist()
    
