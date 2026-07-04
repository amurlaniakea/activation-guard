# Spec — OpenAI Embeddings Adapter (002)

## Qué hace
Implementa un adapter para obtener embeddings usando la API de OpenAI, permitiendo usar el guardrail con representaciones de alta calidad sin necesidad de GPU local.

## Contexto / Motivación
OpenAI provee embeddings de alta calidad (text-embedding-3-small, text-embedding-3-large) que son ideales para el guardrail. Este adapter permite:
- Usar representaciones reales en lugar de dummy
- Aprovechar la infraestructura de OpenAI sin GPU local
- Fácil integración con el core del guardrail

## Criterios de aceptación (AC)

| ID | Criterio | Cómo se verifica |
|----|----------|------------------|
| AC-1 | Extrae embedding de un prompt usando OpenAI API | Test unitario con mock |
| AC-2 | Soporta múltiples modelos (small, large, ada-002) | Test con diferentes modelos |
| AC-3 | Permite dimensión personalizada | Test con dimension=256 |
| AC-4 | Soporta batch de prompts | Test de extract_batch |
| AC-5 | Manejo de errores claro (API key inválida, rate limit) | Test de errores |

## Casos de uso / User Stories
- **Como** usuario del guardrail **quiero** usar embeddings de OpenAI **para** mayor precisión sin GPU
- **Como** desarrollador **quiero** configurar la API key vía entorno **para** no hardcodear credenciales
- **Como** usuario avanzado **quiero** elegir el modelo **para** balancear costo/precisión

## Reglas de negocio / Edge cases
| Escenario | Comportamiento esperado |
|-----------|-------------------------|
| API key no proporcionada | Lanza ValueError claro |
| Rate limit de OpenAI | Reintenta con backoff o lanza error claro |
| Modelo no soportado | Lanza ValueError con lista de modelos válidos |
| Prompt vacío | Retorna embedding de dimensión correcta (vector cero o error) |

## API / Interfaces (si aplica)
### Clase pública
```python
class OpenAIEmbeddingExtractor(RepresentationExtractor):
    def __init__(model="text-embedding-3-small", api_key=None, dimension=None)
    def extract(prompt: str) -> np.ndarray
    def extract_batch(prompts: list[str]) -> np.ndarray
    def get_dimension() -> int
```

## No funcionales
- **Performance**: Latencia < 500ms por llamada (depende de red)
- **Seguridad**: API key nunca loggeada, solo en memoria
- **Accesibilidad**: Documentación clara de costos de API

## Dependencias
- Requiere: `openai` package (pip install openai)
- Requiere: variable de entorno OPENAI_API_KEY o api_key explícita
- Bloquea: ninguna

---
*Documento vivo — actualizar antes de cualquier cambio importante en la feature*
