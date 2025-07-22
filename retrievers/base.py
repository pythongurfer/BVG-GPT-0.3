from abc import ABC, abstractmethod
from typing import List
from models.document import Documento


class EstrategiaRecuperacion(ABC):
    """Clase base abstracta para todas las estrategias de recuperacion. """
    @abstractmethod
    def recuperar(self, pregunta: str, top_k) -> List[Documento]:
        pass

