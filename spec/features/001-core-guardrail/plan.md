# Plan — Core Guardrail (001)

## Enfoque técnico
El core se divide en:
1. **Extractor de representaciones**: Interface común para obtener embeddings/activaciones
2. **Clasificador kNN**: Usa múltiples representaciones con Fisher weighting
3. **API REST**: FastAPI endpoint con validación y logging

## Archivos a crear / modificar
| Archivo | Acción | Descripción |
|---------|--------|-------------|
| `src/activation_guard/core/guardrail.py` | crear | Lógica principal de guardrail |
| `src/activation_guard/core/extractor.py` | crear | Interface de extractor |
| `src/activation_guard/adapters/openai_adapter.py` | crear | Adapter OpenAI |
| `src/activation_guard/adapters/hf_adapter.py` | crear | Adapter HuggingFace |
| `src/activation_guard/models/requests.py` | crear | Tipos Pydantic para requests |
| `src/activation_guard/models/responses.py` | crear | Tipos Pydantic para responses |
| `tests/test_core.py` | crear | Tests unitarios |
| `tests/test_adapters.py` | crear | Tests de integración |

## Estructuras de datos / Modelos
```python
class GuardrailRequest(BaseModel):
    prompt: str
    backend: str = "openai"
    threshold: float = 0.5

class GuardrailResponse(BaseModel):
    safe: bool
    confidence: float
    details: dict
```

## API / Interfaces (detalle de implementación)
- **Endpoints nuevos**: 
  - `POST /v1/guard` - Evaluar seguridad de prompt
- **Endpoints modificados**: ninguno
- **Eventos / Mensajes**: logging de decisiones

## Algoritmos / Lógica clave
1. **Extractor de representaciones**:
   - Recibe prompt + backend
   - Llama al adapter correspondiente
   - Retorna vector de representación

2. **Clasificador kNN**:
   - Calcula distancia coseno con banco de ejemplos
   - Aplica Fisher weighting por capa
   - Retorna score promedio ponderado

3. **Decisión final**:
   - Si score > threshold → seguro
   - Si score ≤ threshold → inseguro

## Migraciones / Datos (si aplica)
- Ninguna

## Configuración / Environment variables
| Variable | Requerida | Default | Descripción |
|----------|-----------|---------|-------------|
| `DEFAULT_BACKEND` | No | "openai" | Backend por defecto |
| `DEFAULT_THRESHOLD` | No | 0.5 | Umbral de clasificación |
| `CACHE_SIZE` | No | 1000 | Tamaño de cache de representaciones |

## Seguridad
- **AuthN**: Ninguna (público)
- **AuthZ**: Ninguna (público)
- **Validación**: Pydantic + input sanitization
- **Rate limiting**: Ninguno (mvp)

## Testing strategy
| Tipo | Qué se testea | Herramienta | Cobertura objetivo |
|------|---------------|-------------|---------------------|
| Unit | Lógica de guardrail | pytest | 90% |
| Integration | Adapters de backend | pytest | 80% |
| E2E | API completa | pytest + httpx | 70% |

## Riesgos técnicos
| Riesgo | Mitigación |
|--------|------------|
| Incompatibilidades de representaciones | Validación de dimensión |
| Cache de representaciones | TTL + LRU |
| Latencia alta en backends | Timeout + fallback |

---