# Biblioteca — Investigación documental y clasificación de derechos

**Objetivo operativo:** investigar fuentes, licencias y derechos de los 28.781 registros bibliográficos del catálogo privado, preservando `E/UNKNOWN` cuando no existe evidencia jurídica suficiente.

**Único Work Item rector:** [#19 — Supervisión continua](https://github.com/cmiloarevalo-hash/indice/issues/19).  
**Código vigente en revisión:** [PR #20](https://github.com/cmiloarevalo-hash/indice/pull/20), sin merge.  
**Mandato y protocolo obligatorio para agentes:** [SUPERVISION_AUTHORITY_AND_EXECUTION_POLICY.md](docs/project-architecture/SUPERVISION_AUTHORITY_AND_EXECUTION_POLICY.md), especialmente sección 6.

**Identificadores exactos:** `SUPERVISOR_WEB` y `IMPLEMENTER_WEB`. Antes de ejecutar, validar `DESTINATARIO`, `REPOSITORIO`, `WORK ITEM`, `ACTIVITY`, autorizaciones y revisión/HEAD; documentar apertura y cierre de cada ciclo en #19. El Supervisor dirige y revisa; el Implementer solo ejecuta el trabajo encargado. El transporte de prompts no supone ejecución, lectura de respuesta ni aprobación.

La SQLite real y sus evidencias permanecen exclusivamente en el repositorio privado; el código público no incorpora datos reales, libros completos ni credenciales.

## Registro canónico de la fuente de investigación

**Base operativa única: SQLite `biblioteca_derechos.sqlite`.** Fuente **PRIVADA**, no incluida en `main`:

- Repositorio: `cmiloarevalo-hash/biblioteca-catalogo-privado`.
- Rama: `work-item-21-private-sqlite-backup-v1`.
- Commit inmutable del respaldo: `642d13a0e59c4834ee04e57868ba7cef84c9c0e4`.
- Ruta: `research/rights-minimum/2026-10-16-v1/biblioteca_derechos.sqlite`.
- SHA-256 documentado: `ac2594cf8c518af54102c52470a5745019e8ffbfaa16ee95699f3149c8058908`.
- Tamaño documentado: 56.938.496 bytes; 28.781 registros según manifiesto y [respaldo verificado #21](https://github.com/cmiloarevalo-hash/indice/issues/21).

**Regla para todos los agentes:** obtener la base desde la rama y commit explícitos mediante acceso autorizado; **no buscarla en `main`**. Utilizar SQLite como fuente de consultas y derechos. Los CSV previos permanecen solo para procedencia, verificación o exportación autorizada, **no como base operativa alternativa**. Distinguir el respaldo documentado de una nueva comprobación byte a byte. La SQLite almacena metadatos, no textos completos. Para actividades concretas se mantienen las puertas y bloqueos del Work Item rector #19; esta ubicación no autoriza eludirlos.
 Ninguna prueba no ejecutada puede declararse satisfactoria.

---

# Antecedente histórico: Biblioteca Desktop

Biblioteca Desktop es un proyecto para una aplicación local de escritorio que permitirá navegar y buscar un catálogo de documentos en Windows.

## Especificación V1

Las fuentes canónicas del alcance y del diseño son:

- [REQUIREMENTS.md](REQUIREMENTS.md) — requisitos funcionales y no funcionales V1.
- [ARCHITECTURE.md](ARCHITECTURE.md) — arquitectura técnica, fronteras y estrategia de empaquetado V1.

El código del proyecto permanece separado del corpus documental. La implementación funcional comenzará en Work Items posteriores.
