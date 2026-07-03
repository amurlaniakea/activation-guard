from typing import Any

from pydantic import BaseModel


class GuardrailRequest(BaseModel):
    """Solicitud para verificar seguridad de un prompt."""

    prompt: str
    backend: str = "openai"
    threshold: float = 0.5
    domain: str | None = None


class GuardrailResponse(BaseModel):
    """Respuesta con resultado de verificación."""

    safe: bool
    confidence: float
    details: dict[str, Any]
