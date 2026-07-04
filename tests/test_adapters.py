"""Tests para adapters."""

import os
from unittest.mock import Mock, patch

import numpy as np
import pytest

from activation_guard.adapters.openai_adapter import OpenAIEmbeddingExtractor


class TestOpenAIEmbeddingExtractor:
    """Tests para OpenAIEmbeddingExtractor."""

    def test_init_requires_api_key(self):
        """Debe requerir API key."""
        # Guardar valor original
        original_key = os.getenv("OPENAI_API_KEY")
        # Remover temporalmente
        if original_key:
            del os.environ["OPENAI_API_KEY"]

        try:
            with pytest.raises(ValueError, match="OPENAI_API_KEY"):
                OpenAIEmbeddingExtractor()
        finally:
            # Restaurar
            if original_key:
                os.environ["OPENAI_API_KEY"] = original_key

    def test_init_with_api_key(self):
        """Debe inicializar con API key explícita."""
        extractor = OpenAIEmbeddingExtractor(api_key="test-key")
        assert extractor.api_key == "test-key"
        assert extractor.get_dimension() == 1536  # default para text-embedding-3-small

    def test_init_with_model(self):
        """Debe soportar diferentes modelos."""
        extractor_small = OpenAIEmbeddingExtractor(
            model="text-embedding-3-small",
            api_key="test-key"
        )
        assert extractor_small.get_dimension() == 1536

        extractor_large = OpenAIEmbeddingExtractor(
            model="text-embedding-3-large",
            api_key="test-key"
        )
        assert extractor_large.get_dimension() == 3072

    def test_init_with_custom_dimension(self):
        """Debe permitir dimensión personalizada."""
        extractor = OpenAIEmbeddingExtractor(
            model="text-embedding-3-large",
            api_key="test-key",
            dimension=256
        )
        assert extractor.get_dimension() == 256

    @patch('openai.OpenAI')
    def test_extract_returns_correct_shape(self, mock_openai_class):
        """Debe retornar vector de dimensión correcta."""
        # Mock del cliente
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = [Mock(embedding=[0.1] * 1536)]
        mock_client.embeddings.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        extractor = OpenAIEmbeddingExtractor(api_key="test-key")
        result = extractor.extract("test prompt")

        assert isinstance(result, np.ndarray)
        assert result.shape == (1536,)
        assert result.dtype == np.float32

    @patch('openai.OpenAI')
    def test_extract_batch_returns_correct_shape(self, mock_openai_class):
        """Debe retornar matriz de forma correcta para batch."""
        # Mock del cliente
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = [
            Mock(embedding=[0.1] * 1536),
            Mock(embedding=[0.2] * 1536),
            Mock(embedding=[0.3] * 1536),
        ]
        mock_client.embeddings.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        extractor = OpenAIEmbeddingExtractor(api_key="test-key")
        result = extractor.extract_batch(["prompt1", "prompt2", "prompt3"])

        assert isinstance(result, np.ndarray)
        assert result.shape == (3, 1536)
        assert result.dtype == np.float32
