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

**Estado de gobierno:** `HUMAN_AUTHORIZED_SUPERVISOR_CONTINUATION`. **Control técnico vigente:** H5 tiene migración inicial reportada satisfactoria sobre copia, pero permanece `BLOCKED_FINAL_VALIDATION` en PR #20, HEAD `b566799691d3caef1db9c920a5e69ca325772d71`: no existe prueba Python final para ese HEAD. H6 no debe comenzar antes de aceptación de H5. H4 sigue `WORKFLOW_PERMISSION_BLOCKED`. La autorización del Human no reemplaza las validaciones ni permite repetir una operación rechazada por otro canal.


## 6. Protocolo canónico de intercambio entre actores Web — ACTIVO

**Clase documental:** NORMATIVE, vigente; **lector:** SUPERVISOR_WEB, IMPLEMENTER_WEB y agentes sucesores; **mantenedor:** SUPERVISOR_WEB; **actualización:** cambio humano o cambio verificable del contrato de transporte; **lugar canónico:** este mismo archivo (no crear documentos duplicados).

**Fuente exclusivamente de consulta:** contrato existente en el repositorio de referencia de transporte, revisión `e22a83a174e54c2b24fbd3aeffd9be17eb847672` de 2026-10-17; se revisaron el contrato `ACTUATION_REQUEST` (§33), `WORKFLOW_PLAN` (§6/§14/§18/§20) y los validadores y renderizadores de los dos roles. **Prohibición absoluta respecto del repositorio de referencia:** solo lectura para estudio, nunca escribir, comentar, crear tickets, modificar archivos/ramas, disparar workflows, configurar su servicio ni enviarle mensajes o solicitudes de trabajo. Esta incorporación se efectúa **exclusivamente en `cmiloarevalo-hash/indice`**.

### 6.1 Identidades y traspasos de vocabulario cerrado

Los identificadores **exactos** son `SUPERVISOR_WEB` y `IMPLEMENTER_WEB`; no abreviar como `IMPLEMENTER` en los sobres de transporte. Direcciones permitidas:

| Autor del payload persistido | Destinatario exacto | `handoffKind` | Resultado de trabajo esperado |
| --- | --- | --- | --- |
| `SUPERVISOR_WEB` | `IMPLEMENTER_WEB` | `IMPLEMENTER_WORK_ITEM` | Ejecutar únicamente la actividad abierta |
| `IMPLEMENTER_WEB` | `SUPERVISOR_WEB` | `SUPERVISOR_REVIEW` | Verificar entrega en PR y SHA exacto |

Un mensaje operativo debe empezar por `DESTINATARIO: IMPLEMENTER_WEB` o `DESTINATARIO: SUPERVISOR_WEB`, según corresponda, y **no** por un encabezado genérico. Si llega al destinatario incorrecto: `DESTINATARIO_INCORRECTO`, no ejecutar, no reinterpretar ni reenviar por inferencia.

**Sobres de salida que genera el transporte — mantener nombres literales:**

Para Implementer:
```text
DESTINATARIO: IMPLEMENTER_WEB
REPOSITORIO: cmiloarevalo-hash/indice
WORK ITEM: #19
WORK ITEM REF: https://github.com/cmiloarevalo-hash/indice/issues/19
AUTHORIZATION REF: <referencia persistente aplicable>
PAYLOAD SOURCE: <URL exacta de comentario GitHub persistido>

<texto literal de la instrucción del Supervisor, idéntico al comentario fuente>
```

Para Supervisor, ante una PR:
```text
DESTINATARIO: SUPERVISOR_WEB
REPOSITORIO: cmiloarevalo-hash/indice
WORK ITEM: #19
WORK ITEM REF: https://github.com/cmiloarevalo-hash/indice/issues/19
PR: #20
PR REF: https://github.com/cmiloarevalo-hash/indice/pull/20
EXPECTED REVISION: <SHA Git exacto de 40 caracteres>
AUTHORIZATION REF: <referencia persistente aplicable>
PAYLOAD SOURCE: <URL exacta de comentario GitHub persistido>

<texto literal de la entrega del Implementer, idéntico al comentario fuente>

PROJECT_ALIGNMENT_CHECK
Verify only from GitHub/Workflow:
- active Work Item + parent Milestone still trace to the product objective;
- no material process/infrastructure drift has accumulated;
- no material scope creep is present.
Persist exactly one result in GitHub/Workflow:
ALIGNED | HOLD | HUMAN_REVIEW_REQUIRED
```

El contenido entre `<...>` es marcador explicativo, **nunca** valor válido de una solicitud real. El Supervisor y el Implementer redactan el **payload**; el sobre lo construye el transporte desde estado factual. El texto del payload debe coincidir **byte por byte** con el cuerpo del comentario en GitHub; no inventar URL `#issuecomment-`, ni un comentario que no existe. El traspaso requiere que el comentario pertenezca al buzón/ruta preconfigurado para el autor y el receptor, sin presuponer que ese buzón esté activo.

### 6.2 Estructura interna de solicitud consumible por el transporte

`ACTUATION_REQUEST` debe contener **solamente** estas claves y tipos; nunca autoriza trabajo por texto libre:

```json
{
  "kind": "ACTUATION_REQUEST",
  "workItem": {"repository": "cmiloarevalo-hash/indice", "number": 19},
  "authorization": "https://github.com/cmiloarevalo-hash/indice/issues/19",
  "expectedRevision": null,
  "targetActor": "IMPLEMENTER_WEB",
  "handoffKind": "IMPLEMENTER_WORK_ITEM",
  "humanRequired": false,
  "humanAuthorization": null,
  "externalEffect": "NONE",
  "deliveryLimit": 0,
  "contextRefs": [],
  "stopConditions": ["Role, Work Item, authorization or current activity does not match GitHub"]
}
```

