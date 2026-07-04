"""HuggingFace Sentence Transformers adapter.

Per-file ignore: Pyright missing import (sentence-transformers is optional dependency).
"""
# pyright: reportMissingImports=false


import numpy as np

from ..core.extractor import RepresentationExtractor

__all__ = ["SentenceTransformerExtractor"]


def _import_sentence_transformer():
    """Importa SentenceTransformer con manejo de error claro."""
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer


class SentenceTransformerExtractor(RepresentationExtractor):
    """Extractor que usa Sentence Transformers de HuggingFace para embeddings.

    Requiere sentence-transformers instalado: pip install sentence-transformers
    Soporta modelos populares: all-MiniLM-L6-v2, all-mpnet-base-v2, multi-qa-MiniLM-L6-cos-v1
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        device: str | None = None,
        normalize_embeddings: bool = True,  # noqa: FBT001, FBT002
    ):
        """Inicializa el extractor.

        Args:
            model_name: Nombre del modelo de Sentence Transformers (HF Hub).
            device: "cuda", "cpu", o None (auto-detect).
            normalize_embeddings: Si True, normaliza embeddings para cosine similarity.
        """
        self.model_name = model_name
        self.normalize_embeddings = normalize_embeddings
        self._model = None
        self._dimension: int | None = None

        # Auto-detect device
        if device is None:
            try:
                import torch
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
            except ImportError:
                self.device = "cpu"
        else:
            self.device = device

    @property
    def model(self):
        """Carga lazy el modelo Sentence Transformer."""
        if self._model is None:
            try:
                sentence_transformer_cls = _import_sentence_transformer()
            except ImportError as e:
                raise ImportError(
                    "sentence-transformers no está instalado. Instala con: "
                    "pip install sentence-transformers"
                ) from e

            self._model = sentence_transformer_cls(
                self.model_name,
                device=self.device,
            )
            self._dimension = self._model.get_sentence_embedding_dimension()

        return self._model

    @property
    def dimension(self) -> int:
        """Retorna la dimensión del embedding."""
        if self._dimension is None:
            _ = self.model  # Trigger carga y detección
        return self._dimension

    def extract(self, prompt: str) -> np.ndarray:
        """Extrae embedding de un prompt usando Sentence Transformer.

        Args:
            prompt: Texto a embedir.

        Returns:
            Vector numpy de dimensión self.dimension.
        """
        embedding = self.model.encode(
            [prompt],
            normalize_embeddings=self.normalize_embeddings,
        )
        return embedding[0].astype(np.float32)

    def get_dimension(self) -> int:
        """Retorna la dimensión del embedding."""
        if self._dimension is None:
            _ = self.model  # Trigger carga y detección
        return self._dimension or 384  # Fallback seguro

    def extract_batch(self, prompts: list[str], batch_size: int = 32) -> np.ndarray:
        """Extrae embeddings de múltiples prompts en una sola llamada.

        Args:
            prompts: Lista de textos a embedir.
            batch_size: Tamaño de batch para encode (default 32).

        Returns:
            Matriz numpy de forma (len(prompts), self.dimension).
        """
        embeddings = self.model.encode(
            prompts,
            normalize_embeddings=self.normalize_embeddings,
            batch_size=batch_size,
        )
        return embeddings.astype(np.float32)
