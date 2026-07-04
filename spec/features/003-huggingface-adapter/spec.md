# Spec: Feature 003 - Adapter HuggingFace/Sentence Transformers

## Objetivo
Implementar un adapter que use `sentence-transformers` de HuggingFace para extraer embeddings locales sin necesidad de API externa.

## Alcance

### In-scope
- Implementar `SentenceTransformerExtractor` que herede de `RepresentationExtractor`
- Soportar modelos populares: `all-MiniLM-L6-v2`, `all-mpnet-base-v2`, `multi-qa-MiniLM-L6-cos-v1`
- Manejo lazy import de `sentence-transformers`
- Dimensiones por defecto según modelo (ej. MiniLM=384, MPNet=768)
- Batch extraction con batching automático si hay muchos prompts
- Tests unitarios con mock o modelo tiny local
- Documentación en README con ejemplo de uso

### Out-of-scope
- Fine-tuning de modelos
- Quantización avanzada (INT8/FP16)
- GPU acceleration setup (solo CPU default, documentar CUDA como opcional)
- Model cache configuration personalizada

## Criterios de Aceptación

### CA-001: Implementación básica
- [ ] Clase `SentenceTransformerExtractor` implementada en `src/activation_guard/adapters/hf_adapter.py`
- [ ] Hereda correctamente de `RepresentationExtractor`
- [ ] Método `__init__` acepta `model_name`, dimension (opcional), device (cpu/cuda)
- [ ] Métodos abstractos implementados: `extract()`, `extract_batch()`, `get_dimension()`

### CA-002: Soporte de modelos
- [ ] Default: `all-MiniLM-L6-v2` (384 dim)
- [ ] Soporte explícito para `all-mpnet-base-v2` (768 dim)
- [ ] Support explícito para `multi-qa-MiniLM-L6-cos-v1` (384 dim)
- [ ] Puede aceptar cualquier modelo compatible de HF Hub

### CA-003: Lazy import
- [ ] Import de `sentence_transformers` ocurre dentro del método/client property
- [ ] Si no instalado, lanzar `ImportError` claro con instrucciones de instalación
- [ ] Dependencia opcional: `[hf]` en pyproject.toml

### CA-004: Extracción individual
- [ ] `extract(prompt: str)` retorna `np.ndarray` de dimensión correcta
- [ ] dtype: `np.float32`
- [ ] shape: `(dimension,)`

### CA-005: Extracción batch
- [ ] `extract_batch(prompts: list[str])` retorna `np.ndarray` 2D
- [ ] shape: `(len(prompts), dimension)`
- [ ] Usa `model.encode()` con `batch_size` configurable (default=32)
- [ ] Normalización opcional (`normalize_embeddings=True`)

### CA-006: Configuración
- [ ] Soporte para `device="cpu"` o `"cuda"`
- [ ] Cache dir configurable (HF_HOME/HF_CACHE_DIR)
- [ ] Max length token configurable (default=128 o auto)

### CA-007: Tests
- [ ] Test inicialización con model name diferente
- [ ] Test dimensions correctas por modelo
- [ ] Test extract retorna shape correcto (mock o tiny model)
- [ ] Test batch extraction shape correcto
- [ ] Test ImportError si no instalada la librería

### CA-008: Docs
- [ ] Ejemplo en README.md sección "Adapter HuggingFace"
- [ ] Lista de modelos recomendados con sus dimensiones
- [ ] Requisitos de instalación: `pip install activation-guard[hf]`

## Dependencias
- `sentence-transformers>=2.2.0` (ya declarada en dependencies principales, se mantiene así)
- `transformers>=4.38.0` (ya declarada)
- `torch` (dependencia automática de sentence-transformers)

## Notas de Implementación
- Usar `@property` para el modelo lazy load como en OpenAI adapter
- Considerar usar `tqdm` para progreso en batch grande (opcional)
- Normalizar embeddings por defecto (cosine similarity funciona mejor con normalizados)
- Caché local de modelos en `~/.cache/huggingface/` automáticamente manejado por librería

## Métricas de Calidad
- Tests: Mínimo 6 tests unitarios
- Coverage: >= 80% en huggingface_adapter.py
- Ruff: 0 errores, 0 warnings
- Tipo hints: Completos y correctos (mypy clean si se ejecuta)

## Timeline Estimado
- Implementation: 2-3 horas
- Tests: 1 hora
- Docs + refinement: 30 min
- **Total**: ~4 horas
