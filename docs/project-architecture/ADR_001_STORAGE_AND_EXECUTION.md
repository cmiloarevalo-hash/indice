# ADR-001: SQLite derivada; Git privado snapshots; Actions efímero

**Decisión:** MVP implementado con Python 3 estándar, sqlite3, un esquema SQL y CLI única. **Estado:** solo prototipo con información INVENTADA.

## Contexto
#18 pide SQLite y GitHub Actions; #19 incluye ese alcance dentro del flujo de investigación jurídica y editorial para KDP. #17 estableció copia privada durable del índice, y #10 sigue investigando derechos; existe un bloqueo separado de publicación de nuevos metadatos.

## Arquitectura adoptada

- Python + sqlite3 versionados en repo PUBLIC: motor común Windows/local y ubuntu-latest, sin servicio SQL.
- Archivos CSV/JSON y SHA256 aceptados en Git PRIVADO, bajo permisos y controles ya aprobados: fuente de verdad del catálogo, evidencias, historial de decisiones y versiones. La base SQLite es RECONSTRUIBLE, no sustituye un snapshot sin aceptar ni verifica derechos por sí sola.
- D: almacena únicamente libros originales READ-ONLY. Ni siquiera el repo privado es backup de PDFs/EPUBs.
- Actions público, evento pull_request hacia main, permisos contents: read, checkout SHA exacto, tests sintéticos, sin secretos ni credenciales de repositorios cruzados. Runner efímero: DB se destruye al acabar. No workflow_dispatch privado en este PR.
- No acceso público a datos privados, ni logs de contenido, ni artefactos reales. Persistencia posterior requiere autorización específica, manifest, digest, read-after-write y validación de privacidad.

## Opciones rechazadas

- Postgres/SQL Server/cloud DB y servidores: complejidad y costes injustificados.
- Git de un solo archivo SQLite mutable con múltiples escritores: mala concurrencia, histórico de binarios y riesgo de conflictos. Versionar CSV/JSON como autoridad, regenerar DB y usar ramas prefijadas separadas.
- Usar ZIP/LFS/SQLite o workflow Actions para retransmitir contenido cuyo push fue denegado: **no autorizados y no permiten eludir controles**.
- GITHUB_TOKEN público para repo privado: token de Actions está limitado al repositorio del job, no concede acceso cruzado automático.

## Consecuencias y revisiones

Reproducible en Windows/Linux, atomicidad de importación, claves foráneas e integridad; no resuelve el problema de permisos para nuevos metadatos, ni implementa trabajo paralelo sobre una DB, ni valida legalidad con CI. Antes de un flujo privado, Human revisa canal permitido, secretos, privilegios mínimos, cuota/costes y retorno de recuperación. No gastar, registrar servicios ni usar presupuestos sin permiso.

Fuentes:
https://docs.python.org/3/library/sqlite3.html
https://docs.github.com/en/actions/concepts/security/github_token
https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
https://docs.github.com/en/billing/concepts/product-billing/github-actions
