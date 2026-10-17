# Biblioteca — Mandato canónico de supervisión y ejecución

**Estado:** VIGENTE — autorización general del Human, 2026-10-17  
**Autoridad:** HUMAN (objetivo y propiedad) → SUPERVISOR_WEB (decisión técnica, continuidad, revisión) → IMPLEMENTER (ejecución).  
**Proyecto:** investigación documental y clasificación de derechos de obras, traducciones y ediciones.  
**Referencias:** [#19](https://github.com/cmiloarevalo-hash/indice/issues/19), [PR #20](https://github.com/cmiloarevalo-hash/indice/pull/20), [#10](https://github.com/cmiloarevalo-hash/indice/issues/10), [#21](https://github.com/cmiloarevalo-hash/indice/issues/21), [#22](https://github.com/cmiloarevalo-hash/indice/issues/22).

## 1. Autorización expresa del Human y regla de continuidad

El Human autoriza **todas las actividades técnicas y de investigación documental necesarias para llevar a término el análisis sistemático de derechos y licencias de los registros bibliográficos del proyecto**, dentro de la finalidad vigente descrita aquí, y **delega en SUPERVISOR_WEB** las decisiones operativas de continuidad entre hitos. No se requiere solicitar una nueva aprobación humana rutinaria al pasar de H4 a H5, H6 o a los lotes sucesivos de investigación de #10/#22.

SUPERVISOR_WEB debe verificar entregables, pruebas y HEAD antes de continuar; puede aceptar, devolver a corrección, bloquear o asignar la siguiente actividad al IMPLEMENTER sin preguntar nuevamente al Human. Si hay una desviación material de objetivo, divulgación de contenido privado, riesgo de seguridad, gasto o permiso externo no disponible, debe detener **solo la operación afectada**, documentar el impedimento y buscar una vía legítima. Esta autorización **no elude restricciones de GitHub, de herramientas, de sitios terceros ni de ley**.

La autoridad delegada incluye aprobar el desarrollo, lectura de esquema y consultas de la SQLite privada, pruebas sobre copias de trabajo, investigación documental por lotes, almacenamiento de evidencias y snapshots versionados en GitHub privado, revisión de PR y, una vez satisfechos criterios de calidad y seguridad, decisiones de integración del código apropiadas al alcance. No implica fusionar ramas automáticamente.

## 2. Alcance y arquitectura obligatoria

- **Objetivo:** identificar y distinguir obra original, autoría, traducción, edición/manifestación y archivo; localizar fuentes válidas; analizar derechos patrimoniales y morales relevantes, licencias y titulares, uso comercial, adaptación, territorios y vigencias; guardar evidencias, incertidumbre y resultados consultables.
- **Motor único:** Python + SQLite. Código, SQL, documentación y fixtures exclusivamente sintéticos en el repositorio público `cmiloarevalo-hash/indice`. SQLite real, metadatos, evidencias de investigación y snapshots únicamente en `cmiloarevalo-hash/biblioteca-catalogo-privado`.
- **Punto de partida privado inmutable:** commit `642d13a0e59c4834ee04e57868ba7cef84c9c0e4`, rama `work-item-21-private-sqlite-backup-v1`, ruta `research/rights-minimum/2026-10-16-v1/biblioteca_derechos.sqlite`, SHA-256 `ac2594cf8c518af54102c52470a5745019e8ffbfaa16ee95699f3149c8058908`, 28.781 registros. No presumir que está en `main`. Nunca modificar este respaldo de origen.
- **Interpretación:** la SQLite contiene *metadatos*, no los libros completos. No presumir que contiene una licencia para cada archivo, que acceso/ISBN prueba derechos, ni que una obra de dominio público libera traducciones/ediciones actuales. Registros no verificables deben permanecer `E/UNKNOWN`, con causa y pendientes; nunca inventar permisos.
- Se conservan CSV históricos para procedencia, no como motor paralelo. El disco D: no está disponible. No iniciar KDP, creación editorial con IA, publicación de libros, OCR masivo o exposición de textos completos. La lectura legítima de documentación pertinente para investigación sí pertenece al estudio autorizado.

## 3. Secuencia de ejecución bajo responsabilidad de SUPERVISOR_WEB

**H0–H3: ACEPTADOS dentro del alcance sintético.** PR pública #20, HEAD aceptado `9046669e0e72444a269162c4d73e017660691d5f`; 39/39 pruebas Python y demo ficticia confirmadas en revisión anterior. No repetir sin defecto nuevo reproducible.

**H4 — CI Python:** autorizado como objetivo, pero la publicación de un archivo workflow está técnicamente bloqueada hasta que GitHub conceda permiso legítimo `workflow` a la credencial pertinente. No intentar otra ruta para eludir un rechazo. Mantener bloqueo localizado: H5 no depende necesariamente de que H4 se haya resuelto; ejecutar pruebas locales verificables y documentar la ausencia de CI Python remota mientras dure el impedimento.

**H5 — Compatibilidad real SQLite (AUTORIZADO):** IMPLEMENTER trabaja desde el commit privado exacto por acceso autorizado, comprueba SHA y `PRAGMA integrity_check`/FK y examina el DDL real en lectura; coteja esquema, PK/FK y migraciones con el motor. Solo ejecutar migraciones sobre **una copia nueva de trabajo**, con backup/rollback, idempotencia y comprobación de que el original no cambió. Nunca commitear SQLite ni datos privados al repositorio público. Entregar HEAD, diff, tablas/campos observados relevantes, comandos, resultados, incidencias y SHA inicial/final del original, sin revelar datos personales o bibliográficos sensibles en el público.

**H6 / #10 / #22 — Estudio de licencias y derechos (AUTORIZADO):** tras aceptación de H5, investigar sistemáticamente el catálogo completo, usando lotes controlados, consultas al motor único y fuentes legalmente accesibles; registrar procedencia/fecha/URL/autoridad, objeto jurídico exacto (obra/edición/traducción/archivo), jurisdicción, concesión de derechos comerciales y de adaptación, condiciones, conflictos y grado de verificación. Distinguir evaluación automática preliminar de revisión jurídica; toda duda o carencia conserva `E/UNKNOWN`. Priorizar trazabilidad y comprobación, no forzar veredictos. Respetar límites de APIs, licencias y fuentes; no descargar ni publicar contenidos completos. Registrar evidencia en SQLite privada mediante snapshots por hitos aprobados.

**Criterio de cierre del objetivo:** cobertura contable del 100 % de los 28.781 registros **con estado y trazabilidad individual de investigación**, sin afirmar que el 100 % tendrá licencia resuelta. Distinguir `verificado`, `pendiente por fuente no accesible`, `evidencia insuficiente` y demás estados razonados; sumar pendientes y documentar el alcance de cualquier conclusión. Los juicios de permiso comercial requieren evidencia suficiente sobre obra **y** edición concreta, no inferencias de título o metadatos. Entregar informe reproducible y SQLite/snapshots privados íntegros, con pruebas y resumen agregado no sensible.

## 4. Contrato de delegación y aceptación

Cada asignación del Supervisor al Implementer debe incluir `TARGET_ROLE: IMPLEMENTER`, `REPOSITORY`, `WORK_ITEM`, `ACTIVITY`, `RETURN_TO: SUPERVISOR_WEB`, autorización, objetivo, archivos, procedimiento, pruebas, restricciones y entregables. El Implementer entrega **código/datos autorizados y resultados comprobables**, no un prompt sustituto. Estados de retorno: `READY_FOR_SUPERVISOR_REVIEW` o `BLOCKED_RETURN_TO_SUPERVISOR`.

El Supervisor verifica **HEAD exacto**, diff, pruebas, integridad y seguridad, y responde `ACCEPTED`, `REWORK_REQUIRED` o `BLOCKED`. La continuidad al siguiente hito es responsabilidad del Supervisor sin consultas rutinarias al Human. No se declara éxito ante una prueba no ejecutada. No crear PR/issues duplicados cuando se puede continuar los existentes. Respetar privacidad, derechos de terceros y controles de herramientas; bloqueos no autorizan bypass.

## 5. Precedencia documental

Esta decisión del Human (2026-10-17) **reemplaza únicamente las pausas anteriores por falta de autorización humana** de H5, H6, #10 y #22. Conserva aceptación H0–H3, inmutabilidad #21, separación público/privado, obligación de pruebas y restricciones técnicas. Los comentarios e historiales anteriores permanecen trazables, pero las frases «WAITING_HUMAN_DECISION», «H5/H6 NO AUTORIZADOS» o «#22 SUSPENDIDO» dejan de ser el estado operativo vigente para estas actividades. Permisos técnicos pendientes (por ejemplo, scope `workflow`) siguen pendientes de concesión real.

**Estado de gobierno:** `HUMAN_AUTHORIZED_SUPERVISOR_CONTINUATION`; **siguiente trabajo implementable:** H5, sujeto a acceso legítimo al repositorio privado; H4 sigue `WORKFLOW_PERMISSION_BLOCKED` si el permiso aún no existe. No confundir autorización con ejecución completada.
