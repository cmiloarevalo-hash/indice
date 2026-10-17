> **ACTUALIZACIÓN OPERATIVA #19 H1–H3:** El diseño vigente es Python + SQLite de metadatos aceptada #21, sin dependencia D:, sin importación recurrente CSV ni módulo editorial en producción. El diagrama abajo es HISTÓRICO, no define el flujo activo. Ver [CURRENT_ENGINE_H1_H3.md](CURRENT_ENGINE_H1_H3.md) y el README del paquete Python. El snapshot de #21 está en su rama privada y no en main. No se tocó la SQLite real en este trabajo.

---

# Arquitectura mínima v2 — componentes y contratos

Un solo paquete público Python (tools/editorial_pipeline_prototype) + sqlite3; **el mismo motor local Windows y GitHub Actions Ubuntu**. No microservicios ni segunda implementación SQLite. Biblioteca Desktop V1 sigue separada.

## Diagrama de componentes

    CORPUS D: READ-ONLY ----[solo inspección autorizada]----> GitHub PRIVATE
            |                                         catálogo/evidencias
       .NET WinForms V1                                  |
                                                         | SHA256 y export permitido
                                                         v
    GitHub PUBLIC (código, SQL, tests ficticios) ---> Python CLI
                                                         |
                                                         v
                                              SQLite local efímera
                                                         |
                                              works <> editions <> files
                                                         |
                                        rights UNDERLYING + EDITION + DERIVATIVE
                                                         + TERRITORY + OBLIGATIONS
                                                         |
                              E/insuficiente ---> STOP   |   A/B + gates OK
                                                         v
                                                Proyecto editorial
                                                SIMULADO sin contenido
                                                         |
                                              Legal humana / QA / KDP
                                                         |
                                            READY_FOR_HUMAN_PUBLICATION_REVIEW
                                                         |
                                              Human publish authorization
                                              (futura, no publica automáticamente)

## Fuentes de verdad y límites

**PUBLIC indice:** código C# histórico, Python, esquema, fixtures inventadas, tests, docs y workflow de PR read-only. Nunca rutas, títulos ni hashes de archivos reales del corpus; no DB real.

**PRIVATE biblioteca-catalogo-privado:** origen durable de identidad de catálogo y evidencias, checkpoints por commit/tag/manifest; no modificar desde #19. Sin libros binarios.

**D: original:** archivos físicos de libros, read-only, no representados como contenido cloud. El índice público NO es fuente de identidades reales.

**SQLite:** estado derivado/reconstruible desde CSV/evidencias autorizadas. GitHub Actions crea DB temporal en runner efímero, no servidor SQL persistente. Rechazar mezcla de snapshots en DB; un solo escritor por DB. En privado se puede considerar snapshot de DB derivada previa revisión, sin convertirla en autoridad.

## Modelo / contratos en schema.sql

- snapshots: checksum SHA-256 del CSV exacto, conteo y UTC.
- files: record_id = SHA256(RelativePath UTF-8 exacta); ruta relativa única, size bytes y extensión. No unir por título.
- works y editions: ID de obra explícito solo tras corroboración; edición 1:1 por archivo, separada de la obra. Sin transferir licencia entre ediciones.
- agents / agent_roles: contributor, autor, traductor, editorial y otras participaciones.
- evidence_sources: tipo UNDERLYING, EDITION, DERIVATIVE, TERRITORY; URL fuente, afirmación, fecha y corroboración.
- rights_decisions: estado calculado por el clasificador Phase A inalterado, fuente por capa, obligaciones y mercado.
- expiry_calculations: términos por capa, precisión y pendientes; todo UNKNOWN por defecto.
- editorial_projects y preflight_audit: proyecto sintético, revisiones y checklist.

**Seguridad:** import-catalog y import-rights transaccionales con rollback y claves foráneas, SHA de entrada, unicidad por ruta. PRAGMA integrity_check + foreign_key_check en verify. Ninguna función abre el corpus ni realiza llamadas de red. Evitar rutas absolutas y traversal en importador.

**Clasificador #16:** vendorizado sin cambio lógico como rights_phase_a.py y documentación de procedencia/sha; ni merge ni modificación de la rama #16.

**Concurrencia #10:** los IDs estables permiten ensamblar observaciones privadas a posteriori sin sobrescribir la investigación. Nunca escribir en el mismo archivo Git/DB desde dos tareas sin coordinación.

## Límite de pruebas

Fixtures sintéticas usan el dominio ficticio example.org para demostrar enlaces de evidencia. Una etiqueta VERIFIED en JSON es una entrada de test, **no una verdad legal** ni firma humana comprobable. Activación en corpus real requiere revisión de una cadena de procedencia y autorización independiente.
