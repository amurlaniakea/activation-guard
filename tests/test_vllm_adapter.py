"""Tests for vLLM adapter."""

from unittest.mock import Mock, patch

import httpx
import numpy as np
import pytest

from activation_guard.adapters.vllm_adapter import VLLMEmbeddingExtractor


class TestVLLMEmbeddingExtractor:
    """Test suite for VLLMEmbeddingExtractor."""

    def test_init_default_parameters(self):
        """Test initialization with default parameters."""
        with patch('httpx.Client'):
            extractor = VLLMEmbeddingExtractor(
                base_url="http://localhost:8000",
                dimension=4,
            )

            assert extractor.base_url == "http://localhost:8000"
            assert extractor.timeout == 30.0
            assert extractor.max_retries == 3
            assert extractor.normalize is False
            assert extractor.get_dimension() == 4

    def test_init_custom_parameters(self):
        """Test initialization with custom parameters."""
        with patch('httpx.Client'):
            extractor = VLLMEmbeddingExtractor(
                base_url="http://custom:8080",
                dimension=8,
                timeout=60.0,
                max_retries=5,
                normalize=True,
            )

            assert extractor.base_url == "http://custom:8080"
            assert extractor.timeout == 60.0
            assert extractor.max_retries == 5
            assert extractor.normalize is True
            assert extractor.get_dimension() == 8

    def test_extract_single_prompt(self):
        """Test extracting embedding for a single prompt."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"embedding": [0.1, 0.2, 0.3, 0.4]}]
        }

        with patch('httpx.Client') as mock_client:
            mock_client_instance = Mock()
            mock_client_instance.post.return_value = mock_response
            mock_client.return_value = mock_client_instance

            extractor = VLLMEmbeddingExtractor(
                base_url="http://localhost:8000",
                dimension=4,
            )
            embedding = extractor.extract("Hello world")

            assert isinstance(embedding, np.ndarray)
            assert embedding.shape == (4,)
            assert np.array_equal(embedding, np.array([0.1, 0.2, 0.3, 0.4], dtype=np.float32))

            call_args = mock_client_instance.post.call_args
            assert call_args[0][0] == "/v1/embeddings"
            assert call_args[1]["json"]["input"] == ["Hello world"]

    def test_extract_with_normalization(self):
        """Test embedding extraction with normalization enabled."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"embedding": [3.0, 4.0]}]  # Norm = 5.0
        }

        with patch('httpx.Client') as mock_client:
            mock_client_instance = Mock()
            mock_client_instance.post.return_value = mock_response
            mock_client.return_value = mock_client_instance

            extractor = VLLMEmbeddingExtractor(
                base_url="http://localhost:8000",
                dimension=2,
                normalize=True,
            )
            embedding = extractor.extract("Test")

            expected = np.array([3.0, 4.0], dtype=np.float32) / 5.0
            assert np.allclose(embedding, expected)

    def test_extract_batch(self):
        """Test batch embedding extraction."""
        mock_responses = [
            Mock(status_code=200, json=lambda: {"data": [{"embedding": [0.1, 0.2]}]}),
            Mock(status_code=200, json=lambda: {"data": [{"embedding": [0.3, 0.4]}]}),
            Mock(status_code=200, json=lambda: {"data": [{"embedding": [0.5, 0.6]}]}),
        ]

        with patch('httpx.Client') as mock_client:
            mock_client_instance = Mock()
            mock_client_instance.post.side_effect = mock_responses
            mock_client.return_value = mock_client_instance

            extractor = VLLMEmbeddingExtractor(
                base_url="http://localhost:8000",
                dimension=2,
            )
            embeddings = extractor.extract_batch(["Prompt 1", "Prompt 2", "Prompt 3"])

            assert isinstance(embeddings, np.ndarray)
            assert embeddings.shape == (3, 2)
            assert np.allclose(embeddings[0], [0.1, 0.2])
            assert np.allclose(embeddings[1], [0.3, 0.4])
            assert np.allclose(embeddings[2], [0.5, 0.6])

    def test_retry_on_server_error(self):
        """Test retry logic on 5xx server errors."""
        error_response = Mock(status_code=500, text="Internal Server Error")
        success_response = Mock(
            status_code=200,
            json=lambda: {"data": [{"embedding": [0.1, 0.2]}]}
        )

        with patch('httpx.Client') as mock_client:
            mock_client_instance = Mock()
            mock_client_instance.post.side_effect = [
                error_response,
                error_response,
                success_response,
            ]
            mock_client.return_value = mock_client_instance

            extractor = VLLMEmbeddingExtractor(
                base_url="http://localhost:8000",
                dimension=2,
                max_retries=3,
            )

            with patch('time.sleep'):
                embedding = extractor.extract("Test")

                assert isinstance(embedding, np.ndarray)
                assert mock_client_instance.post.call_count == 3

    def test_no_retry_on_client_error(self):
        """Test that 4xx errors are not retried."""
        error_response = Mock(status_code=400, text="Bad Request")
        error_response.raise_for_status = Mock(side_effect=httpx.HTTPStatusError(
            "Bad Request", request=Mock(), response=error_response
        ))

        with patch('httpx.Client') as mock_client:
            mock_client_instance = Mock()
            mock_client_instance.post.return_value = error_response
            mock_client.return_value = mock_client_instance

            extractor = VLLMEmbeddingExtractor(
                base_url="http://localhost:8000",
                dimension=2,
                max_retries=3,
            )

            with pytest.raises(httpx.HTTPStatusError):
                extractor.extract("Test")

            assert mock_client_instance.post.call_count == 1

    def test_max_retries_exceeded(self):
        """Test that RuntimeError is raised after max retries."""
        error_response = Mock(status_code=500, text="Internal Server Error")

        with patch('httpx.Client') as mock_client:
            mock_client_instance = Mock()
            mock_client_instance.post.return_value = error_response
            mock_client.return_value = mock_client_instance

            extractor = VLLMEmbeddingExtractor(
                base_url="http://localhost:8000",
                dimension=2,
                max_retries=2,
            )

            with patch('time.sleep'):
                with pytest.raises(RuntimeError, match="Failed after 2 retries"):
                    extractor.extract("Test")

                assert mock_client_instance.post.call_count == 2

    def test_connection_error_handling(self):
        """Test handling of connection errors."""
        with patch('httpx.Client') as mock_client:
            mock_client_instance = Mock()
            mock_client_instance.post.side_effect = httpx.ConnectError("Connection refused")
            mock_client.return_value = mock_client_instance

            extractor = VLLMEmbeddingExtractor(
                base_url="http://localhost:8000",
                dimension=2,
                max_retries=1,
            )

            with pytest.raises(RuntimeError, match="Failed to connect"):
                extractor.extract("Test")

    def test_timeout_handling(self):
        """Test handling of timeout errors."""
        with patch('httpx.Client') as mock_client:
            mock_client_instance = Mock()
            mock_client_instance.post.side_effect = httpx.TimeoutException("Timeout")
            mock_client.return_value = mock_client_instance

            extractor = VLLMEmbeddingExtractor(
                base_url="http://localhost:8000",
                dimension=2,
                max_retries=1,
            )

            with pytest.raises(RuntimeError, match="Failed to connect"):
                extractor.extract("Test")

    def test_cleanup_on_deletion(self):
        """Test that HTTP client is closed on deletion."""
        with patch('httpx.Client') as mock_client:
            mock_client_instance = Mock()
            mock_client.return_value = mock_client_instance

            extractor = VLLMEmbeddingExtractor(
                base_url="http://localhost:8000",
                dimension=4,
            )
            del extractor

            mock_client_instance.close.assert_called_once()
