from retrievers.lexical import RecuperadorLexical
from models.document import Documento

def test_recuperador_lexical(): 
    documentos = [
        Documento("La inteligencia artificial está transformando el mundo", metadata={}),
        Documento("El aprendizaje automático es una rama de la IA", metadata={}),
        Documento("Messi ganó la Copa del Mundo con Argentina", metadata={}),
        Documento("La inteligencia artificial también se usa en medicina", metadata={}),
    ]

    recuperador = RecuperadorLexical(documentos)
    pregunta = "inteligencia artificial"
    indices = recuperador.recuperar(pregunta, top_k = 5)

    print("indices recuperados")
    for i in indices: 
        print(f"Documento {i}: {documentos[i].texto}")

if __name__=="__main__":
    test_recuperador_lexical()