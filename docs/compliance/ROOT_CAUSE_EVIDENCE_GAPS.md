# WI #23 — ROOT_CAUSE_EVIDENCE_GAPS

**Estado diagnóstico:** evidencia suficiente para caracterizar tres **fronteras de rechazo**, insuficiente para identificar el disparador de seguridad interno de OpenAI en #10 y #22.  
**Esta tarea es únicamente forense, no ensayo de permisos, no prueba de explotación, no reactivación de #22.**

## 1. Conclusión sobre SQL, con niveles de certeza

**NO EXISTE EVIDENCIA DE UN BLOQUEO ESPECÍFICO DE SQL.**

- **#22 — hecho confirmado:** la solicitud \`mcp__Remote_Desktop_Commander__write_file\` incluía el **texto de un script Python** que importaba \`sqlite3\`, abría la base con \`mode=ro\` y contenía \`SELECT\`. No se pidió ejecutar el script; se rechazó **escribirlo**. El texto SQL pudo estar presente como contexto de evaluación, pero no se ha probado relación causal.
- **#10 — evidencia incompleta:** el rechazo registrado fue una operación para enviar metadatos con Git al repositorio privado antes de comenzar el comando. No está preservado en el informe el sobre íntegro de esa solicitud: el campo «contenía SQL» es **UNKNOWN**.
- **#19 — error de GitHub identificado:** faltaba el permiso OAuth \`workflow\` para crear un YAML en \`.github/workflows/\`. Los archivos de la rama incluían un prototipo de Python/SQLite, pero la condición explícita del rechazo fue **el permiso del workflow**. No adjudicar ese rechazo a SQL.
- **#21 — evidencia contraria a un veto universal:** se construyó SQLite usando Python, se ejecutaron comprobaciones SQL y se publicó una base real de 56.938.496 bytes mediante Git normal con restauración independiente exitosa. Es un antecedente **positivo**, no garantía de futuras autorizaciones.

