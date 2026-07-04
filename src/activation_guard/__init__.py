"""activation-guard - Training-free LLM guardrail framework.

Framework de guardrail basado en representaciones internas de LLMs.
Soporta múltiples backends (OpenAI, HuggingFace, Ollama, vLLM) sin necesidad de fine-tuning.

Uso básico:

    from activation_guard import Guardrail

    guard = Guardrail(backend="openai")
    result = guard.check("¿Cómo hackear un banco?")
    print(f"Prompt {'seguro' if result.safe else 'inseguro'} - confidence: {result.confidence:.2f}")
"""

from .adapters.openai_adapter import OpenAIEmbeddingExtractor
from .core.guardrail import Guardrail
from .models.requests import GuardrailRequest, GuardrailResponse

__version__ = "0.1.0"
__author__ = "Pedro Sordo Martínez (Sil)"
__email__ = "amurlaniakea@example.com"
__license__ = "AGPL-3.0"

__all__ = [
    "Guardrail",
    "GuardrailRequest",
    "GuardrailResponse",
    "OpenAIEmbeddingExtractor",
]
