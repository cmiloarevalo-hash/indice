# Implementation Roadmap — Monetización y utilización de derechos

Fecha de corte del marco: 2026-10-08.

## 1. Objetivo

Convertir la clasificación de derechos de Work Item #10 en una operación comercial futura que maximice cobertura sin redistribuir archivos restringidos.

Este roadmap es de diseño. No autoriza publicación, venta, pagos, contacto con titulares, contratación ni despliegue.

## 2. Principios de implementación

- empezar por evidencia y controles, no por ventas;
- monetizar software/discovery antes de depender de clearance masivo;
- habilitar distribución sólo para A/B y sólo por mercado;
- hacer clearance de D selectivamente;
- mantener E bloqueado;
- tratar licencias y estatus territorial como datos versionados;
- bloquear por defecto cuando evidencia o licencia expiran;
- conservar historial y trazabilidad.

## 3. Fase 0 — clasificación y evidencia

### Objetivo

Construir el sistema de verdad para derechos.

### Inputs

- esquema A/B/C/D/E de #10;
- metadata de catálogo en repositorio privado autorizado por #10;
- evidence URLs/notes;
- información de obra y edición.

### Entregables futuros

- RightsRegistry;
- RightsCase por edición;
- MarketRightsStatus;
- EvidenceRegistry;
- historial de decisiones;
- commercial_candidates;
- manual_review_queue.

### Controles

Cada registro debe separar:

- UnderlyingWorkStatus;
- EditionFileStatus;
- License;
- RightsClass;
- JurisdictionBasis;
- Confidence;
- ManualReviewRequired.

### Gate de salida

No avanzar a explotación directa hasta que:

- exista evidencia por A/B;
- D/E estén bloqueados;
- mercados estén modelados;
- no existan rutas de código que habiliten archivo por simple disponibilidad.

## 4. Fase 1 — catálogo y servicios sin redistribución

### Objetivo

Crear ingresos con el menor riesgo de copyright del corpus.

### Productos priorizados

- Biblioteca Desktop Pro;
- discovery avanzado;
- filtros, listas y colecciones;
- bibliografías;
- research-as-a-service;
- enlaces a fuentes autorizadas;
- afiliación válida cuando exista;
- gestión local de archivos que el usuario ya posee.

### Dependencia de rights clearance

Baja.

### Ventaja

Permite generar demanda y datos comerciales sobre A/B/C/D/E sin vender archivos restringidos.

### Gate de salida

- política de metadata;
- términos de producto;
- control de enlaces;
- analytics agregados;
- no subida de libros;
- separación clara entre servicio y distribución.

## 5. Fase 2 — monetización directa A/B

### Objetivo

Activar sólo activos rights-cleared.

### Funciones necesarias

- AllowedMarketStatus;
- GeoRestrictionRequired;
- CommercialActionsAllowed;
- CommercialActionsBlocked;
- attribution engine;
- license condition engine;
- expiry/hold controls;
- takedown.

### Attribution engine

Debe poder generar y almacenar:

- creador/licenciante;
- título o identificador cuando aplique;
- copyright notice;
- licencia;
- link de licencia;
- cambios realizados;
- atribuciones adicionales.

No debe “inventar” una atribución si la evidencia no contiene los datos.

### ShareAlike

Para material B con SA:

- detectar si el producto crea Adapted Material;
- registrar licencia de salida;
- bloquear licencia de salida incompatible.

### NoDerivatives

Para ND:

- permitir sólo acciones compatibles con distribución de material no adaptado;
- marcar adaptaciones como CommercialActionsBlocked salvo permiso separado.

### Gate de salida

Para cada SKU/archivo:

- A/B;
- mercado permitido;
- obligación renderizable;
- evidencia vigente;
- hash/identidad de edición;
- ausencia de hold;
- test de geo;
- test de attribution;
- rollback.

## 6. Fase 3 — licencias D seleccionadas

### Objetivo

Expandir catálogo comercial sólo donde el expected value justifique clearance.

### Pipeline

