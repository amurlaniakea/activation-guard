# Tasks — Core Guardrail (001)

## Checklist de implementación (orden de ejecución)

### 0. Preparación
- [ ] **T001** — Leer y entender `spec.md` y `plan.md` completos
- [ ] **T002** — Crear rama `feature/001-core-guardrail` desde `main`
- [ ] **T003** — Verificar que tests existentes pasan (`pytest`)

### 1. Modelos / Datos
- [ ] **T010** — Crear modelos Pydantic para requests/responses (`src/activation_guard/models/`)
- [ ] **T011** — Crear clase base de extractor (`src/activation_guard/core/extractor.py`)
- [ ] **T012** — Crear clase principal de guardrail (`src/activation_guard/core/guardrail.py`)

### 2. Lógica de negocio / Servicios
- [ ] **T020** — Implementar lógica de kNN + Fisher weighting (`src/activation_guard/core/guardrail.py`)
- [ ] **T021** — Implementar método de clasificación (`src/activation_guard/core/guardrail.py`)
- [ ] **T022** — Tests unitarios para guardrail (`tests/test_core.py`)

### 3. API / Interfaces
- [ ] **T030** — Crear endpoint FastAPI `/v1/guard` (`src/activation_guard/main.py`)
- [ ] **T031** — Configurar ruta y validación (`src/activation_guard/main.py`)
- [ ] **T032** — Validación request/response (`src/activation_guard/models/`)
- [ ] **T033** — Tests integración API (`tests/test_api.py`)

### 4. Frontend / UI (si aplica)
- [ ] **T040** — No aplica

### 5. Calidad y cierre
- [ ] **T050** — Lint + format (`ruff format` && `ruff check`)
- [ ] **T051** — Tests suite completa (`pytest`) — target: 90%+
- [ ] **T052** — Actualizar docs si cambia API (`README.md`)
- [ ] **T053** — PR description con: qué cambia, cómo testear, rollback plan
- [ ] **T054** — Code review (pedir a Sil)
- [ ] **T055** — Merge a `main` tras CI verde + approval

---
## Definición de "Done" por tarea
- Código compila y pasa tests locales
- Lint/formato OK
- Tests nuevos cubren la funcionalidad (unit/integration según capa)
- Sin warnings nuevos en CI

## Notas / Blockers
- T020 depende de T010, T011
- T030 depende de T020
- T050 depende de todas las tareas anteriores

---