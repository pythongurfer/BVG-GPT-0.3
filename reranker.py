import cohere
from typing import List
from models.document import Documento
from dotenv import load_dotenv
load_dotenv()
import os
api_key = os.environ["COHERE_API_KEY"]

class Reordenador:
    """
    Reordena una lista de documentos usando un modelo Cross-Encoder. 
    Aqui se usa la API de Cohere como ejemplo. 
    """
    def __init__(self, api_key: str, model ='rerank-english-v3.0'):
        self.client = cohere.Client(api_key)
        self.model = model
        self.api_key = api_key

    def reordenar(self, pregunta, documentos: List[Documento], top_n = 3) -> List[Documento]:
        textos_candidatos = [doc.texto for doc in documentos]


        resultados = self.client.rerank(
            model=self.model,
            query=pregunta,
            documents=textos_candidatos,
            top_n=top_n
        )

        documentos_reordenados = []
        for hit in resultados.results:
            indice_original = hit.index
            documentos_reordenados.append(documentos[indice_original])
        return documentos_reordenados

"""if __name__== "__main__":
    docs = [
        Documento("La inteligencia artificial está cambiando el mundo", metadata={}),
        Documento("Messi ganó el mundial con Argentina", metadata={}),
        Documento("El aprendizaje profundo impulsa la IA", metadata={}),
    ]
    pregunta = "inteligencia artificial"
    reord = Reordenador(api_key)
    docs_ordenados = reord.reordenar(pregunta, docs, top_n=2)
        
    for doc in docs_ordenados:
        print(doc.texto)
"""