Ejemplo **inertemente documental** (`NONE/0`, no entrega externa). Para un `SUPERVISOR_REVIEW` deben cambiar juntos el destinatario a `SUPERVISOR_WEB`, `handoffKind` a `SUPERVISOR_REVIEW` y `expectedRevision` a un SHA exacto de 40 dígitos **que coincida con el HEAD factual de la PR**. La revisión requiere contexto factual PR; no usar `null`/NONE allí.

Solo las parejas `externalEffect: NONE` + `deliveryLimit: 0` o `externalEffect: PROMPT_DELIVERY` + `deliveryLimit: 1` son válidas. La segunda **no** autoriza un envío real por sí sola: se requieren el control de autorización humana específico y concordante que exija el mecanismo, sesión de destinatario comprobada, buzón origen factual y prueba de legitimidad. La autorización general para trabajar en Biblioteca no equivale automáticamente a un permiso técnico de Send para cualquier actor/sesión/PR. Si Send fue incierto (`UNCERTAIN_AFTER_SEND`), **STOP sin reintento**. La entrega mecánica nunca es prueba de que el destinatario ejecutó, respondió o aprobó; el transporte de referencia es *output-blind*.

### 6.3 Apertura y cierre de subactividad sin proliferar Work Items

El **único Work Item rector sigue siendo #19**, y la **PR #20** conserva el código actual sin merge. Cada nuevo tramo material se identifica como `CICLO-NNNN` dentro del mismo expediente: nunca convertir cada lote o cambio en issue nuevo. Existe **máximo una subactividad activa por Implementer**.

**Apertura por SUPERVISOR_WEB:** primero registrar de manera durable en #19 (o en comentario del buzón GitHub aplicable verificado) un `ACTIVITY_OPEN` con:
```text
ACTIVITY_OPEN
CYCLE_ID: CICLO-NNNN
TARGET_ROLE: IMPLEMENTER_WEB
REPOSITORY: cmiloarevalo-hash/indice
WORK_ITEM: #19
ACTIVITY: <identificador acotado>
AUTHORITY_REF: <URL GitHub factual>
BASE_SHA: <40-hex confirmado o N/A por causa>
OBJECTIVE:
ACCEPTANCE_CRITERIA:
SEMANTIC_SCOPE:
PATH_SCOPE:
RESOURCE_SCOPE:
VERIFICATION:
STOP_CONDITIONS:
RETURN_TO: SUPERVISOR_WEB
STATE: OPEN / AUTHORIZED
```

**Entrega por IMPLEMENTER_WEB:** persistir respuesta con `CYCLE_ID`, `ACTIVITY`, `WORK_ITEM`, `BRANCH/PR`, `BASE`, `HEAD` exacto, archivos/recursos modificados, ejecución real, pruebas/CI, límites, evidencias, bloqueos y `STATE: READY_FOR_SUPERVISOR_REVIEW` o `BLOCKED_RETURN_TO_SUPERVISOR`. Usar `SUPERVISOR_REVIEW` con `EXPECTED REVISION` exacto cuando haya PR.

**Revisión y cierre por SUPERVISOR_WEB:** verificar independientemente HEAD, diff, alcance y evidencia; publicar `PROJECT_ALIGNMENT_CHECK: ALIGNED | HOLD | HUMAN_REVIEW_REQUIRED` y una decisión `ACCEPT | REWORK | BLOCK | ESCALATE`. En caso de aceptación, la subactividad se cierra como `ACTIVITY_CLOSE: ACCEPTED`; si hay corrección, `ACTIVITY_CLOSE: REWORK_REQUIRED` seguida de nueva actividad; ante bloqueo, `ACTIVITY_CLOSE: BLOCKED` con causa, operaciones no repetibles y próxima actividad lícita. El cierre de subactividad **no** cierra #19: Supervisor abre `CICLO-(N+1)` después de cada revisión, salvo que el proyecto entero satisfaga sus criterios finales. El siguiente ciclo **no supone** un nuevo Send autorizado automáticamente.

**Contrato de actividad exigible al Implementer:** ejecutar código, pruebas, investigación y registros reales; nunca devolver otro prompt como sustituto. H5 sigue `BLOCKED_FINAL_VALIDATION`, H6 espera revisión legítima de H5; no eludir el rechazo de herramientas. El objetivo final sigue siendo 28.781 registros con investigación trazable y clasificación prudente; resultados `E/UNKNOWN` son admisibles cuando hay insuficiencia probatoria documentada.

### 6.4 Recuperación y diferencias entre protocolo y transporte real

Todo agente nuevo reconstruye primero #19, mandato canónico, comentario durable vigente, PR/HEAD exacto, estado de bloqueo y recursos permitidos; pasa el control de destinatario antes de ejecutar. Si falta una referencia factual, el payload está desactualizado, el rol no coincide o la configuración del buzón/sesión no está demostrada: `STOP / ROUTING_MISMATCH` o `BLOCKED`, sin transformación inferida ni operaciones externas.

La adopción documental de esta estructura **no instala ni conecta automáticamente el software de transporte**. Solo se puede afirmar `REQUEST_READY`, `PROMPT_READY` o `HANDOFF_TECHNICAL_SUCCESS` cuando el componente correspondiente lo haya comprobado realmente; un archivo guardado o una revisión escrita no significan que se haya enviado nada. Todo registro canónico/decisión operativa se escribe en **Biblioteca**, nunca en el repositorio de consulta.
