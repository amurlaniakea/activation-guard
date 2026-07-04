# Plan: Feature 004 - Adapter vLLM

## Tareas de Implementación

### T-001: Estructura del Adapter
1. Crear `src/activation_guard/adapters/vllm_adapter.py`
2. Definir clase `VLLMEmbeddingExtractor` heredando de `RepresentationExtractor`
3. Configurar imports: `httpx`, `numpy`, base classes

### T-002: Constructor y Configuración
1. Parámetros: `base_url`, `model`, `dimension`, `timeout`, `max_retries`
2. Auto-detect de dimensión si no se especifica
3. Cliente HTTP con pool de conexiones

### T-003: Método extract()
1. POST request a `/v1/embeddings`
2. Payload: `{"model": model, "input": [prompt]}`
3. Parse response: `response["data"][0]["embedding"]`
4. Convertir a numpy array
5. Manejo de errores HTTP y timeout

### T-004: Método extract_batch()
1. POST request con lista de prompts
2. Parse response: `response["data"][i]["embedding"]` para cada item
3. Stacking en matriz numpy (N, dim)
4. Optimización: single request vs múltiples

### T-005: Retry Logic
1. Wrapper para requests con backoff exponencial
2. Reintentos en: 5xx, timeout, connection errors
3. No reintentar en: 4xx (client errors)
4. Logging de reintentos

### T-006: Tests
1. Mock de servidor vLLM con responses predefinidas
2. Test extract() single prompt
3. Test extract_batch() múltiple prompts
4. Test timeout handling
5. Test retry logic (simulate 500, then success)
6. Test dimension auto-detect

### T-007: Documentación
1. Ejemplo de uso en README
2. Configuración de vLLM server (setup guide)
3. Notas sobre compatibilidad con OpenAI API

### T-008: Integración
1. Export en `adapters/__init__.py`
2. Export en `src/activation_guard/__init__.py`
3. Actualizar roadmap con estado "done"

## Dependencias
- `httpx` para HTTP client (async-ready)
- vLLM server para testing manual (opcional)

## Estimación
- 4 días de trabajo
- Prioridad: P2
