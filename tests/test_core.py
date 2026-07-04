import pytest

from activation_guard.core.guardrail import Guardrail
from activation_guard.models.requests import GuardrailRequest, GuardrailResponse


def test_guardrail_initialization():
    """Test de inicialización del guardrail"""
    guard = Guardrail()
    assert guard.backend == "openai"
    assert guard.threshold == 0.5

def test_guardrail_request_model():
    """Test del modelo de solicitud"""
    request = GuardrailRequest(prompt="Hola", backend="openai", threshold=0.7)
    assert request.prompt == "Hola"
    assert request.backend == "openai"
    assert request.threshold == 0.7

def test_guardrail_response_model():
    """Test del modelo de respuesta"""
    response = GuardrailResponse(
        safe=True,
        confidence=0.8,
        details={"reason": "test"}
    )
    assert response.safe is True
    assert response.confidence == 0.8
    assert response.details["reason"] == "test"

def test_guardrail_check():
    """Test de verificación básica"""
    guard = Guardrail()
    request = GuardrailRequest(prompt="Test prompt")
    response = guard.check(request)

    # Debe devolver una respuesta válida
    assert isinstance(response, GuardrailResponse)
    assert hasattr(response, 'safe')
    assert hasattr(response, 'confidence')
    assert hasattr(response, 'details')

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
