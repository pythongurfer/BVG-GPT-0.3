from rank_bm25 import BM25Okapi
from retrievers.base import EstrategiaRecuperacion, Documento
from typing import List

class RecuperadorLexical(EstrategiaRecuperacion):
    """ Recupera documentos usando busqueda por palabras clave (BM25)"""
    def __init__(self, documentos: List[Documento]):
        self.documentos = documentos
        textos_corpus = [doc.texto for doc in documentos]
        tokenized_corpus = [doc.lower().split() for doc in textos_corpus]
        self.bm25 = BM25Okapi(tokenized_corpus)

    def recuperar(self, pregunta: str, top_k: int) -> List[int]: 
        """ Devuelve los indices de los documentos mas relevantes. """
        tokenized_query = pregunta.lower().split()
        print(f"Tokenized query: {tokenized_query}")
        doc_scores = self.bm25.get_scores(tokenized_query)
        # Usamos argsort para obtener los indices de los scores mas altos
        indices = doc_scores.argsort()[::-1][:top_k]
        return indices.tolist()


