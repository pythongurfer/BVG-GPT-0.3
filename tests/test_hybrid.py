from retrievers.hybrid import RecuperadorHibrido
from models.document import Documento

def test_recuperador_hibrido():
    documentos = [
        Documento("La inteligencia artificial está cambiando el mundo", metadata={}),
        Documento("Messi ganó el mundial con Argentina", metadata={}),
        Documento("El aprendizaje profundo impulsa la IA", metadata={}),
        Documento("Cocinar puede ser una actividad relajante", metadata={}),
    ]

    pregunta = "inteligencia artificial"

    recuperador = RecuperadorHibrido(documentos, peso_lexical=0.5, peso_semantico=0.5)
    resultados = recuperador.recuperar(pregunta, top_k=3)

    print("Documentos recuperados:")
    for doc in resultados:
        print("-", doc.texto)

    # Asegurarse de que al menos un documento contenga el término "inteligencia"
    assert any("inteligencia" in doc.texto.lower() for doc in resultados), \
        "Ningún documento relevante fue recuperado."

if __name__ == "__main__":
    test_recuperador_hibrido()
