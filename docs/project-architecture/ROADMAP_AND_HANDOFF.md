# Plan de crecimiento, gobierno y entrega

## Fase 0 — esta única PR (#19)
Visión/arquitectura V2, diagrama, ADR, estudio de bloqueo, motores de entidad obra y edición, SQLite stdlib, importación transaccional, CLI, gates legales/editoriales/KDP, tests sintéticos, Actions read-only. NO hay producto comercial ni legal clearance. La idea #18 está reconciliada aquí, sin PR separada.

## Fase 1 — #10 continúa en paralelo
Investigación real y evidencia por archivo/traducción, derechos Chile y otros mercados, expiración y permisos de transformar. Las E pendientes no pasan a A por heurística. Trabajar en repositorio PRIVADO y en corpus read-only según su autorización distinta. #19 no cambia esos resultados.

## Fase 2 — integración privada posterior (pendiente gate Human)
Resolver la causa/permiso del bloqueo; autorización y protocolo de seguridad específicos; snapshots de metadatos PRIVATE con SHA/rows e independencia de D:, regenerar SQLite derivada en ambiente autorizado, nunca CI PUBLIC. No activar automáticamente ningún workflow_dispatch privado.

## Fase 3 — edición asistida por IA (requiere nuevo alcance)
Modelos, presupuestos y protección de datos autorizados; derechos de adaptación probados; originalidad, trazabilidad de contribuciones, revisión humano legal y editorial, control de alucinaciones y traducción. Nunca usar libros reales con API externa sin autorización.

## Fase 4 — KDP (requiere nueva aprobación Human)
Validación legal por jurisdicción y versión, obra diferenciada, prueba de PD o licencias, contribuyentes, declaración IA, preflight técnico con Kindle Previewer, cuenta KDP y decisión humana de publicar. Sin automatizar ventas/subida.

## Responsabilidades
**Human product owner** define dirección, costes, privacidad, lanzamiento, uso de proveedores. **Supervisor** autoriza/revisa Work Items y HEAD, acepta o pide REWORK. **Implementer** prepara una rama/PR sin merge y tests reproducibles. **CI** verifica esquema/función/regresión y fixtures fake; no se autoaprueba, no verifica derechos jurídicos ni criterios reales KDP.

## Handoff reproducible
Entregar SHA exacto de base y HEAD, PR sin merge, referencias workflow run y check, 17+ tests incluidos 28.781 filas **sintéticas**, demo que llega a READY_FOR_HUMAN_PUBLICATION_REVIEW (con human_publish_authorization false), SQL integrity/FK, diff paths autorizados, trazabilidad a classifier Phase A aceptado y cero filas del catálogo real.

Toda ejecución del MVP fuera de fixtures queda condicionada a autorización de accesos y privacidad.
