#!/usr/bin/env python3
"""CLI para activation-guard"""

import argparse
import sys

from activation_guard import Guardrail, GuardrailRequest


def main():
    parser = argparse.ArgumentParser(description="activation-guard CLI")
    parser.add_argument("prompt", help="Prompt a verificar")
    parser.add_argument("--backend", "-b", default="openai", help="Backend a usar")
    parser.add_argument("--threshold", "-t", type=float, default=0.5, help="Umbral de seguridad")
    parser.add_argument("--domain", "-d", default=None, help="Dominio específico")
    parser.add_argument("--verbose", "-v", action="store_true", help="Salida detallada")

    args = parser.parse_args()

    request = GuardrailRequest(
        prompt=args.prompt,
        backend=args.backend,
        threshold=args.threshold,
        domain=args.domain
    )

    guard = Guardrail(backend=args.backend)
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
