#!/usr/bin/env python3
"""CLI para activation-guard"""

import argparse
import sys
from activation_guard import Guardrail, GuardrailRequest
from activation_guard.adapters.hf_adapter import SentenceTransformerExtractor


def main():
    parser = argparse.ArgumentParser(description="activation-guard CLI")
    parser.add_argument("prompt", help="Prompt a verificar")
    parser.add_argument("--backend", "-b", default="openai", help="Backend a usar")
    parser.add_argument("--threshold", "-t", type=float, default=0.5, help="Umbral de seguridad")
    parser.add_argument("--domain", "-d", default=None, help="Dominio específico")
    parser.add_argument("--verbose", "-v", action="store_true", help="Salida detallada")

    args = parser.parse_args()

    # Registrar extractor por defecto
    extractor = SentenceTransformerExtractor()
    guard = Guardrail(backend=args.backend)
    guard.register_extractor(args.backend, extractor)

    # Agregar ejemplos safe/unsafe
    guard.add_examples(domain="default", safe_examples=["Hola mundo"], unsafe_examples=["Texto malicioso"])

    request = GuardrailRequest(
        prompt=args.prompt,
        backend=args.backend,
        threshold=args.threshold,
        domain=args.domain
    )

    response = guard.check(request)

    if args.verbose:
        print(f"Prompt: {args.prompt}")
        print(f"Safe: {response.safe}")
        print(f"Confidence: {response.confidence:.3f}")
        print(f"Details: {response.details}")
    else:
        print(f"{'✅ SAFE' if response.safe else '❌ UNSAFE'} - confidence: {response.confidence:.3f}")

    return 0 if response.safe else 1

if __name__ == "__main__":
    sys.exit(main())
