# Spec — Core Guardrail (001)

## Qué hace
Implementa la lógica central del guardrail: recibir un prompt, extraer representaciones, comparar con bancos de ejemplo usando kNN, y devolver una clasificación de seguridad.

## Contexto / Motivación
Este es el núcleo del framework. Permite evaluar la seguridad de un prompt sin necesidad de entrenar modelos, usando representaciones internas de LLMs.

## Criterios de aceptación (AC)

| ID | Criterio | Cómo se verifica |
|----|----------|------------------|
| AC-1 | Dado un prompt, extrae representaciones de un backend | Test unitario con mock de backend |
| AC-2 | Clasifica un prompt como seguro/inseguro con score > 0.5 | Test con dataset de prueba |
| AC-3 | Soporta múltiples backends (OpenAI, HuggingFace, etc.) | Test de integración para cada backend |
| AC-4 | Retorna score de confianza y decisión binaria | Test de schema de respuesta |
| AC-5 | Latencia < 100ms por prompt en CPU | Benchmark de inferencia |

## Casos de uso / User Stories
- **Como** desarrollador de LLM **quiero** evaluar un prompt en tiempo real **para** evitar respuestas inseguras
- **Como** ingeniero de seguridad **quiero** configurar diferentes bancos por dominio **para** adaptar el guardrail a mi contexto
- **Como** usuario de API **quiero** recibir respuesta estructurada **para** integrar fácilmente en pipelines

## Reglas de negocio / Edge cases
| Escenario | Comportamiento esperado |
|-----------|-------------------------|
| Prompt vacío | Retorna "inseguro" con score 0.0 |
| Backend no disponible | Lanza excepción específica |
| Representación inválida | Retorna "inseguro" con score 0.0 |
| Score cercano a 0.5 | Retorna "inseguro" por defecto |

## API / Interfaces (si aplica)
### Endpoints
| Método | Ruta | Request | Response | Códigos |
|--------|------|---------|----------|---------|
| POST | `/v1/guard` | `{ "prompt": "..." }` | `{ "safe": true, "confidence": 0.85 }` | 200, 400, 500 |

### Contratos de datos
```json
{
  "prompt": "string",
  "backend": "string",
  "threshold": "float"
}
```

```json
{
  "safe": "boolean",
  "confidence": "float",
  "details": "object"
}
```

## No funcionales
- **Performance**: p95 < 50ms
- **Seguridad**: Validación de input, manejo de errores
- **Accesibilidad**: API REST estándar

## Dependencias
- Requiere: ninguna
- Bloquea: ninguna

---
*Documento vivo — actualizar antes de cualquier cambio importante en la feature*