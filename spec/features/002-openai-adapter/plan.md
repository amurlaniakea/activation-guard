# Plan — OpenAI Embeddings Adapter (002)

## Enfoque técnico
- Clase que implementa `RepresentationExtractor`
- Usa `openai` package oficial
- Lazy initialization del cliente para evitar import si no se usa
- Soporte batch para eficiencia

## Archivos a crear / modificar
| Archivo | Acción | Descripción |
|---------|--------|-------------|
| `src/activation_guard/adapters/openai_adapter.py` | crear | Adapter OpenAI |
| `src/activation_guard/adapters/__init__.py` | crear | Export del módulo |
| `tests/test_adapters.py` | crear | Tests del adapter |
| `src/activation_guard/__init__.py` | modificar | Exportar OpenAIEmbeddingExtractor |

## Estructuras de datos / Modelos
```python
class OpenAIEmbeddingExtractor(RepresentationExtractor):
    model: str
    api_key: str
    dimension: int
    _client: Optional[OpenAI]
```

## API / Interfaces (detalle de implementación)
- **Métodos nuevos**: 
  - `extract(prompt: str) -> np.ndarray`
  - `extract_batch(prompts: list[str]) -> np.ndarray`
  - `get_dimension() -> int`

## Algoritmos / Lógica clave
1. **Inicialización**: 
   - Validar API key (entorno o explícita)
   - Configurar modelo y dimensión
2. **Extracción**:
   - Lazy init del cliente OpenAI
   - Llamar a `embeddings.create()`
   - Convertir response a numpy array

## Configuración / Environment variables
| Variable | Requerida | Default | Descripción |
|----------|-----------|---------|-------------|
| `OPENAI_API_KEY` | Sí (si no se pasa en constructor) | - | API key de OpenAI |

## Testing strategy
| Tipo | Qué se testea | Herramienta | Cobertura objetivo |
|------|---------------|-------------|---------------------|
| Unit | Inicialización, validación | pytest | 90% |
| Integration | Llamada real a API (opcional) | pytest + mock | 50% |

## Riesgos técnicos
| Riesgo | Mitigación |
|--------|------------|
| API key expuesta en logs | Nunca loggear, solo usar en memoria |
| Rate limit de OpenAI | Documentar, usuario debe manejar |
| Costos de API | Documentar precios por modelo |

---
