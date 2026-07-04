"""Adapter para OpenAI Embeddings API."""

import os

import numpy as np

from ..core.extractor import RepresentationExtractor


class OpenAIEmbeddingExtractor(RepresentationExtractor):
    """Extractor que usa la API de OpenAI para obtener embeddings.

    Requiere OPENAI_API_KEY en variables de entorno.
    Soporta modelos: text-embedding-3-small, text-embedding-3-large, text-embedding-ada-002
    """

    def __init__(
        self,
        model: str = "text-embedding-3-small",
        api_key: str | None = None,
        dimension: int | None = None,
    ):
        """Inicializa el extractor.

        Args:
            model: Modelo de embeddings a usar.
            api_key: API key de OpenAI. Si es None, usa OPENAI_API_KEY del entorno.
            dimension: Dimensión del embedding. Si es None, usa la default del modelo.
        """
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY no proporcionada. "
                "Pasa api_key= o configura la variable de entorno OPENAI_API_KEY"
            )

        # Dimensiones por defecto según modelo
        self._dimension_map = {
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
            "text-embedding-ada-002": 1536,
        }
        self.dimension = dimension or self._dimension_map.get(model, 1536)

        # Lazy import para evitar dependencia si no se usa
        self._client = None

    @property
    def client(self):
        """Inicializa el cliente de OpenAI lazy."""
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.api_key)
            except ImportError:
                raise ImportError(
                    "openai no está instalado. Instala con: pip install openai"
                ) from None
        return self._client

    def extract(self, prompt: str) -> np.ndarray:
        """Extrae embedding de un prompt usando OpenAI API.

        Args:
            prompt: Texto a embedir.

        Returns:
            Vector numpy de dimensión self.dimension.
        """
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=prompt,
                dimensions=self.dimension,
            )
            embedding = response.data[0].embedding
            return np.array(embedding, dtype=np.float32)
        except (ValueError, KeyError, IndexError) as e:
            raise RuntimeError(f"Error obteniendo embedding de OpenAI: {e}") from e

    def get_dimension(self) -> int:
        """Retorna la dimensión del embedding."""
        return self.dimension

    def extract_batch(self, prompts: list[str]) -> np.ndarray:
        """Extrae embeddings de múltiples prompts en una sola llamada.

        Args:
            prompts: Lista de textos a embedir.

        Returns:
            Matriz numpy de forma (len(prompts), self.dimension).
        """
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=prompts,
                dimensions=self.dimension,
            )
            embeddings = [item.embedding for item in response.data]
            return np.array(embeddings, dtype=np.float32)
        except (ValueError, KeyError, IndexError) as e:
            raise RuntimeError(f"Error obteniendo embeddings batch de OpenAI: {e}") from e
