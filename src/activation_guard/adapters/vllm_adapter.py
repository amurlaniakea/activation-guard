"""vLLM adapter for activation-guard.

Provides embedding extraction from models served via vLLM HTTP API.
vLLM exposes OpenAI-compatible /v1/embeddings endpoint.
"""

import time
from typing import Any

import httpx
import numpy as np

from activation_guard.core.extractor import RepresentationExtractor


class VLLMEmbeddingExtractor(RepresentationExtractor):
    """Extract embeddings from vLLM-served models via HTTP API.

    vLLM provides an OpenAI-compatible REST API at /v1/embeddings.
    This adapter connects to a running vLLM server to extract embeddings
    from any model it serves (Llama, Mistral, Qwen, etc.).

    Args:
        base_url: Base URL of vLLM server (e.g., "http://localhost:8000")
        model: Model identifier (default: uses server's default model)
        dimension: Embedding dimension (auto-detected if None)
        timeout: Request timeout in seconds (default: 30)
        max_retries: Maximum retry attempts for failed requests (default: 3)
        normalize: Normalize embeddings to unit length (default: False)

    Example:
        >>> extractor = VLLMEmbeddingExtractor(
        ...     base_url="http://localhost:8000",
        ...     model="meta-llama/Llama-2-7b-hf"
        ... )
        >>> embedding = extractor.extract("Hello world")
    """

    def __init__(
        self,
        base_url: str,
        model: str | None = None,
        dimension: int | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        normalize: bool = False,  # noqa: FBT001, FBT002  # noqa: FBT001, FBT002
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.max_retries = max_retries
        self.normalize = normalize

        # HTTP client with connection pooling
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
        )

        # Auto-detect dimension if not provided
        if dimension is None:
            self._dimension = self._detect_dimension()
        else:
            self._dimension = dimension

    def get_dimension(self) -> int:
        """Return the embedding dimension."""
        return self._dimension

    def _detect_dimension(self) -> int:
        """Auto-detect embedding dimension via test request.

        Returns:
            int: Embedding dimension

        Raises:
            RuntimeError: If dimension cannot be detected
        """
        try:
            test_embedding = self._make_request("test", retries=1)
            return len(test_embedding)
        except Exception as e:
            raise RuntimeError(
                f"Cannot auto-detect embedding dimension from {self.base_url}. "
                "Please specify dimension explicitly. Error: {e}"
            ) from e

    def _make_request(self, prompt: str, retries: int | None = None) -> list[float]:
        """Make embedding request with retry logic.

        Args:
            prompt: Input text to embed
            retries: Override max_retries for this request

        Returns:
            list[float]: Embedding vector

        Raises:
            httpx.HTTPStatusError: On 4xx errors (non-retryable)
            RuntimeError: On max retries exceeded
        """
        if retries is None:
            retries = self.max_retries

        payload: dict[str, Any] = {
            "input": [prompt],
        }
        if self.model:
            payload["model"] = self.model

        last_error = None
        for attempt in range(retries):
            try:
                response = self.client.post("/v1/embeddings", json=payload)

                # Don't retry 4xx errors (client errors)
                if 400 <= response.status_code < 500:
                    response.raise_for_status()

                # Retry on 5xx errors (server errors)
                if response.status_code >= 500:
                    last_error = httpx.HTTPStatusError(
                        f"Server error {response.status_code}",
                        request=response.request,
                        response=response,
                    )
                    if attempt < retries - 1:
                        wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                        time.sleep(wait_time)
                        continue
                    else:
                        raise RuntimeError(
                            f"Failed after {retries} retries: {last_error}"
                        ) from last_error

                response.raise_for_status()
                data = response.json()
                return data["data"][0]["embedding"]

            except (httpx.TimeoutException, httpx.ConnectError) as e:
                last_error = e
                if attempt < retries - 1:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                    continue
                else:
                    raise RuntimeError(
                        f"Failed to connect to vLLM server after {retries} attempts: {e}"
                    ) from e

        raise RuntimeError(f"Failed after {retries} retries: {last_error}")

    def extract(self, prompt: str) -> np.ndarray:
        """Extract embedding for a single prompt.

        Args:
            prompt: Input text to embed

        Returns:
            np.ndarray: Embedding vector of shape (dimension,)
        """
        embedding = self._make_request(prompt)
        vec = np.array(embedding, dtype=np.float32)

        if self.normalize:
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm

        return vec

    def extract_batch(self, prompts: list[str]) -> np.ndarray:
        """Extract embeddings for multiple prompts.

        Args:
            prompts: List of input texts to embed

        Returns:
            np.ndarray: Embedding matrix of shape (len(prompts), dimension)

        Note:
            Currently uses sequential requests. Batch optimization via
            single POST request is planned for future release.
        """
        embeddings = []
        for prompt in prompts:
            embedding = self._make_request(prompt)
            embeddings.append(embedding)

        matrix = np.array(embeddings, dtype=np.float32)

        if self.normalize:
            norms = np.linalg.norm(matrix, axis=1, keepdims=True)
            norms = np.where(norms > 0, norms, 1.0)  # Avoid division by zero
            matrix = matrix / norms

        return matrix

    def __del__(self):
        """Cleanup HTTP client on deletion."""
        if hasattr(self, "client"):
            self.client.close()
