# Visión V2 — plataforma editorial responsable

**Work Item #19 · 2026-10-16.** Define un producto ampliado sin invalidar Biblioteca Desktop V1.

## Misión

Convertir el catálogo documental en una plataforma de investigación de derechos y producción editorial asistida por IA para eventual publicación en Amazon KDP:

catalogar → identificar obra y edición específica → verificar derechos comerciales, transformación y territorio → seleccionar material acreditado → preparación editorial con asistencia de IA → revisión legal y QA humanas → preflight KDP → autorización humana expresa.

No autoriza reescribir títulos reales, exportar contenido, publicar libros, hacer pagos ni usar APIs externas de IA.

## Componentes y estado

| Componente | Situación | Responsabilidad |
|---|---|---|
| Biblioteca Desktop V1 (C#/.NET 10 WinForms) | T1–T8 existentes, T9/T10 pendientes | Consulta offline local, documentos read-only |
| Catálogo metadatos #17 | Snapshot privado aceptado | Identidad exacta de 28.781 registros, sin binarios |
| Derechos #10 | Investigación Phase B activa | Evidencias por obra/edición, A/B/C/D/E, licencias, expiración |
| Motor Python/sqlite3 #18 incluido en #19 | Este MVP sintético | ETL, joins, trazabilidad, editorial gates |
| Edición real asistida por IA | Futura, no autorizada | Producción humana y eventualmente integración autorizada |
| KDP y ventas | Futuro, no autorizado | Preflight manual y autorización humana |

## Postulados

1. Dominio público de una obra original nunca limpia una traducción, notas, ilustraciones, cubierta o archivo digital moderno.
2. A/B se basan en evidencia independiente de obra y edición; **adaptación** y territorios requieren verificaciones distintas. Un título disponible en Internet no significa uso comercial gratuito.
3. Los aprobadores humanos deben verificar derechos legales, fidelidad editorial, calidad, políticas KDP, costes y responsabilidades. CI prueba software, no certifica legalidad.
4. Los documentos V1 README.md, ARCHITECTURE.md y REQUIREMENTS.md se mantienen como historia válida de Biblioteca Desktop. No renombrar repositorio ni sustituir el legado.
5. Código público y pruebas sintéticas, resultados personales/bibliográficos reales en GitHub PRIVATE solo bajo autorización; originales en D: estrictamente READ-ONLY.
6. Evolucionar por fases sin servidores/microservicios/servicios de pago prematuros.

## No objetivos

No OCR ni texto de libros, no motor de IA conectado, no KDP uploader, no ingestion de catálogo real en PR o Actions públicas, no bypass de bloqueos de publicación de datos, no merges, no infraestructura de cuentas, no base SQL de producción.

Seguimiento: #5, #9, #10, #17, #18 absorbido, #19. PR #12 y #16 aceptadas pero no merged.
