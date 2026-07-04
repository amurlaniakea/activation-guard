# Tasks: Feature 004 - Adapter vLLM

## T-001: Estructura del Adapter
- [ ] Crear archivo `vllm_adapter.py`
- [ ] Definir clase con herencia correcta
- [ ] Configurar imports

## T-002: Constructor y Configuración
- [ ] Implementar __init__ con parámetros
- [ ] Auto-detect de dimensión
- [ ] Setup de cliente HTTP

## T-003: Método extract()
- [ ] POST request a /v1/embeddings
- [ ] Parse response
- [ ] Error handling

## T-004: Método extract_batch()
- [ ] Batch request implementation
- [ ] Response parsing y stacking
- [ ] Optimización

## T-005: Retry Logic
- [ ] Wrapper con backoff
- [ ] Clasificación de errores
- [ ] Logging

## T-006: Tests
- [ ] Mock de servidor vLLM
- [ ] Test extract()
- [ ] Test extract_batch()
- [ ] Test timeout
- [ ] Test retry logic
- [ ] Test dimension detection

## T-007: Documentación
- [ ] Ejemplo en README
- [ ] Setup guide
- [ ] Notas de compatibilidad

## T-008: Integración
- [ ] Export en adapters/__init__.py
- [ ] Export en __init__.py principal
- [ ] Actualizar roadmap

## Progreso
- [ ] Feature completa
- [ ] Tests pasando
- [ ] Coverage >80%
- [ ] Linting limpio
- [ ] Commit y push
