
import numpy as np
from sklearn.neighbors import NearestNeighbors

from ..models.requests import GuardrailRequest, GuardrailResponse
from .extractor import RepresentationExtractor


class Guardrail:
    """Framework de guardrail training-free basado en representaciones"""

    def __init__(self, backend: str = "openai", threshold: float = 0.5):
        self.backend = backend
        self.threshold = threshold
        self.extractors = {}
        self.knn_models = {}
        self.example_vectors = {}
        self.example_labels = {}

    def register_extractor(self, name: str, extractor: RepresentationExtractor):
        """Registra un extractor de representaciones"""
        self.extractors[name] = extractor

    def add_examples(self, domain: str, safe_examples: list[str], unsafe_examples: list[str]):
        """Agrega ejemplos para un dominio específico"""
        # Para simplificar, usamos un extractor dummy
        extractor = self.extractors.get(self.backend)
        if not extractor:
            raise ValueError(f"No hay extractor registrado para {self.backend}")

        # En MVP, usamos representaciones aleatorias
        safe_vectors = extractor.extract_batch(safe_examples)
        unsafe_vectors = extractor.extract_batch(unsafe_examples)

        self.example_vectors[domain] = np.vstack([safe_vectors, unsafe_vectors])
        self.example_labels[domain] = np.array([1] * len(safe_examples) + [0] * len(unsafe_examples))

        # Entrenar modelo kNN
        knn = NearestNeighbors(n_neighbors=min(5, len(self.example_vectors[domain])), metric='cosine')
        knn.fit(self.example_vectors[domain])
        self.knn_models[domain] = knn

    def check(self, request: GuardrailRequest) -> GuardrailResponse:
        """Verifica si un prompt es seguro"""
        try:
            # Extraer representación
            extractor = self.extractors.get(request.backend)
            if not extractor:
                raise ValueError(f"Backend no soportado: {request.backend}")

            # En MVP, usamos representación aleatoria
            representation = extractor.extract(request.prompt)

            # Clasificación con kNN
            domain = request.domain or "default"
            if domain not in self.knn_models:
                # Por defecto, consideramos seguro
                return GuardrailResponse(
                    safe=True,
                    confidence=0.5,
                    details={"reason": "No hay ejemplos para este dominio"}
                )

            # Obtener vecinos más cercanos
            distances, indices = self.knn_models[domain].kneighbors([representation])

            # Calcular score basado en vecinos
            neighbor_labels = self.example_labels[domain][indices[0]]
            score = np.mean(neighbor_labels)

            # Devolver resultado
            return GuardrailResponse(
                safe=bool(score > request.threshold),
                confidence=float(score),
                details={
                    "distance": float(distances[0][0]) if len(distances[0]) > 0 else 0.0,
                    "domain": domain,
                    "threshold": request.threshold
                }
            )

        except (ValueError, KeyError, IndexError) as e:
            # Manejo de errores específicos
            return GuardrailResponse(
                safe=False,
                confidence=0.0,
                details={"error": str(e)}
            )
