# Tasks — OpenAI Embeddings Adapter (002)

## Checklist de implementación (orden de ejecución)

### 0. Preparación
- [ ] **T001** — Leer y entender `spec.md` y `plan.md` completos
- [ ] **T002** — Crear rama `feature/002-openai-adapter` desde `main`
- [ ] **T003** — Verificar que tests existentes pasan (`pytest`)

### 1. Implementación del adapter
- [ ] **T010** — Crear clase `OpenAIEmbeddingExtractor` (`src/activation_guard/adapters/openai_adapter.py`)
- [ ] **T011** — Implementar método `extract()` con llamada a OpenAI API
- [ ] **T012** — Implementar método `extract_batch()` para eficiencia
- [ ] **T013** — Implementar validación de API key y modelos

### 2. Tests
- [ ] **T020** — Tests de inicialización (API key requerida, modelos)
- [ ] **T021** — Tests de extracción con mocks
- [ ] **T022** — Tests de batch extraction
- [ ] **T023** — Tests de manejo de errores

### 3. Integración
- [ ] **T030** — Exportar desde `src/activation_guard/adapters/__init__.py`
- [ ] **T031** — Exportar desde `src/activation_guard/__init__.py`
- [ ] **T032** — Actualizar documentación del README

### 4. Calidad y cierre
- [ ] **T040** — Lint + format (`ruff format` && `ruff check`)
- [ ] **T041** — Tests suite completa (`pytest`) — target: 90%+
- [ ] **T042** — Actualizar tasks.md con checkboxes
- [ ] **T043** — Commit y push a rama feature
- [ ] **T044** — PR description con: qué cambia, cómo testear
- [ ] **T045** — Code review (pedir a Sil)
- [ ] **T046** — Merge a `main` tras CI verde + approval

---
## Definición de "Done" por tarea
- Código compila y pasa tests locales
- Lint/formato OK
- Tests nuevos cubren la funcionalidad
- Sin warnings nuevos en CI

## Notas / Blockers
- T010 depende de T001
- T020 depende de T010
- Requiere `pip install openai` para tests reales (opcional)

---
