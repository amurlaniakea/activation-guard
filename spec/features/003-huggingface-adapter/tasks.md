# Tasks: Feature 003 - Adapter HuggingFace/Sentence Transformers

## T-001: Estructura del proyecto
**Estado**: Pendiente
**Descripción**: Crear archivo `src/activation_guard/adapters/hf_adapter.py` y actualizar `__init__.py` de adapters

## T-002: Clase base SentenceTransformerExtractor
**Estado**: Pendiente
**Descripción**: Implementar __init__ con model_name, device, normalize_embeddings. Property model con lazy import. Detect dimension automáticamente.

## T-003: Métodos abstractos
**Estado**: Pendiente
**Descripción**: Implementar extract() y extract_batch() usando model.encode(). Retornar np.float32 arrays correctos.

## T-004: Configuraciones avanzadas
**Estado**: Pendiente
**Descripción**: Soporte CUDA auto-detect, parámetros encode (max_length, show_progress_bar), documentation en docstrings.

## T-005: Tests unitarios
**Estado**: Pendiente
**Descripción**: 
- test_init_default_model()
- test_init_custom_model()
- test_get_dimension()
- test_import_error_when_not_installed()
- test_extract_returns_correct_shape() (mock)
- test_extract_batch_returns_correct_shape() (mock)

## T-006: Docs e integración
**Estado**: Pendiente
**Descripción**: Actualizar README.md sección HuggingFace, lista de modelos recomendados, commit + push a GitHub.

## Prioridad
Alta — sigue el orden lógico del roadmap y añade un backend local sin dependencias externas (a diferencia de OpenAI).

## Timebox Estimado
4 horas máx.

## Bloqueantes
Ninguno — depende solo de sentence-transformers que ya está en dependencies principales.
