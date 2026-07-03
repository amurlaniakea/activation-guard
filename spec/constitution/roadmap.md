# Roadmap — activation-guard

## Visión general
Desarrollar un framework de guardrail universal basado en representaciones internas de LLMs. Primero lanzar soporte para 3 backends principales, luego expandir a más.

## Fases / Releases

### Fase 1 — MVP (Julio 2026)
**Objetivo**: Framework básico con soporte para 3 backends

| Feature ID | Feature | Prioridad | Estimación | Estado |
|------------|---------|-----------|------------|--------|
| 001 | Core API y representaciones básicas | P0 | 5 días | pendiente |
| 002 | Adapter OpenAI embeddings | P1 | 3 días | pendiente |
| 003 | Adapter HuggingFace | P1 | 3 días | pendiente |
| 004 | Adapter vLLM | P2 | 4 días | pendiente |
| 005 | Benchmark de comparación | P1 | 2 días | pendiente |

### Fase 2 — Expansión (Agosto 2026)
**Objetivo**: Soporte para más backends y mejoras de rendimiento

| Feature ID | Feature | Prioridad | Estimación | Estado |
|------------|---------|-----------|------------|--------|
| 006 | Adapter Ollama | P1 | 3 días | pendiente |
| 007 | Multi-representación con Fisher weighting | P0 | 5 días | pendiente |
| 008 | Soporte para múltiples modelos por backend | P2 | 4 días | pendiente |
| 009 | Documentación técnica y tutoriales | P1 | 3 días | pendiente |

### Fase 3 — Producción (Septiembre 2026)
**Objetivo**: Establecer como referencia de la industria

| Feature ID | Feature | Prioridad | Estimación | Estado |
|------------|---------|-----------|------------|--------|
| 010 | Integración con Langfuse | P2 | 3 días | pendiente |
| 011 | Dashboard de métricas | P3 | 5 días | pendiente |
| 012 | Plugin para FastAPI | P1 | 4 días | pendiente |

## Dependencias entre features
- `002` depende de `001`
- `003` depende de `001`
- `004` depende de `001`
- `005` depende de `001`, `002`, `003`, `004`

## Riesgos y mitigaciones
| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Incompatibilidades de modelos | Media | Alto | Pruebas con múltiples versiones |
| Latencia alta en backends | Alta | Medio | Benchmark y optimización de cache |
| Falta de datasets públicos | Baja | Bajo | Crear datasets propios o usar estándares |

---