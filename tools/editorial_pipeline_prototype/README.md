# Motor único Python + SQLite — H1/H2/H3 (solo desarrollo sintético)

**Estado:** componente PÚBLICO de PR #20, todavía SIN MERGE; el estudio real de derechos permanece suspendido.
Este paquete usa `sqlite3` de Python y contiene la única implementación activa del combinador
de capas Phase A (`rights_phase_a.py`). `licenses.py` concentra la normalización de
licencias CC para todas las rutas de importación/eligibilidad. `registry.py` y
`migrations/001_rights_registry.sql` definen el registro jurídico *aditivo* para una
copia de trabajo del esquema #21. No hay motor CSV secundario ni dependencia D:.

El snapshot real aceptado **NO está en main privado**: permanece bajo el commit
`642d13a0e59c4834ee04e57868ba7cef84c9c0e4` en la rama
`work-item-21-private-sqlite-backup-v1`. **No se abrió ni migró en esta PR.**
La plantilla `fixtures/accepted_schema_synthetic.sql` aproxima los nombres
de tablas/identidades documentados; NO es el DDL real ni demuestra compatibilidad
binaria hasta revisión expresamente autorizada.

## Comandos de investigación y estado de SQLite (no ejecutados con datos reales)

- `rights-verify --expected-rows N`: comprobación de esquema/ficheros/ediciones e integridad en modo lectura.
- `rights-search --phrase ...`: consulta local parametrizada; nunca en CI público con datos privados.
- `rights-registry-summary`: conteos relacionales de evidencias, licencias y revisiones.
- `rights-prepare-copy --source-sqlite ... --source-sha256 ... --out ... --expected-rows N`:
  en una futura fase autorizada, abre el origen **READ-ONLY**, valida digest,
  hace backup SQLite consistente a una ruta nueva NO existente y migra únicamente
  la copia, preservando archivo de origen. Ningún script descarga/busca por sí
  mismo un repositorio privado o solicita credenciales.

Los comandos originales `init`, `import-catalog`, `import-rights`,
`start-project`, `simulate-editorial`, `review-gate`,
`preflight`, `authorize-publication-simulation` ahora requieren
`--synthetic-fixture`: se conservan para regresiones y demostración,
**nunca para regenerar la SQLite aceptada desde CSV**. El comando `demo`
crea datos totalmente inventados y no publica.

## Semántica NC/ND y alcance

- CC BY/SA: uso comercial potencial condicionado a atribución/ShareAlike.
- CC BY-ND: compartir inalterado puede ser comercial, **NO adaptaciones** por esa licencia.
- CC BY-NC: la licencia NO permite uso comercial.
- `CC-BY-ND-4.0`, `CC-BY-NC-4.0`, URLs oficiales y variantes sintácticas reconocidas
  sin coincidencias por subcadena. Declaraciones contradictorias => E/STOP.
- Fuentes, licenciante, territorio, obra, edición y permisos adicionales no se
  deducen de la etiqueta. Concesiones excepcionales requieren registro aparte
  y corroboración humana, NO una bandera que silencie NC/ND.
- Migración aditiva con `lr_` sin alterar `files`, `editions`, `works` ni
  las tablas jurídicas anteriores; evidencia sin revisar permanece UNVERIFIED,
  revisiones automáticas únicamente E/UNKNOWN.

## Validaciones de seguridad de desarrollo

```text
py -3 -m unittest discover -s tools/editorial_pipeline_prototype/tests -v
py -3 -m tools.editorial_pipeline_prototype.cli demo
```

Utilizar `python` en entornos que lo tengan en PATH. Los archivos de test son
ficticios. La CI nueva de Python no se incorporó: requiere permiso legítimo
de GitHub `workflow`; no se intentó reutilizar otra vía.

---

## Descripción histórica del prototipo editorial (solo simulación)

# Prototipo editorial V2 — un solo motor Python + SQLite

**Solo datos sintéticos, Work Item #19 (integra #18).** Python 3.11+ estándar y SQLite. No APIs de IA/KDP/GitHub, ni corpus real. Nombres y rutas del fixture son inventados. Los enlaces example.org ilustran columnas de evidencia pero nunca justifican derechos reales.

## Ejecución idéntica en Windows, Linux y Actions

Desde la raíz del repo:

    python -m tools.editorial_pipeline_prototype.cli demo
    python -m unittest discover -s tools/editorial_pipeline_prototype/tests -v

    python -m tools.editorial_pipeline_prototype.cli --db local-demo.sqlite --synthetic-fixture init
    python -m tools.editorial_pipeline_prototype.cli --db local-demo.sqlite --synthetic-fixture import-catalog --csv tools/editorial_pipeline_prototype/fixtures/synthetic_catalog.csv
    python -m tools.editorial_pipeline_prototype.cli --db local-demo.sqlite --synthetic-fixture import-rights --json tools/editorial_pipeline_prototype/fixtures/synthetic_rights.json
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
