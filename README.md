# activation-guard

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Tests](https://img.shields.io/endpoint?url=https:// Shield)](https://github.com/amurlaniakea/activation-guard/actions)
[![codecov](https://img.shields.io/codecov/c/github/amurlaniakea/activation-guard)](https://codecov.io/gh/amurlaniakea/activation-guard)

Framework de guardrail **training-free** basado en representaciones internas de LLMs.

## Características

- ✅ **Training-free**: No requiere fine-tuning de modelos
- ✅ **Multi-backend**: Soporta OpenAI, HuggingFace, Ollama, vLLM
- ✅ **Multi-representación**: Usa embeddings, activaciones y más
- ✅ **Configurable**: Adaptación por dominio (seguridad, código, médica, etc.)
- ✅ **Low-latency**: <50ms por prompt en CPU

## Instalación

```bash
# Requiere Python 3.11+
pip install activation-guard
```

## Uso básico

```python
from activation_guard import Guardrail

# Crear guardrail
guard = Guardrail(backend="openai", threshold=0.5)

# Verificar prompt
result = guard.check("¿Cómo hackear un banco?")
print(f"Prompt {'seguro' if result.safe else 'inseguro'} - confidence: {result.confidence:.2f}")
```

## CLI

```bash
# Uso básico
python -m activation_guard.cli "¿Cómo hackear un banco?"

# Modo verbose
python -m activation_guard.cli "¿Cómo hackear un banco?" --verbose

# Con threshold personalizado
python -m activation_guard.cli "Prompt" --threshold 0.7
```

## API REST

```bash
curl -X POST http://localhost:8000/v1/guard \
  -H "Content-Type: application/json" \
  -d '{"prompt": "¿Cómo hackear un banco?"}'
```

## Roadmap

- [x] Core API y representaciones básicas
- [ ] Adapter OpenAI embeddings
- [ ] Adapter HuggingFace
- [ ] Adapter vLLM
- [ ] Adapter Ollama
- [ ] Multi-representación con Fisher weighting
- [ ] Benchmark de comparación
- [ ] Documentación técnica

## Contribuciones

1. Fork del repo
2. Crear rama feature/nueva-caracteristica
3. Commit cambios
4. Push a la rama
5. Abrir Pull Request

## Licencia

AGPL-3.0 — Pedro Sordo Martínez (Sil)