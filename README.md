# Plataforma de investigación de derechos y edición asistida por IA — V2

El proyecto ahora abarca la identificación y clasificación de obras/ediciones, verificación de copyright y licencias comerciales, producción editorial futura con asistencia de IA, revisión jurídica/editorial y preparación de publicaciones para Amazon KDP. La publicación y transformación de libros reales **no están autorizadas** por el MVP.

- [Visión integral V2](docs/project-architecture/PROJECT_VISION.md)
- [Arquitectura mínima y contratos](docs/project-architecture/SYSTEM_DESIGN.md)
- [Política jurídica y KDP](docs/project-architecture/RIGHTS_KDP_POLICY.md)
- [ADR persistencia / SQLite / Actions](docs/project-architecture/ADR_001_STORAGE_AND_EXECUTION.md)
- [Seguridad, sincronización y diagnóstico del bloqueo](docs/project-architecture/SECURITY_SYNC_AND_BLOCKER.md)
- [Roadmap y roles](docs/project-architecture/ROADMAP_AND_HANDOFF.md)
- [Prototipo Python + SQLite sintético](tools/editorial_pipeline_prototype/README.md)

**El componente original Biblioteca Desktop V1 se conserva íntegro a continuación**, junto con sus documentos históricos ARCHITECTURE.md y REQUIREMENTS.md. Work Item #10 continúa separadamente; no hay libros ni catálogo privado en este repositorio público.

---

# Biblioteca Desktop

Biblioteca Desktop es un proyecto para una aplicación local de escritorio que permitirá navegar y buscar un catálogo de documentos en Windows.

## Especificación V1

Las fuentes canónicas del alcance y del diseño son:

- [REQUIREMENTS.md](REQUIREMENTS.md) — requisitos funcionales y no funcionales V1.
- [ARCHITECTURE.md](ARCHITECTURE.md) — arquitectura técnica, fronteras y estrategia de empaquetado V1.

El código del proyecto permanece separado del corpus documental. La implementación funcional comenzará en Work Items posteriores.
