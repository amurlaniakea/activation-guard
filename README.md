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

## Adapter OpenAI

Para usar embeddings de OpenAI:

```bash
pip install activation-guard[openai]
export OPENAI_API_KEY="sk-..."
```

```python
from activation_guard import OpenAIEmbeddingExtractor

extractor = OpenAIEmbeddingExtractor(
    model="text-embedding-3-small",  # o text-embedding-3-large
    dimension=1536,  # opcional, default según modelo
)

# Extraer embedding de un prompt
embedding = extractor.extract("¿Cómo hackear un banco?")
print(f"Dimensión: {embedding.shape}")  # (1536,)

# Batch de prompts
embeddings = extractor.extract_batch(["prompt1", "prompt2", "prompt3"])
print(f"Batch shape: {embeddings.shape}")  # (3, 1536)
```

## Adapter HuggingFace

Para usar embeddings locales con Sentence Transformers:

```bash
pip install activation-guard[hf]
```

```python
from activation_guard import SentenceTransformerExtractor

extractor = SentenceTransformerExtractor(
    model="all-MiniLM-L6-v2",  # o all-mpnet-base-v2, multi-qa-MiniLM-L6-cos-v1
    device="cpu",  # "cuda" si tienes GPU, None para auto-detect
    normalize_embeddings=True,
)

# Extraer embedding de un prompt
embedding = extractor.extract("¿Cómo hackear un banco?")
print(f"Dimensión: {embedding.shape}")  # (384,) para MiniLM

# Batch de prompts
embeddings = extractor.extract_batch(["prompt1", "prompt2", "prompt3"])
print(f"Batch shape: {embeddings.shape}")  # (3, 384)

# Obtener dimensión del modelo
print(f"Dimensión: {extractor.get_dimension()}")  # 384
```

**Modelos recomendados:**
- `all-MiniLM-L6-v2` (384 dim) - Rápido y ligero, ideal para producción
- `all-mpnet-base-v2` (768 dim) - Mayor precisión, requiere más recursos
- `multi-qa-MiniLM-L6-cos-v1` (384 dim) - Optimizado para preguntas

## Adapter vLLM

Para usar embeddings desde modelos servidos via vLLM HTTP API:

```bash
pip install activation-guard
```

```python
from activation_guard import VLLMEmbeddingExtractor

extractor = VLLMEmbeddingExtractor(
    base_url="http://localhost:8000",  # vLLM server URL
    model="meta-llama/Llama-2-7b-hf",  # opcional, usa default del server
    dimension=4096,  # opcional, auto-detect si no se especifica
    timeout=30.0,
    max_retries=3,
    normalize=False,
)

# Extraer embedding de un prompt
embedding = extractor.extract("¿Cómo hackear un banco?")
print(f"Dimensión: {extractor.get_dimension()}")

# Batch de prompts
embeddings = extractor.extract_batch(["prompt1", "prompt2", "prompt3"])
print(f"Batch shape: {embeddings.shape}")  # (3, dimension)
```

**Características:**
- Retry automático con backoff exponencial (5xx, timeout, connection errors)
- Pool de conexiones HTTP con httpx para máximo throughput
- Auto-detección de dimensión del embedding
- Normalización L2 opcional de vectores

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
- [x] Adapter OpenAI embeddings
- [x] Adapter HuggingFace
- [x] Adapter vLLM
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