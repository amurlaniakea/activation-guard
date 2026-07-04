"""activation-guard - Training-free LLM guardrail framework.

Framework de guardrail basado en representaciones internas de LLMs.
Soporta múltiples backends (OpenAI, HuggingFace, Ollama, vLLM) sin necesidad de fine-tuning.

Uso básico:

    from activation_guard import Guardrail, GuardrailRequest
    from activation_guard.adapters import SentenceTransformerExtractor

    guard = Guardrail(backend="openai")
    guard.register_extractor("openai", SentenceTransformerExtractor())
    guard.add_examples(domain="default", safe_examples=["Hola mundo"], unsafe_examples=["Texto malicioso"])
    request = GuardrailRequest(prompt="¿Cómo hackear un banco?")
    result = guard.check(request)
    print(f"Prompt {'seguro' if result.safe else 'inseguro'} - confidence: {result.confidence:.2f}")
"""

from .adapters.hf_adapter import SentenceTransformerExtractor
from .adapters.openai_adapter import OpenAIEmbeddingExtractor
from .adapters.vllm_adapter import VLLMEmbeddingExtractor
from .core.guardrail import Guardrail
from .models.requests import GuardrailRequest, GuardrailResponse

__version__ = "0.1.0"
__author__ = "Pedro Sordo Martínez (Sil)"
__email__ = "amurlaniakea@gmail.com"
__license__ = "AGPL-3.0"

__all__ = [
    "Guardrail",
    "GuardrailRequest",
    "GuardrailResponse",
    "OpenAIEmbeddingExtractor",
    "SentenceTransformerExtractor",
    "VLLMEmbeddingExtractor",
]
