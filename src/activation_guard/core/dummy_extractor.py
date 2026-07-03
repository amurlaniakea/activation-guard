"""Dummy extractor para pruebas y casos simples"""

import numpy as np
from .extractor import RepresentationExtractor

class DummyExtractor(RepresentationExtractor):
    """Extractor dummy que genera representaciones aleatorias"""
    
    def __init__(self, dimension: int = 768):
        self.dimension = dimension
        self.rng = np.random.default_rng()
        
    def extract(self, prompt: str) -> np.ndarray:
        """Genera representación aleatoria (para MVP)"""
        return self.rng.standard_normal(self.dimension)
    
    def get_dimension(self) -> int:
        return self.dimension