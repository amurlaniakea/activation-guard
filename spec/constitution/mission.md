# Mission — activation-guard

## Qué construimos
Un framework de guardrail training-free basado en representaciones internas de LLMs que permite detectar prompts peligrosos, inseguros o fuera de contexto sin necesidad de fine-tuning.

## Para quién
- **Usuario principal**: Desarrolladores de sistemas LLM que requieren guardrails de seguridad en producción
- **Stakeholders**: Equipos de seguridad AI, ingenieros de ML, CTOs de startups de LLM

## Problema que resuelve
Los guardrails tradicionales requieren fine-tuning, tienen alta latencia y no se generalizan bien. Los métodos basados en activaciones ocultas son poderosos pero poco accesibles.

## Valor diferencial
- Training-free: no requiere reentrenar clasificadores
- Multi-backend: soporta modelos de diferentes proveedores (OpenAI, HuggingFace, Ollama, vLLM)
- Multi-representación: utiliza múltiples tipos de embeddings para mayor robustez
- Configurable por dominio: fácil adaptar a seguridad, código, médica, etc.

## Métricas de éxito (KPIs)
| Métrica | Target | Cómo se mide |
|---------|--------|--------------|
| F1 score | ≥ 0.85 en benchmark público | Pruebas unitarias con datasets estándar |
| Latencia promedio | < 50ms por prompt | Benchmark de inferencia |
| Soporte de modelos | ≥ 3 backends | Tests de integración |

## Fuera de alcance (Out of scope)
- Fine-tuning de modelos
- Soporte para modelos con arquitecturas no compatibles
- Interfaz web de administración

---
*Documento vivo — actualizar cuando cambie la visión del proyecto*