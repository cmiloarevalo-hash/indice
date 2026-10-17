# Arquitectura vigente H1–H3: Python + SQLite + GitHub

**Alcance:** Work Item #19, PR #20, desarrollo PUBLICO y exclusivamente sintético. No se ejecutó ninguna investigación jurídica real, migración de la SQLite aceptada, Git privado, IA editorial ni publicación.

## Arquitectura

Un único paquete Python de biblioteca estándar: tools/editorial_pipeline_prototype. La CLI es el punto de entrada único; engine.py gestiona consultas/gates heredados, rights_phase_a.py conserva una sola instancia del clasificador Phase A, licenses.py interpreta identificadores CC y registry.py gestiona las migraciones e investigación estructurada. SQLite es la ÚNICA base operativa. Ningún CSV se utiliza como motor paralelo.

GitHub público: código Python, SQL, documentación, fixtures inventadas y pruebas. GitHub privado: SQLite real y nuevos snapshots únicamente si el Human lo autoriza expresamente. GitHub no es un servidor SQLite de consultas permanentes.

La fuente real #21 permanece INALTERADA y no fue abierta: commit 642d13a0e59c4834ee04e57868ba7cef84c9c0e4, rama privada work-item-21-private-sqlite-backup-v1, NO presente en main privada. 28.781 registros y 28.781 ediciones, con clase E/UNKNOWN. El disco D: NO es recurso ni dependencia. Sin originales, la licencia de una edición concreta puede seguir desconocida. Los CSV antiguos #17/#10 y el Desktop #5 se conservan históricamente.

## Qué está implementado vs no integrado

- PR #16, HEAD d0dc5bd36012a02c3263373e57ff769fed60a6d7: Phase A, separación obra-edición y combiner A/B/C/D/E con fuentes por ambas capas. Aún sin merge. En PR #20 se conserva una sola copia ejecutable de la lógica de clasificación Phase A, y su interpretación de licencias llama al nuevo parser canónico en licenses.py.
- PR #20, base original 3c3cdeae70bab2b9a4f8295e894d701747ba10ec: prototipo Python/sqlite3, CLI, esquema diferente, tests y demostración sintética. No está en main, PR DRAFT. H1–H3 añaden registro, migraciones y correcciones NC/ND, sin crear otro motor.
- Base #21 (esquema documentado, NO inspeccionado aquí): tiene source_snapshots, files, editions, works, authors, evidence, rights_layer_status, author_file_leads, missing_required_fields, research_notes y sample_assessment. El esquema viejo #20 usa snapshots, evidence_sources, rights_decisions y columnas distintas. Por eso ejecutar init o import-catalog sobre #21 sería incorrecto. Los comandos heredados están limitados a --synthetic-fixture.
- Workflow Python de CI: ausente de la rama remota. GitHub había negado un archivo de workflow por falta del permiso OAuth workflow. No se ha reintentado ni cambiado ese permiso.

## Esquema SQL aditivo e histórico

La migración 001_rights_registry.sql se aplica únicamente a una COPIA DE TRABAJO. Tablas nuevas: lr_schema_migrations, lr_sources, lr_evidence, lr_work_identity_claims, lr_authority_claims, lr_edition_match_claims, lr_rightsholders, lr_holder_claims, lr_license_claims, lr_license_territories, lr_expiry_assessments, lr_rights_reviews y lr_review_evidence.

Estas tablas enlazan con files.record_id existente y conservan por capa los titulares, traductores, licencias y versiones, obra/edición, términos comerciales y de transformación, territorios, duración, fuentes y revisión humana. El contrato de evidencia difiere de los registros históricos, pero no se borra ni reemplaza ninguno. La migración está versionada con SHA-256, usa una transacción explícita, conserva claves foráneas, y es idempotente. Se probó rollback sintético inyectado.

La operación prevista, NO EJECUTADA con datos reales: checkout privado autorizado por SHA explícito → abrir SQLite origen mode=ro → SHA256/integrity_check/FK/filas → SQLite backup consistente a destino NUEVO y distinto → migración sobre copia → captura de fuentes/claims/revisiones → nuevo snapshot privado inmutable autorizado → restauración independiente y comparación de hashes. Conservar bytes originales y política clara LF/CRLF del manifiesto.

## Semántica de derechos H2

- CC BY / BY-SA: potencialmente comerciales con atribución/ShareAlike y fuentes aplicables al objeto exacto.
- CC BY-ND-4.0: posible compartir inalterado comercialmente pero NO autoriza adaptación por esa licencia.
- CC BY-NC-4.0 y NC-SA/NC-ND: NO autorizan uso comercial bajo esa licencia.
- Licencias versionadas, URLs oficiales, mayúsculas y guiones se normalizan en una sola rutina, sin búsqueda por subcadenas. NC/ND contradictorio => E/STOP. El derecho de adaptar es distinto del comercial.
- UNKNOWN, ausencia de evidencia independiente para obra o edición, titular no acreditado, otro mercado y edición ambigua => E. No convertir una URL genérica en autorización. Solo nueva concesión separada y legítimamente acreditada podría dar un permiso adicional.
- La CLI puede registrar fuentes y evidencias inicialmente UNVERIFIED y revisiones automáticas E, nunca una autorización A/B inventada. Las revisiones jurídicas reales se reservan para fase futura autorizada.

## Pruebas y alcance actual

Los tests sintéticos cubren CC BY/NC/ND/SA, variantes y versiones, permisos contradictorios, permisos revocados después del preflight, migración transaccional, idempotencia, rollback, FK, identidad estable, copy SQLite y preservación del origen. El ensayo que crea 28.781 identidades es INVENTADO y de la suite anterior; no toca el catálogo real.

Los tests solo validan la réplica aceptada_sintetica, NO prueban que el DDL exacto del snapshot real sea idéntico. Antes de una fase privada se debe autorizar separadamente inspección limitada de esquema y validar columnas, FKs y claves sin modificar el snapshot.

## Fases revisadas

| Hito | Aceptación y límite |
|---|---|
| H1 | Único paquete/CLI y parser compartido, importar CSV solo con flag sintético. |
| H2 | NC/ND y revocación correctas, regresiones sintéticas y no fail-open. |
| H3 | Migración SQL aditiva contra réplica de esquema #21 totalmente inventada; integridad, rollback, FK, idempotencia; sin copia real. |
| H4 | Workflow de tests Python pendiente del permiso legítimo de GitHub; no incorporado. |
| H5 | Acceso/copia/migración real y nuevo snapshot Git privado, SOLO con autorización Human futura. |
| H6 | Investigación #10/#22 de registros reales, todavía SUSPENDIDA; ediciones sin fuente siguen E. |
| H7 | Editorial, IA, KDP y Desktop V1: archivo histórico/futuro, no la operación de hoy. |

**Ninguna implementación aprobada aquí reactiva #22 ni cambia permisos o respaldos. No merge.**
