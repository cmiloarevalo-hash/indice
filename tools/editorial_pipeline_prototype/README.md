# Prototipo editorial V2 — un solo motor Python + SQLite

**Solo datos sintéticos, Work Item #19 (integra #18).** Python 3.11+ estándar y SQLite. No APIs de IA/KDP/GitHub, ni corpus real. Nombres y rutas del fixture son inventados. Los enlaces example.org ilustran columnas de evidencia pero nunca justifican derechos reales.

## Ejecución idéntica en Windows, Linux y Actions

Desde la raíz del repo:

    python -m tools.editorial_pipeline_prototype.cli demo
    python -m unittest discover -s tools/editorial_pipeline_prototype/tests -v

    python -m tools.editorial_pipeline_prototype.cli --db local-demo.sqlite init
    python -m tools.editorial_pipeline_prototype.cli --db local-demo.sqlite import-catalog --csv tools/editorial_pipeline_prototype/fixtures/synthetic_catalog.csv
    python -m tools.editorial_pipeline_prototype.cli --db local-demo.sqlite import-rights --json tools/editorial_pipeline_prototype/fixtures/synthetic_rights.json
    python -m tools.editorial_pipeline_prototype.cli --db local-demo.sqlite summary
    python -m tools.editorial_pipeline_prototype.cli --db local-demo.sqlite verify
    python -m tools.editorial_pipeline_prototype.cli --db local-demo.sqlite rights-status --relative-path "fixture/fiction/Invented River Fables.pdf"
    python -m tools.editorial_pipeline_prototype.cli --db local-demo.sqlite export-report --out local-synthetic-report.json

Windows: use py -3 en vez de python si es necesario. La demo utiliza una carpeta temporal que se destruye automáticamente. Evite guardar SQLite en un directorio público/versionado.

## Flujo

init crea schema.sql y migrations v1. import-catalog valida cabeceras, unicidad de ruta exacta, tamaño, SHA256 e idempotencia. import-rights conserva evidencia por cada obra/edición/derivación/territorio y aplica el clasificador Phase A. verify ejecuta PRAGMA integrity_check y foreign_key_check.

start-project solo admite A/B y verificaciones separadas de obra, edición, permisos para adaptación, obligaciones y país autorizado. simulate-editorial registra estados sin generar texto ni solicitar IA. review-gate requiere el flag explícito --synthetic-attestation para el simulacro, nunca representa una aprobación legal real. preflight comprueba QA/legal/KDP, diferenciación PD e información IA, termina en READY_FOR_HUMAN_PUBLICATION_REVIEW. human_publish_authorization es una fase distinta y no se publica nunca, ni siquiera en el simulacro.

Todos los registros se enlazan por record_id = SHA256(RelativePath UTF-8 EXACTA), no por coincidencias de título. Las traducciones/ediciones concretas y derechos de obras subyacentes son entidades distintas. Importación de snapshots y evidencia es transaccional, con rollback y foreign keys; 28.781 filas sintéticas se prueban sin tocar datos privados.

## Dependencia Phase A conservada

rights_phase_a.py es copia de tools/rights-classification/rights_classifier.py en PR #16, HEAD d0dc5bd36012a02c3263373e57ff769fed60a6d7, sin cambios lógicos. PR #16 permanece abierta; no se hizo merge. Esta versión se fija dentro del mismo paquete Python, sin segundo motor #18.

## Garantías y límites

Las banderas de aprobación humana son **mocks**, no firmas válidas ni certificado de derechos. El motor no contiene una herramienta de recuperación/escritura de datos privados. La futura ejecución privada requiere decisión específica y vía de sincronización autorizada, sin eludir bloqueos de seguridad de herramientas.

Ver docs/project-architecture/: PROJECT_VISION.md, SYSTEM_DESIGN.md, RIGHTS_KDP_POLICY.md, ADR_001_STORAGE_AND_EXECUTION.md, SECURITY_SYNC_AND_BLOCKER.md y ROADMAP_AND_HANDOFF.md.
