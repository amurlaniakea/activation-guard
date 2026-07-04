"""Tests para HuggingFace adapter."""

from unittest.mock import Mock, patch

import numpy as np
import pytest

from activation_guard.adapters.hf_adapter import SentenceTransformerExtractor


class TestSentenceTransformerExtractor:
    """Tests para SentenceTransformerExtractor."""

    def test_init_default_model(self):
        """Debe inicializar con modelo default MiniLM."""
        extractor = SentenceTransformerExtractor()
        assert extractor.model_name == "all-MiniLM-L6-v2"
        assert extractor.normalize_embeddings is True
        assert extractor.device in ["cpu", "cuda"]

    def test_init_custom_model(self):
        """Debe soportar modelos personalizados."""
        extractor = SentenceTransformerExtractor(
            model_name="all-mpnet-base-v2",
            normalize_embeddings=False,
        )
        assert extractor.model_name == "all-mpnet-base-v2"
        assert extractor.normalize_embeddings is False

    @patch("activation_guard.adapters.hf_adapter._import_sentence_transformer")
    def test_get_dimension_after_load(self, mock_import):
        """Dimensión debe ser correcta después de cargar el modelo."""
        mock_st_class = Mock()
        mock_instance = Mock()
        mock_instance.get_sentence_embedding_dimension.return_value = 384
        mock_st_class.return_value = mock_instance
        mock_import.return_value = mock_st_class

        extractor = SentenceTransformerExtractor(model_name="test-model")
        dim = extractor.get_dimension()
        assert dim == 384
        mock_instance.get_sentence_embedding_dimension.assert_called_once()

    @patch("activation_guard.adapters.hf_adapter._import_sentence_transformer")
    def test_extract_returns_correct_shape(self, mock_import):
        """Debe retornar vector de dimensión correcta."""
        mock_st_class = Mock()
        mock_instance = Mock()
        mock_instance.encode.return_value = np.array(
            [[0.1, 0.2, 0.3]], dtype=np.float32
        )
        mock_instance.get_sentence_embedding_dimension.return_value = 3
        mock_st_class.return_value = mock_instance
        mock_import.return_value = mock_st_class

        extractor = SentenceTransformerExtractor(model_name="test-model")
        result = extractor.extract("test prompt")

        assert isinstance(result, np.ndarray)
        assert result.shape == (3,)
        assert result.dtype == np.float32
        mock_instance.encode.assert_called_once()

    @patch("activation_guard.adapters.hf_adapter._import_sentence_transformer")
    def test_extract_batch_returns_correct_shape(self, mock_import):
        """Batch extraction debe retornar matriz 2D correcta."""
        mock_st_class = Mock()
        mock_instance = Mock()
        mock_instance.encode.return_value = np.array(
            [[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]], dtype=np.float32
        )
        mock_instance.get_sentence_embedding_dimension.return_value = 2
        mock_st_class.return_value = mock_instance
        mock_import.return_value = mock_st_class

        extractor = SentenceTransformerExtractor(model_name="test-model")
        prompts = ["prompt1", "prompt2", "prompt3"]
        result = extractor.extract_batch(prompts)

        assert isinstance(result, np.ndarray)
        assert result.shape == (3, 2)
        assert result.dtype == np.float32
        mock_instance.encode.assert_called_once_with(
            prompts, normalize_embeddings=True, batch_size=32, show_progress=False
        )

    def test_import_error_when_not_installed(self):
        """Debe lanzar ImportError claro si sentence-transformers no instalado."""
        with patch(
            "activation_guard.adapters.hf_adapter._import_sentence_transformer",
            side_effect=ImportError("no module"),
        ):
            extractor = SentenceTransformerExtractor()
            with pytest.raises(
                ImportError, match="sentence-transformers no está instalado"
            ):
                _ = extractor.model
