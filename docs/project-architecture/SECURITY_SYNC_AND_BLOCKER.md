# Análisis del bloqueo de publicación de metadatos y sincronización autorizada

**Evidencia disponible al 2026-10-16; causa raíz específica indeterminada.** Este documento solo diseña controles: **no intenta repetir operaciones bloqueadas**. Work Item #10 sigue sin ser modificado por #19.

## Hechos del incidente de #10 (comprobados en handoff previo)

1. El PC con D: accesible comprobó la presencia y tamaños de los 28.781 documentos contra el índice aceptado. El rescate local leyó metadatos incrustados en 2.000 archivos y conservó lotes reanudables en la PC (no son backup remoto).
2. Un intento de git push de una NUEVA rama de metadatos fue **bloqueado por el runtime de herramientas ANTES de ejecutar el comando**, con mensaje literal: «Los controles de seguridad de OpenAI bloquearon esta llamada a la herramienta. Verifica nuevamente lo que estás intentando enviar.» También se rechazaron intentos posteriores de inspección/consolidación y comentario de handoff.
3. Consultas GET confirmaban visibilidad PRIVATE del repo y que remoto conservaba únicamente main, HEAD 10fc576205c7259b3cf57058aaf9baa2446eff66. El commit local ac9bc187b06458cc423ba62086ac5334fb64f25e **no estaba en GitHub**. No existió recuperación GitHub del nuevo rescate.
4. El upload ANTERIOR del catálogo aceptado y del checkpoint de derechos sí se completó con éxito. No es legítimo concluir que todos los metadatos privados están prohibidos o que la causa probada es un límite de Github.

## Diferenciar hipótesis

| Hipótesis | Evidencia/estado | Acciones legítimas |
|---|---|---|
| Control del runtime de invocación de herramienta | **Observado**, rechazo antes de git HTTP | Pedir diagnóstico/política al soporte autorizado, sin repetir carga |
| GitHub permiso de token/branch protection | **No comprobado como causa**, no hubo respuesta remota al comando | Solo comprobaciones de lectura por administrador, no ensayos de payload |
| Privacidad, DLP, contenido o tamaño del envío | **Desconocido**, posible | Evaluación por Humano con clasificación del dato, no fragmentar o transformar para saltar veto |
| Incompatibilidad Git/SQLite y sincronización concurrente | Riesgo arquitectónico independiente; **no explica** el rechazo de herramientas | Versionar lotes y manifest con un escritor, revisar canales |
| GitHub prohibió usar PRIVATE para metadata | **No demostrado**, existen cargas privadas previas aceptadas | No atribuir causa al servicio sin logs oficiales |

**Diagnóstico objetivo:** el fallo observado ocurrió en el plano de seguridad de herramientas; disparador y política concreta no están disponibles. No se posee request-id de seguridad, respuesta HTTP de git ni datos suficientes para una atribución ulterior. NO se disfraza un nuevo envío en GitHub API/ZIP/LFS/Actions ni se reintenta la acción denegada desde este Work Item.

## Diseño seguro de recuperación y sync — NO ACTIVADO

1. **Identidad y consentimiento:** human autoriza por escrito categoría de nuevos metadatos, repositorio privado y un método de escritura aceptado por el runtime. Aprobación previa de reglas de clasificación y permisos. Si persiste bloqueo STOP.
2. **Mínimo conjunto:** sólo campos estructurados y sus observaciones, id SHA256(RelativePath) y rutas relativas; nunca libros, extracción de texto completo, OCR, imágenes, secretos o rutas absolutas. Datos sin publicar en repo PUBLIC ni logs de PR.
3. **Validar antes:** digest de catalog accepted, conteo y unicidad de 28.781, idempotencia, privacidad PRIVATE, límites de tamaño autorizados, evaluación de datos sensibles. Ningún cambio de formato elude la autorización.
4. **Versionar** en rama/prefijo PRIVATE nuevo, sin reescribir historial del catálogo ni los resultados activos de #10. Un solo escritor con commit normal (no force push), versión y manifest SHA-256 por salida.
5. **Validar después:** canal GitHub autorizado confirma push/commit, clon independiente autenticado en entorno diferente y sin D:, cada SHA y fila, ausencia de documentos, visibilidad privada antes/después, reportes de errores y continuidad de checkpoints.
6. **Runner privado propuesto:** solo con aprobación específica posterior; checkout de código PUBLIC desde commit revisado pinneado, GITHUB_TOKEN privado read-only para métricas del propio repo y resultados solo privados conforme a reglas autorizadas. No publicación de catálogo bloqueado via Actions. No acceder a PRs no confiables con tokens privados.

## Matriz de permisos

| Actor | Repositorio PUBLIC | Repositorio PRIVATE | Corpus D: | IA/KDP |
|---|---|---|---|---|
| Implementer #19 | Escritura en rama + PR, sin merge | Solo GET para conocer estado | Ninguno necesario | Ninguno |
| Public pull_request CI | contents: read | Ninguno | Ninguno | Ninguno |
| Ejecutable Python | Archivos parametrizados por operador | DB y datos locales SOLO si autorizados | No abre books | Ninguno |
| Futuro job PRIVATE de análisis | Código revisado pinneado | Token read-only propio repo | Ninguno | Ninguno |
| Futuro operador de respaldo | Ninguno | contents:write SOLO con consentimiento y controles | READ-ONLY | Ninguno |
| Supervisor / Human | Audita, aprueba, activa fases | Autoriza acceso legítimo | Decide alcance | Autoriza publicación futura |

Los runners de Actions son efímeros, no mantienen BD duradera; cuotas gratuitas, retención/almacenamiento de artifacts y facturación pueden cambiar. Validar documentación GitHub y los límites del plan antes de ejecutar privado; no habilitar uso pago.

Documentación de referencia:
https://docs.github.com/en/actions/concepts/security/github_token
https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
https://docs.github.com/en/security-for-organizations/security-guides/security-hardening-for-github-actions
https://docs.github.com/en/billing/concepts/product-billing/github-actions