\`sqlite3\` **es una biblioteca**, \`SELECT\` **es texto SQL**, \`write_file\` **es una operación de escritura de archivo**, \`git push\` **es una acción de publicación remota**. Son dimensiones distintas. La coexistencia de estas cadenas en una solicitud no explica por sí sola un rechazo.

## 2. Hipótesis técnicas — no confundir con resultados

| Hipótesis alternativa | Datos a favor observados | Datos en contra o que reducen alcance | ¿Veredicto causal? |
|---|---|---|---|
| **H1. Reglas/riesgo propios de la acción \`write_file\` o su contexto**. | #22 fue detenida antes de que el agente recibiera el archivo; el nombre de la acción es comprobable. | Hubo escrituras de scripts locales y ejecución Python exitosas en #21; no prueba veto general de \`write_file\`. El paso exacto de decisión interna no está documentado. | **UNKNOWN**. |
| **H2. Clasificación del contenido/destino o de operaciones sobre metadatos privados**. | #10 y #22 se relacionaban con operaciones sobre datos bibliográficos privados, y fueron bloqueadas por el runtime. | #21 publicó metadatos y SQLite privados legítimamente; no hay clasificación DLP ni regla concreta en el mensaje. Que el proyecto trate copyright no implica automáticamente una infracción. | **UNKNOWN**. |
| **H3. Sensibilidad específica a texto SQL/\`sqlite3\` dentro del código solicitado**. | #22 llevaba explícitamente \`sqlite3\` y \`SELECT\` como texto. | No se ejecutó SQL cuando falló; #21 y #19 ejecutaron Python/SQLite localmente. #10 no documenta SQL en su llamada fallida; el mensaje no cita SQL. | **NO DEMOSTRADA**. |
| **H4. Rechazo de proveedor por permisos OAuth GitHub**. | #19 tiene mensaje remoto inequívoco: \`workflow\` scope ausente. | #10 se detuvo antes del transporte GitHub; #22 ni siquiera intentaba GitHub. | **DEMOSTRADA PARA #19 ÚNICAMENTE**. |
| **H5. Otro contexto de permisos, consentimiento, configuración del app, política o implementación no pública**. | Mensajes de runtime #10/#22 son genéricos y no identifican una regla. | No existen logs de decisión, ID de control ni respuesta administrativa revisables. | **UNKNOWN**. |

**No es un objetivo de este proyecto inferir reglas ocultas por variaciones sucesivas de payload.** Tal experimentación no está autorizada y no sería prueba confiable de cumplimiento.

## 3. Cadena de evidencia que falta

| Elemento | #10 | #19 | #22 | Procedencia permitida |
|---|---|---|---|---|
| Tool/acción exacta | Tool específico del comando denegado: **UNKNOWN**; se conoce \`git push\` | Acción \`git push\` GitHub; wrapper exacto UNKNOWN | \`mcp__Remote_Desktop_Commander__write_file\` | Handoff, registro del agente/proveedor si fue guardado legítimamente |
| Argumentos completos pasados al sistema de controles | **UNKNOWN** | Diferencia pública del commit y ruta YAML conocidas; request envelope UNKNOWN | Tipo y estructura de script conocidos por transcripción, no evaluación interna | Copia sanitizada **aprobada por Human**; nunca publicar datos privados |
| Request/correlation ID del rechazo | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** | Soporte OpenAI / GitHub / administrador |
| Timestamp exacto con zona | **UNKNOWN** | **UNKNOWN** | **UNKNOWN** | Logs de sesión auditables |
| Punto de corte | Pre-ejecución del comando (reportado) | GitHub remoto OAuth \`workflow\` (observado) | Pre-creación de archivo (observado) | Reportes preservados |
| Nombre de regla o control disparado | **UNKNOWN** | Error proveedor explícito \`workflow\`; ID de política de OpenAI no corresponde | **UNKNOWN** | Solo soporte/admin autorizado puede aclarar, si la información es divulgable |
| SQL realmente ejecutado durante rechazo | **NO DEMOSTRADO**, UNKNOWN | **No hay evidencia** | **NO** | Traza de ejecución independiente, no repetir acciones |
| Efectos posteriores y publicación | Nueva rama de rescate no publicada (reportado) | Workflow no publicado; PR #20 sin workflow | Script no creado; 0/75 | Repositorios y handoffs ya existentes |
| Comparador positivo | Checkpoints privados previos sí publicaron | 17 archivos de PR #20 sí publicados; no el workflow | #21 SQLite+Git PASS | Handoffs anteriores |

**Limitación del historial de Desktop Commander:** es circular/acotado, puede omitir outputs largos y no contiene necesariamente rechazos que nunca entraron al agente. La inspección realizada fue solo de metadatos filtrados del log ya existente, sin buscar títulos privados o reabrir bases. Un evento ausente del log **no prueba** que el runtime no lo haya rechazado.

## 4. Preguntas acotadas para Soporte OpenAI / administrador / GitHub

**Para OpenAI Support / equipo responsable del conector:**

1. ¿Pueden verificar con el historial del usuario, fecha aproximada 2026-10-16 y nombre del conector **Remote Desktop Commander**, si el bloqueo de \`write_file\` en #22 fue una restricción de **tipo de acción**, de **clasificación de datos/destino**, de **permisos del app/workspace** u otra clase divulgable? No solicitamos reglas ocultas ni umbrales técnicos.
2. ¿Dispone el usuario de un registro de auditoría o request-ID visible que permita documentar la causa y etapa de rechazo de #10 y #22 sin reenviar los payloads? ¿Cómo obtenerlo por vía oficial?
3. ¿Cuál es el **procedimiento expresamente permitido**, con aprobación humana y del administrador cuando aplique, para redactar scripts locales y procesar metadata bibliográfica privada de propiedad autorizada, **sin transferir libros**?
4. ¿Qué alcance real tienen los permisos de escritura del conector sobre archivos privados locales, y qué controles adicionales debe aprobar el usuario? ¿Puede una acción ser denegada aun con permiso de Windows/GitHub legítimo?
5. ¿Qué datos mínimos pueden suministrarse a Support para el diagnóstico sin publicar rutas/títulos privados? ¿Existe un canal seguro de envío de trazas si se requieren?
6. ¿Qué documentación pública vigente conviene citar para separar reglas de uso, controles del conector, controles de la cuenta/workspace y permisos del proveedor?

**Para GitHub / administrador GitHub — incidente independiente #19:**

7. ¿Qué autorización OAuth, control de organización y aprobación explícita serían necesarios para crear un archivo de workflow en esa rama? **No pedir ni compartir tokens**. La PR seguirá suspendida mientras la tarea esté en pausa.
8. ¿Existe una traza de auditoría del rechazo del workflow y su hora exacta que permita completar el expediente de #19 sin volver a intentar el push?

**Para el Human / Supervisor:**

9. ¿Aprueban elevar a soporte un **resumen sanitizado**? No se transmitirá el reporte ni se adjuntarán payloads/logs por iniciativa del Implementer.
10. Tras una explicación formal, ¿qué **operaciones concretas** se autorizan y cuáles quedan suspendidas? Una autorización genérica para usar SQL no sustituye controles del conector.

## 5. Texto opcional para consulta a soporte — borrador NO ENVIADO

> Asunto: Consulta sobre rechazos de controles de herramientas en operación autorizada de metadatos
>
> El 16 de octubre de 2026, un intento de usar el conector Remote Desktop Commander para crear localmente un script Python de consulta **read-only** a una base SQLite bibliográfica privada fue rechazado **antes de crear el archivo** con el mensaje «Los controles de seguridad de OpenAI bloquearon esta llamada a la herramienta. Verifica nuevamente lo que estás intentando enviar.» Un incidente anterior rechazó, también antes de ejecución, una solicitud de envío de metadatos a un repositorio GitHub privado. No se transfirieron libros, ni se ejecutó la selección del último incidente. Otras operaciones autorizadas de Python+SQLite sí funcionaron.
>
> Solicitamos aclarar, en lo que sea divulgable, si la restricción corresponde al permiso del conector, al tipo de acción, a la clasificación del contenido o a requisitos adicionales de autorización, así como la vía para revisar registros de auditoría. No pedimos desactivar ni evitar protecciones. Podemos facilitar datos de sesión sanitizados por un canal aprobado.
>
> Este borrador no contiene títulos privados, rutas reales de documentos ni credenciales. **Requiere consentimiento explícito del Human para su envío**.

## 6. Recomendación de arquitectura autorizada — solo propuesta, no implementación

Separar **siete fronteras** y dejar registro del consentimiento/permiso en cada una:

| Puerta | Comprobación previa | Acción si no hay autorización o existe denegación |
|---|---|---|
| 0 — Política y tareas | Alcance humano vigente; #22 sigue SUSPENDIDO. Reglas públicas y documentación oficiales a revisar en tarea separada. | No procesar registros; solo informe público, genérico y sanitizado. |
| 1 — Activos y titularidad | Clasificación por origen: datos públicos, títulos/rutas de catálogo privado, evidencias jurídicas, contenidos de libros, credenciales. | Aplicar mínimo privilegio y no distribuir. |
| 2 — Identidad/permisos de herramienta | Rol aprobado del app, alcance de lectura/escritura, host y ubicación autorizados. | STOP si la herramienta prohíbe la acción; no sustituirla por Python, Shell, REST, Actions u otro canal. |
| 3 — Ejecución controlada | Solo tras aprobación expresa: especificación revisada; código y pruebas con **datos inventados** y autorización del método; lectura real limitada. | No repetir acción denegada ni hacer pruebas exploratorias de su filtro. |
| 4 — Evidencia y clasificación | Distinguir autoridad bibliográfica, obra, traducción, edición, permiso comercial, territorio y precisión; falta de prueba => UNKNOWN/E. | No elevar evidencia bibliográfica a licencia. |
| 5 — Almacenamiento | Entregables reales solo privados y mediante canal **normal autorizado**; snapshots inmutables, manifest canónico LF + bytes Git y checkout cuando corresponda. | STOP antes de publicar si falla permiso/protección. |
| 6 — Auditoría/recuperación | Verificar SHA-256 de blobs, SQLite integrity/FK, número de filas, privacidad, HEAD sin merge; guardar **solo rastros sanitizados** en issues públicos. | No afirmar PASS sin restauración verificada. |

**Roles:** Human decide fines y consentimiento; Supervisor valida alcance y metodología; Implementer ejecuta solamente actos permitidos; Support/admin responde dudas de permisos/seguridad; asesoría jurídica humana evalúa derechos antes de comercializar. Un permiso GitHub no equivale a permiso de OpenAI; un consentimiento humano no anula una denegación de herramienta; un resultado de una IA no es concesión de copyright.

**Árbol de decisión para #22:** (a) mientras está SUSPENDIDO → no ejecutar; (b) si Human no aprueba pedir soporte → conservar incidente y STOP; (c) si Support/admin no aclara compatibilidad o persiste veto → STOP; (d) si las reglas públicas, consentimiento, titularidad, permisos y alcance quedan documentados y **Human autoriza por escrito una nueva actividad**, diseñar por separado plan de prueba con datos sintéticos **que no repita el objetivo bloqueado**, sin asumir éxito; (e) ejecutar solo lo autorizado, deteniendo todo ante un nuevo rechazo. Ninguna de estas decisiones ha sido tomada en este Work Item.

## 7. Alcance pendiente fuera de esta actividad forense

El cuerpo original de [#23](https://github.com/cmiloarevalo-hash/indice/issues/23) enumera políticas públicas y ayuda de OpenAI que requieren una revisión **documental independiente y fechada**. El encargo más reciente acota este paso a **registros e informes existentes**; por ese motivo **NO** se ha navegado ahora a esas políticas ni se afirma haber confirmado su versión o cláusulas vigentes. Los enlaces de consulta están en el cuerpo del Work Item #23 y se revisarán solo si Human/Supervisor lo solicita dentro de alcance permitido.

**Conclusión final:** *rechazo de acción* ≠ *rechazo de SQL*. Causa interna #10/#22 **UNKNOWN**. Permiso GitHub \`workflow\` faltante en #19 **CONFIRMADO**. El precedente #21 refuta un veto técnico universal a SQLite. No hubo nuevos ensayos de acciones rechazadas ni operaciones sobre datos privados.