1. DemandScore.
2. ScarcityScore.
3. StrategicValueScore.
4. RightsClarityScore.
5. EstimatedRightsClearanceCost.
6. priorización.
7. research.
8. outreach bajo Work Item separado.
9. negociación.
10. contrato.
11. ingestión de derechos.
12. activación por mercado.

### Estrategia de portfolio

Priorizar:

- grupos de títulos del mismo titular;
- ediciones con derechos digitales claros;
- licencias no exclusivas;
- mercados de mayor demanda;
- contratos con reporting simple.

Evitar inicialmente:

- huérfanas complejas;
- titularidad fragmentada;
- mínimos garantizados altos sin demanda;
- exclusividad cara;
- rights bundles innecesarios.

### Gate de salida

No cambiar D a comercializable sólo porque existe negociación. Se requiere contrato ejecutado y evidencia completa.

## 7. Fase 4 — expansión internacional

### Objetivo

Abrir nuevos mercados de forma controlada.

### Requisitos

- Jurisdiction Matrix actualizada;
- reglas por mercado;
- georestricción;
- términos de venta;
- impuestos/pagos tratados separadamente de copyright;
- soporte de moneda/idioma cuando proceda;
- revisión de privacidad/consumer law en Work Items específicos.

### Regla

La incorporación/tributación no define por sí sola copyright. Cada nuevo mercado se activa sólo con rights clearance territorial.

## 8. Controles de cumplimiento

### 8.1 Evidence Registry

Campos mínimos:

- EvidenceId;
- RightsCaseId;
- SourceType;
- URL/document identifier;
- fetched/reviewed date;
- jurisdiction;
- scope;
- notes;
- confidence;
- reviewer;
- immutable hash cuando exista documento autorizado.

Jerarquía:

1. texto legal oficial;
2. licencia incluida/edición;
3. titular/editor;
4. Creative Commons;
5. registro oficial;
6. repositorio institucional con rights statement;
7. fuentes auxiliares.

### 8.2 Versionado de RightsStatus

Cada cambio produce una nueva versión:

- PreviousRightsClass;
- NewRightsClass;
- reason;
- evidence;
- timestamp;
- approver.

No se sobrescribe el pasado.

### 8.3 Attribution Engine

Entrada:

- License;
- attribution parties;
- source URI;
- changes;
- notices.

Salida:

- bloque de atribución validado;
- warning si faltan elementos;
- status BLOCKED si una obligación no puede cumplirse.

### 8.4 GeoRestriction

La capa de entrega debe consultar AllowedMarketStatus antes de servir un archivo.

Requisitos:

- deny by default;
- no confiar sólo en frontend;
- logging de decisión;
- capacidad de desactivar mercado;
- fallback a catálogo/discovery sin archivo cuando sea legalmente apropiado.

### 8.5 Takedown workflow

Estados:

- ACTIVE;
- HOLD;
- INVESTIGATING;
- TAKEDOWN;
- REINSTATED;
- PERMANENTLY_BLOCKED.

Flujo:

1. intake;
2. preservar evidencia;
3. HOLD cuando la reclamación sea material;
4. investigar;
5. retirar o reinstalar;
6. registrar resultado.

### 8.6 Audit log

Registrar:

- quién cambió rights status;
- qué evidencia cambió;
- acción comercial afectada;
- mercado;
- fecha;
- aprobación.

### 8.7 Expiry control

Un job futuro debe detectar:

- licencia vencida;
- evidencia stale;
- contrato terminado;
- territory removed.

Resultado: BLOCKED automático, no continuidad silenciosa.

## 9. Arquitectura de datos sugerida

Entidades conceptuales:

### Work

- WorkId
- title
- authors
- country of origin
- publication facts

### Edition

- EditionId
- WorkId
- translator/editor/contributors
- publication facts
- file identity

### RightsCase

- RightsCaseId
- WorkId
- EditionId
- RightsClass
- UnderlyingWorkStatus
- EditionFileStatus

### MarketRightsStatus

