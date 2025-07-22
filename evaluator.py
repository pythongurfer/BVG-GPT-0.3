# /evaluator.py

import pandas as pd # Asegúrate de tener pandas instalado (pip install pandas)
from typing import List, Dict
from models.document import Documento
from retrievers.lexical import RecuperadorLexical
from retrievers.semantic import RecuperadorSemantico
from retrievers.hybrid import RecuperadorHibrido

class EvaluadorPipeline:
    """
    Una clase para ejecutar y comparar diferentes estrategias de recuperación.
    Ahora devuelve los resultados en un DataFrame de Pandas para su uso en frontends.
    """
    def __init__(self, documentos: List[Documento]):
        self.documentos = documentos
        self.recuperador_lexical = RecuperadorLexical(documentos)
        self.recuperador_semantico = RecuperadorSemantico(documentos)
        self.recuperador_hibrido = RecuperadorHibrido(documentos)

    def _calcular_rr(self, resultados: List[Documento], doc_correcto: Documento) -> (float, int):
        """Devuelve el Reciprocal Rank y la posición del documento correcto."""
        for i, doc in enumerate(resultados):
            if doc.texto == doc_correcto.texto:
                rank = i + 1
                return (1 / rank), rank
        return 0.0, -1

    def evaluar_pregunta(self, pregunta: str, doc_correcto: Documento, top_k: int = 10) -> pd.DataFrame:
        """
        Ejecuta la evaluación y devuelve un DataFrame con los resultados.
        """
        data = []

        # Lexical
        indices_lexical = self.recuperador_lexical.recuperar(pregunta, top_k)
        resultados_lexical = [self.documentos[i] for i in indices_lexical]
        rr_l, rank_l = self._calcular_rr(resultados_lexical, doc_correcto)
        data.append({"Estrategia": "Lexical (BM25)", "Reciprocal Rank (RR)": rr_l, "Posición Correcta": rank_l})

        # Semantic
        indices_semantico = self.recuperador_semantico.recuperar(pregunta, top_k)
        resultados_semantico = [self.documentos[i] for i in indices_semantico]
        rr_s, rank_s = self._calcular_rr(resultados_semantico, doc_correcto)
        data.append({"Estrategia": "Semántica (Vectores)", "Reciprocal Rank (RR)": rr_s, "Posición Correcta": rank_s})
        
        # Hybrid
        resultados_hibrido = self.recuperador_hibrido.recuperar(pregunta, top_k)
        rr_h, rank_h = self._calcular_rr(resultados_hibrido, doc_correcto)
        data.append({"Estrategia": "Híbrida", "Reciprocal Rank (RR)": rr_h, "Posición Correcta": rank_h})

        # Crear y formatear DataFrame
        df = pd.DataFrame(data)
        df['Posición Correcta'] = df['Posición Correcta'].apply(lambda x: str(x) if x > 0 else "No Encontrado")
        df['Reciprocal Rank (RR)'] = df['Reciprocal Rank (RR)'].map('{:,.4f}'.format)
        
        return df