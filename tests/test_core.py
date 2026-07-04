import unittest
import numpy as np
from src.activation_guard.core.guardrail import Guardrail
from src.activation_guard.models.requests import GuardrailRequest

class FakeExtractor:
    def get_dimension(self):
        return 4

    def extract(self, prompt):
        return np.array([1.0, 2.0, 3.0, 4.0])

    def extract_batch(self, prompts):
        return np.array([[1.0, 2.0, 3.0, 4.0]] * len(prompts))

class TestGuardrail(unittest.TestCase):
    def test_check_consistency(self):
        backend = "openai"
        extractor = FakeExtractor()
        guard = Guardrail(backend=backend)
        guard.register_extractor(backend, extractor)
        guard.add_examples(
            domain="default",
            safe_examples=["hola", "buenos dias"],
            unsafe_examples=["hackear banco", "crear virus"],
        )
        prompt = GuardrailRequest(prompt="Este es un prompt de prueba", backend=backend)
        result1 = guard.check(prompt)
        result2 = guard.check(prompt)
        self.assertEqual(result1.confidence, result2.confidence)
        self.assertNotIn("error", result1.details)

    def test_check_uses_real_extraction_not_random(self):
        """Confirma que dos prompts DISTINTOS con el mismo extractor determinista
        producen el MISMO resultado si el extractor devuelve el mismo vector
        (prueba que ya no hay np.random.rand en el pipeline)."""
        extractor = FakeExtractor()
        guard = Guardrail(backend="openai")
        guard.register_extractor("openai", extractor)
        guard.add_examples(
            domain="default",
            safe_examples=["hola"],
            unsafe_examples=["malo"],
        )
        req_a = GuardrailRequest(prompt="prompt A", backend="openai")
        req_b = GuardrailRequest(prompt="prompt B", backend="openai")
        result_a = guard.check(req_a)
        result_b = guard.check(req_b)
        # Mismo extractor determinista -> mismo vector -> mismo resultado
        self.assertEqual(result_a.confidence, result_b.confidence)

if __name__ == "__main__":
    unittest.main()