- RightsCaseId
- Market
- AllowedMarketStatus
- GeoRestrictionRequired
- CommercialActionsAllowed
- CommercialActionsBlocked
- LegalBasisVersion

### LicenseObligation

- attribution
- SA
- ND
- territory
- expiry
- reporting
- payment

### Evidence

- source
- authority level
- date
- notes
- hash/reference

### CommercialDecision

- scores
- cost
- expected value
- RecommendedAction
- decision version

## 10. Priorización técnica

### P0 — imprescindible antes de dinero

- rights registry;
- market status;
- evidence versioning;
- default block;
- audit.

### P1 — imprescindible antes de A/B directo

- attribution;
- geo;
- license expiry;
- takedown;
- SKU-to-rights binding.

### P2 — antes de scale

- clearance CRM;
- contract obligation engine;
- royalty reporting;
- catalog-level deal support;
- analytics de demanda.

## 11. Experimentos comerciales permitidos sólo en fases futuras autorizadas

### Software Pro

Medir:

- willingness to pay;
- activation;
- retention;
- search usage;
- collection creation.

No requiere vender libros.

### A/B bundles

Medir:

- CTR;
- conversion;
- price elasticity;
- topic demand.

Sólo con assets autorizados.

### D demand signals

Antes del clearance:

- wishlist;
- waitlist;
- interest score;
- clicks a fuente autorizada.

No adjuntar copia restringida.

## 12. Métricas de programa

Compliance:

- % A/B con evidencia completa;
- % títulos con MarketRightsStatus;
- incidents/takedowns;
- tiempo a bloqueo;
- licencias expiradas servidas: objetivo 0.

Economía:

- ARPU software;
- gross margin A/B;
- clearance cost/title;
- conversion D→license;
- payback de fixed fees;
- revenue per rights holder.

Portfolio:

- % ingresos software vs contenido;
- % catálogo monetizable directo;
- % valor económico concentrado en top rights holders;
- nº títulos agregados por negociación.

## 13. Criterios de STOP

Detener activación si:

- no se puede demostrar edición correcta;
- RightsClass E;
- D sin contrato;
- C bajo uso comercial del archivo;
- mercado REVIEW_REQUIRED;
- licencia expirada;
- attribution imposible;
- conflicto de titularidad;
- takedown material;
- contrato no cubre la acción.

## 14. Secuencia de implementación resumida

| Fase | Producto/operación | Rights dependency | Riesgo |
|---|---|---|---|
| 0 | clasificación/evidencia | alta en datos, sin explotación | bajo |
| 1 | software/catalog/discovery | baja | bajo-medio |
| 2 | monetización A/B | alta | medio |
| 3 | licencias D | muy alta | medio-alto |
| 4 | expansión internacional | alta por mercado | medio-alto |

## 15. Qué no forma parte de Work Item #11

- contactar titulares;
- firmar licencias;
- pagar;
- crear checkout;
- publicar libros;
- crear empresa;
- contratar proveedores;
- desplegar geo-blocking real;
- ejecutar marketing;
- redistribuir archivos.

## 16. Dependencias documentales

- MONETIZATION_STRATEGY.md — modelos de negocio y política por RightsClass.
- RIGHTS_TO_REVENUE_MATRIX.md — campos y scoring.
- LICENSING_PLAYBOOK.md — clearance y negociación futura.
- JURISDICTION_MATRIX.md — reglas por mercado.

## 17. Fuente de verdad

La metadata y clasificación completa siguen la arquitectura privada establecida en Work Item #10. Este repositorio público conserva solamente metodología y estrategia.

## 18. Definición de éxito futura

Biblioteca Desktop maximiza valor cuando puede:

- monetizar software sobre la mayor cobertura posible;
- monetizar directamente A/B sin ambigüedad;
- convertir D sólo cuando la economía es favorable;
- no explotar C/E de forma incompatible;
- abrir mercados de forma reversible y auditada;
- demostrar por qué cada archivo se encuentra habilitado o bloqueado.
