# H5 — Compatibilidad real SQLite: ejecución verificada y bloqueo final

**Work Item:** #19 · **PR:** #20 (DRAFT, NO MERGE)  
**Actividad:** H5_REAL_SQLITE_COMPATIBILITY · **Retorno:** SUPERVISOR_WEB  
**Estado de entrega:** \`BLOCKED_RETURN_TO_SUPERVISOR\` — **no** declarar H5 aceptado ni H6 iniciado.  
**Corte técnico:** código ejecutado hasta \`cb855885ee4eb49eae9967e91d1b27f83b0b48bf\`; dos ajustes posteriores de fixtures publicados sin nueva verificación ejecutada.

## 1. Plan y alcance

Se comprobó legítimamente el snapshot #21 en lectura, se comparó su esquema contra el paquete Python aceptado H1–H3, se ejecutó una copia local SQLite derivada y se migró **solo la copia**. No se copiaron libros ni registros al repositorio público. No se investigó ninguna licencia o bibliografía individual (H6 aún no iniciado). No se fusionó la PR ni se añadió el workflow H4 bloqueado.

**Fuente exacta** en GitHub PRIVADO: commit \`642d13a0e59c4834ee04e57868ba7cef84c9c0e4\`, rama \`work-item-21-private-sqlite-backup-v1\` (no en \`main\`). SQLite SHA-256 aceptado \`ac2594cf8c518af54102c52470a5745019e8ffbfaa16ee95699f3149c8058908\`, 56.938.496 bytes. Este dato es una referencia al backup ya documentado; no se adjunta el archivo binario ni metadata individual privada.

## 2. Resultados efectivamente ejecutados

| Verificación | Resultado comprobado |
|---|---|
| Checkout Git autenticado y commit fuente | Exacto; se confirmó commit \`642d13a...\`. |
| SHA-256 antes de inspeccionar | \`ac2594cf8c518af54102c52470a5745019e8ffbfaa16ee95699f3149c8058908\`. |
| Apertura SQLite | \`mode=ro\`, \`PRAGMA query_only=ON\` para inspección. |
| \`PRAGMA integrity_check\` del origen | \`ok\`. |
| \`PRAGMA foreign_key_check\` del origen | 0 violaciones. |
| Conteo \`files\` / \`editions\` | 28.781 / 28.781, 28.781 identidades distintas por tabla. |
| Comparación contractual | 11 tablas aceptadas presentes, columnas/PK/FK/índices inspeccionados; el nuevo namespace de migraciones no colisiona. |
| \`rights-prepare-copy\` desde HEAD público aceptado H1–H3 | PASS: copia **nueva**, \`sqlite3.Connection.backup\`, migración aditiva v1, preservación de 28.781/28.781, integrity=ok, FK=0. |
| SHA-256 del derivado tras la migración | \`83b77130ace99835de82b9e2db7542cc9fd330f860ab7d5c769e8084ff1c1867\`; tamaño 57.069.568 bytes, conservado exclusivamente local. |
| Reaplicación de migración en el derivado | \`already_applied=true\` (idempotencia PASS), checksum SQL \`379d48f90b70c355e0807814fd0113261f6ffc664266c3b9351cbeb08721bcc6\`. |
| Identidades del origen vs derivado | Huellas calculadas sobre los 28.781 \`record_id\` ordenados de ambas tablas coinciden: \`true\`. No se imprimieron identidades. |
| Rollback en **otra copia** | Fallo artificial inyectado tras cuatro sentencias; excepción controlada, conjunto de tablas original sin cambio, integridad=ok, FK=0. La copia de rollback se eliminó tras comprobarla. |
| Nuevas tablas \`lr_*\` | 13 tablas incluyendo registro de migración; **0 evidencias y 0 revisiones jurídicas** nuevas. |
| SHA-256 fuente después de inspección, backup, migración e idempotencia | Exactamente el SHA-256 aceptado, sin alteraciones del respaldo. |

**Hallazgo estructural real:** la tabla \`editions\` del backup aceptado tiene PK \`edition_id\`, mientras \`record_id\` es FK a \`files(record_id)\` y tiene unicidad. La fixture H3 anterior trataba \`editions.record_id\` como PK. El motor H3, sin embargo, migró correctamente el contrato real porque referencia \`files(record_id)\` de forma aditiva, sin recrear \`editions\`.

Se constató que 11/11 nombres de tablas, relaciones FK e índices de la nueva fixture de H5 son estructuralmente equivalentes al contrato privado. En un cotejo automatizado **anterior al último ajuste**, se detectaron **seis diferencias de valores DEFAULT** en los campos genéricos \`editions.edition_license_verified\`, \`files.actual_stat_status\`, \`rights_layer_status.commercial_royalty_free_confirmed\`, \`rights_layer_status.jurisdiction\`, \`source_snapshots.original_modified\` y \`works.file_identity_verified\`. Se añadieron los DEFAULT documentados a la fixture y un test sintético que los comprueba. **El nuevo cotejo después de corregirlos NO se ejecutó** por bloqueo técnico detallado abajo: no afirmar igualdad final probada.

## 3. Cambios públicos en la misma PR #20

Dos archivos nuevos, sin filas reales ni datos bibliográficos identificables:

1. \`tools/editorial_pipeline_prototype/fixtures/accepted_schema_h5_synthetic.sql\`: 11 tablas y columnas/PK/FK/índices/DEFAULTs generados por contrato, sin registros reales.
2. \`tools/editorial_pipeline_prototype/tests/test_h5_schema_contract.py\`: cinco regresiones estructurales H5 y una de los seis DEFAULTs; fixture de **tres entradas totalmente inventadas**. Verifican separación \`edition_id\`/FK, conservación del original, copia/migración, idempotencia, rollback, FK y E/UNKNOWN.

No se modificó la lógica del motor Python, la SQLite aceptada, la PR #16 ni ningún workflow. Los archivos del proyecto editorial permanecen solo como legado sintético.

### Pruebas realmente ejecutadas

- Bajo HEAD intermedio \`cb855885ee4eb49eae9967e91d1b27f83b0b48bf\`, en PC Windows con Python 3.13:  
  \`py -3 -m unittest discover -s tools/editorial_pipeline_prototype/tests -q\` → **44 tests PASS**, 17,960 s, sin failures ni errors.  
  \`py -3 -m tools.editorial_pipeline_prototype.cli demo\` → PASS, \`integrity_check=ok\`, FK=0, \`external_kdp_publication_performed=false\`, exclusivamente sintético.
- La primera corrida del nuevo módulo H5 reveló cuatro errores de **limpieza de archivos Windows por conexiones abiertas en los tests**, no de SQLite real; se corrigió con \`contextlib.closing\` en \`cb855885...\`; recién entonces resultaron los **44/44 PASS**.
- Después de ese PASS, los commits \`ef09e7fe74fe7220f7f52c2edb4ea9860d7a0ed9\` y \`bb93d8cbe1bc45267123d1592966656e5661ea9b\` armonizaron la fixture con seis DEFAULTs y agregaron una prueba de esos DEFAULTs. **NO se ha ejecutado suite sobre este HEAD posterior**.

## 4. Bloqueo real y regla de STOP

Al solicitar la ejecución final combinada de cotejo de estructura real vs fixture y la suite sintética tras el ajuste, el runtime **rechazó ANTES de ejecutar** la llamada a la herramienta. Texto exacto:

> Los controles de seguridad de OpenAI bloquearon esta llamada a la herramienta. Verifica nuevamente lo que estás intentando enviar.

No existe evidencia suficiente para inferir qué regla interna motivó el rechazo, ni de que se haya ejecutado alguna porción de esa última llamada. **No se reintentó la misma operación ni se cambió de herramienta, endpoint, credencial o envoltura para ejecutarla.** El bloqueo afecta la **revalidación final del HEAD de H5**, no invalida retrospectivamente los PASS ya obtenidos de lectura del origen, migración de copia, idempotencia, rollback o los 44 tests anteriores.

De acuerdo con el contrato de seguridad, se detiene la operación rechazada y se remite al Supervisor. **H5 no se presenta como formalmente aceptado**; H6 y consultas/investigaciones jurídicas de títulos reales no se iniciaron. H4 continúa pendiente del permiso GitHub \`workflow\`.

## 5. Decisión y dependencias para SUPERVISOR_WEB

1. Revisar los commits y diferencias de H5 en la **misma PR #20** (DRAFT/no merge).
2. Reconocer por separado el éxito de verificación/copia/migración real **ya comprobado**, el PASS 44/44 en \`cb855885...\` y la **revalidación final pendiente** sobre el último HEAD.
3. Decidir cómo resolver la validación pendiente **por un procedimiento legítimo sin eludir el rechazo**; no autorizar al Implementer a repetir la acción bloqueada por otro canal.
4. No ordenar H6 hasta que SUPERVISOR_WEB revise y acepte H5. El snapshot #21 permanece inmutable.

**RETURN_TO:** SUPERVISOR_WEB  
**STATE:** \`BLOCKED_RETURN_TO_SUPERVISOR\`
