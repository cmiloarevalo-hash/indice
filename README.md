# Biblioteca — Investigación documental y clasificación de derechos

**Objetivo operativo:** investigar fuentes, licencias y derechos de los 28.781 registros bibliográficos del catálogo privado, preservando `E/UNKNOWN` cuando no existe evidencia jurídica suficiente.

**Único Work Item rector:** [#19 — Supervisión continua](https://github.com/cmiloarevalo-hash/indice/issues/19).  
**Código vigente en revisión:** [PR #20](https://github.com/cmiloarevalo-hash/indice/pull/20), sin merge.  
**Mandato y protocolo obligatorio para agentes:** [SUPERVISION_AUTHORITY_AND_EXECUTION_POLICY.md](docs/project-architecture/SUPERVISION_AUTHORITY_AND_EXECUTION_POLICY.md), especialmente sección 6.

**Identificadores exactos:** `SUPERVISOR_WEB` y `IMPLEMENTER_WEB`. Antes de ejecutar, validar `DESTINATARIO`, `REPOSITORIO`, `WORK ITEM`, `ACTIVITY`, autorizaciones y revisión/HEAD; documentar apertura y cierre de cada ciclo en #19. El Supervisor dirige y revisa; el Implementer solo ejecuta el trabajo encargado. El transporte de prompts no supone ejecución, lectura de respuesta ni aprobación.

La SQLite real y sus evidencias permanecen exclusivamente en el repositorio privado; el código público no incorpora datos reales, libros completos ni credenciales. Ninguna prueba no ejecutada puede declararse satisfactoria.

---

# Antecedente histórico: Biblioteca Desktop

Biblioteca Desktop es un proyecto para una aplicación local de escritorio que permitirá navegar y buscar un catálogo de documentos en Windows.

## Especificación V1

Las fuentes canónicas del alcance y del diseño son:

- [REQUIREMENTS.md](REQUIREMENTS.md) — requisitos funcionales y no funcionales V1.
- [ARCHITECTURE.md](ARCHITECTURE.md) — arquitectura técnica, fronteras y estrategia de empaquetado V1.

El código del proyecto permanece separado del corpus documental. La implementación funcional comenzará en Work Items posteriores.
