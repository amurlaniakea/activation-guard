# Feature 004: Adapter vLLM

## Descripción
Implementar un adapter para extraer embeddings desde modelos desplegados en vLLM, permitiendo acceso a representaciones internas de LLMs en producción.

## Casos de Uso
- Guardrails en sistemas de producción con vLLM
- Acceso a embeddings de modelos open-source (Llama, Mistral, etc.)
- Integración con infraestructura existente de vLLM

## Requisitos Funcionales

### RF-1: Conexión a vLLM
- Debe conectarse a un servidor vLLM via HTTP API
- Soporte para endpoint estándar `/v1/embeddings`
- Configuración de URL base y autenticación (si aplica)

### RF-2: Extracción de Embeddings
- Extraer embeddings de prompts individuales
- Soporte batch para múltiples prompts
- Normalización opcional de vectores

### RF-3: Manejo de Errores
- Timeout configurable para requests HTTP
- Reintentos con backoff exponencial
- Mensajes de error claros y accionables

### RF-4: Configuración
- Modelo personalizable (default: modelo cargado en vLLM)
- Dimensión del embedding (auto-detect o manual)
- Device selection (auto desde servidor vLLM)

## Requisitos No Funcionales

### RNF-1: Rendimiento
- Latencia <100ms por prompt (network-bound)
- Throughput >50 req/s en batch mode
- Pool de conexiones HTTP reutilizable

### RNF-2: Dependencias
- `requests` o `httpx` para HTTP client
- Sin dependencia directa de vLLM (solo API REST)

### RNF-3: Testing
- Mock del servidor vLLM en tests
- Cobertura >80% en adapter
- Tests de timeout y retry logic

## Criterios de Aceptación
- [ ] Implementación en `src/activation_guard/adapters/vllm_adapter.py`
- [ ] Tests unitarios con mocks
- [ ] Documentación de uso con ejemplo
- [ ] Export en `__init__.py` principal
- [ ] Coverage >80%
- [ ] Linting limpio (ruff)

## Notas de Diseño
- vLLM expone API compatible con OpenAI (`/v1/embeddings`)
- Usar `httpx` para async-ready si es necesario en el futuro
- No requerir instalación de vLLM localmente
- Auto-detect de dimensión via request de prueba
