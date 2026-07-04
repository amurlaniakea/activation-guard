# Plan: Feature 003 - Adapter HuggingFace/Sentence Transformers

## Tasks de Implementación

### T-001: Estructura del proyecto
1. Crear archivo `src/activation_guard/adapters/hf_adapter.py`
2. Actualizar `src/activation_guard/adapters/__init__.py` para exportar el nuevo adapter
3. Añadir opción `[hf]` en `pyproject.toml` (opcional, ya tenemos sentence-transformers en main deps)

### T-002: Clase base SentenceTransformerExtractor
1. Implementar `__init__(self, model_name="all-MiniLM-L6-v2", device=None, normalize_embeddings=True)`
2. Implementar property `model` con lazy import de `sentence_transformers.SentenceTransformer`
3. Manejar ImportError claro si librería no instalada
4. Determinar dimension automáticamente desde `model.get_sentence_embedding_dimension()`

### T-003: Métodos abstractos
1. `extract(self, prompt: str) -> np.ndarray`:
   - Llamar a `self.model.encode(prompt, normalize_embeddings=self.normalize_embeddings)`
   - Retornar como np.float32 array
2. `extract_batch(self, prompts: list[str], batch_size: int = 32) -> np.ndarray`:
   - Usar `self.model.encode(prompts, batch_size=batch_size, ...)`
   - Retornar matriz 2D np.float32

### T-004: Configuraciones avanzadas
1. Soporte device automático: si CUDA disponible y user no especifica, usar GPU
2. Parámetros encode adicionales: max_length, show_progress_bar (opcional)
3. Documentar parámetros en docstrings

### T-005: Tests unitarios
1. `test_init_default_model()`: inicialización por defecto con MiniLM
2. `test_init_custom_model()`: inicialización con MPNet u otro modelo
3. `test_get_dimension()`: dimensiones correctas según modelo
4. `test_import_error_when_not_installed()`: mock que simula ImportError
5. `test_extract_returns_correct_shape()`: usar mock de model.encode
6. `test_extract_batch_returns_correct_shape()`: mock de encode con lista

### T-006: Integración y docs
1. Actualizar README.md: sección "Adapter HuggingFace" con ejemplo
2. Lista de modelos recomendados en docs
3. Ejemplo de uso CLI si aplica (o dejar solo programático por ahora)
4. Commit semántico + push a GitHub

## Orden de Ejecución

1. **T-001**: Estructura básica
2. **T-002**: Clase base con lazy import
3. **T-003**: Métodos extract y extract_batch
4. **T-004**: Configuraciones adicionales (device, etc.)
5. **T-005**: Tests unitarios
6. **T-006**: Docs e integración

## Criterios de Verificación

### Antes de cada commit:
- [ ] `ruff check src/activation_guard/adapters/hf_adapter.py` limpio
- [ ] `pytest tests/test_hf_adapter.py -v` pasando
- [ ] Type hints completos y correctos

### Al finalizar feature:
- [ ] Todos los tests passing
- [ ] Coverage >= 80% en hf_adapter.py
- [ ] Docs README actualizados
- [ ] Commit limpio con mensaje semántico
- [ ] Push exitoso a GitHub

## Risgos y Mitigaciones

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| sentence-transformers requiere torch pesado | Tiempo de install largo | Documentar dependencia, usar pyproject.optional-dependencies si es necesario |
| Modelos grandes consumen mucha memoria | Crashes en RAM limitada | Default a modelos pequeños (MiniLM), documentar requerimientos mínimos |
| CUDA vs CPU automático | User obtiene peor performance | Detectar CUDA disponible, advertir log al iniciar, permitir override explícito |
| Batching automático complejo | Overhead innecesario | Usar batching simple de librería, exponer parámetro batch_size opcional |

## Dependencias Externas

- HF Hub (descarga automática de modelos)
- transformers (backend)
- torch (backend de sentence-transformers)

## Notas de Diseño

### Lazy Import Pattern
Seguir el patrón de OpenAI adapter:
```python
@property
def model(self):
    if self._model is None:
        from sentence_transformers import SentenceTransformer
        self._model = SentenceTransformer(...)
    return self._model
```

### Dimension Detection
Obtener dimensión automáticamente:
```python
dim = self.model.get_sentence_embedding_dimension()
```

### Device Auto-detect
```python
import torch
if device is None:
    self.device = "cuda" if torch.cuda.is_available() else "cpu"
else:
    self.device = device
```

## Checklist Final
- [ ] Implementado T-001
- [ ] Implementado T-002
- [ ] Implementado T-003
- [ ] Implementado T-004
- [ ] Implementado T-005
- [ ] Implementado T-006
- [ ] Tests passing
- [ ] Ruff clean
- [ ] Docs actualizadas
- [ ] Commit + push
