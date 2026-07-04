import unittest
from src.activation_guard.core.guardrail import Guardrail
from src.activation_guard.adapters.hf_adapter import SentenceTransformerExtractor
from src.activation_guard.models.requests import GuardrailRequest

class TestGuardrail(unittest.TestCase):
    def test_check_consistency(self):
        backend = "hf"
        extractor = SentenceTransformerExtractor()
        guard = Guardrail(backend=backend)
        guard.register_extractor(backend, extractor)
        prompt = GuardrailRequest(prompt="Este es un prompt de prueba")
        result1 = guard.check(prompt)
        result2 = guard.check(prompt)
        self.assertEqual(result1.confidence, result2.confidence)
