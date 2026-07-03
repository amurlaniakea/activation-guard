from abc import ABC, abstractmethod

import numpy as np


class RepresentationExtractor(ABC):
    """Interface para extraer representaciones de prompts"""

    @abstractmethod
    def extract(self, prompt: str) -> np.ndarray:
        """Extrae representación de un prompt"""

    @abstractmethod
    def get_dimension(self) -> int:
        """Retorna la dimensión de la representación"""
