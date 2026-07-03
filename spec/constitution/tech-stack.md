# Tech Stack — activation-guard

## Stack principal
| Capa | Tecnología | Versión | Justificación |
|------|------------|---------|---------------|
| Lenguaje | Python | 3.12 | Mayor compatibilidad con HuggingFace, Transformers |
| Framework | FastAPI | 0.110 | Rápido, fácil de documentar, soporta OpenAPI |
| DB | None | - | No requiere base de datos |
| ORM/ODM | None | - | No se necesita persistencia |
| Testing | pytest + pytest-cov | - | Testing unitario y cobertura |
| Lint/Format | ruff + mypy | - | Linter y checker de tipos |
| CI/CD | GitHub Actions | - | Integración continua automática |
| Documentación | mkdocs | - | Generación automática de docs |

## Convenciones de código
- **Estilo**: PEP 8 + Black
- **Naming**: snake_case para funciones, CamelCase para clases
- **Commits**: Conventional Commits
- **Branching**: GitFlow (main, develop, feature/*)

## Arquitectura
- **Patrón**: Clean Architecture + Modular Monolith
- **Estructura carpetas**:
  ```
  src/
  ├── activation_guard/
  │   ├── core/              # Lógica central
  │   ├── adapters/          # Adaptadores de entrada/salida
  │   ├── models/            # Tipos de datos
  │   ├── utils/             # Funciones auxiliares
  │   └── __init__.py
  ├── tests/
  └── docs/
  ```

## Dependencias clave
| Paquete | Propósito | Licencia |
|---------|-----------|----------|
| transformers | Extracción de representaciones | Apache 2.0 |
| sentence-transformers | Embeddings de texto | Apache 2.0 |
| scikit-learn | kNN y estadísticas | BSD 3-Clause |
| fastapi | API REST | MIT |
| pydantic | Validación de datos | MIT |

## Infraestructura
- **Hosting**: GitHub + PyPI
- **Contenedores**: No necesarios (librería pura)
- **Observabilidad**: Logging básico con structlog
- **Secrets**: No se requieren

---