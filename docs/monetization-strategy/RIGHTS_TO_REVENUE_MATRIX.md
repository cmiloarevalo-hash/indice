# Rights-to-Revenue Matrix

Fecha de corte del marco: 2026-10-08.

## 1. Propósito

Esta matriz convierte la clasificación jurídica de Work Item #10 en decisiones comerciales trazables. No sustituye la evidencia jurídica: consume RightsClass y los campos de evidencia como input y produce una recomendación de negocio.

La decisión se realiza por obra/edición/archivo y por mercado. El mismo título puede tener acciones distintas en Chile, Estados Unidos, Unión Europea y México.

## 2. Esquema mínimo por libro/edición

Cada registro de decisión comercial debe incluir, como mínimo:

| Campo | Tipo sugerido | Regla |
|---|---|---|
| RightsClass | enum A/B/C/D/E | viene del contrato de #10 |
| UnderlyingWorkStatus | texto controlado | estado de la obra subyacente |
| EditionFileStatus | texto controlado | estado de traducción/edición/archivo |
| AllowedMarkets | lista | mercados donde la acción concreta está habilitada |
| AllowedMarketStatus | mapa mercado→estado | ALLOWED, ALLOWED_WITH_CONDITIONS, BLOCKED, REVIEW_REQUIRED |
| GeoRestrictionRequired | boolean | true si no todos los mercados tienen el mismo estado |
| CommercialActionsAllowed | lista | acciones específicas permitidas |
| CommercialActionsBlocked | lista | acciones específicas prohibidas/no demostradas |
| RequiredAttribution | texto/estructura | crédito, link, aviso, cambios y otros elementos |
| DerivativeRestrictions | texto controlado | NONE, SHARE_ALIKE, NO_DERIVATIVES, OTHER |
| RequiredLicense | texto | licencia/permiso necesario antes de activar |
| EvidenceURLs | lista | fuentes que soportan la decisión |
| EvidenceVersionDate | fecha | última validación |
| LicenseExpiryDate | fecha/null | si aplica |
| EstimatedRightsClearanceCost | rango monetario | hipótesis comercial, no hecho legal |
| DemandScore | 0–100 | señal de demanda normalizada |
| ScarcityScore | 0–100 | escasez de oferta autorizada comparable |
| StrategicValueScore | 0–100 | valor de marca, colección, cross-sell, completitud |
| RightsClarityScore | 0–100 | claridad de titular, cadena y derechos solicitados |
| OperationalComplexityScore | 0–100 | complejidad de atribución, reporting, geo, formatos |
| ExpectedAnnualGrossMargin | rango | hipótesis comercial |
| RecommendedAction | enum/texto | acción prioritaria |
| DecisionOwner | identificador de rol | responsable de aprobar activación |
| DecisionTimestamp | fecha/hora | auditoría |

## 3. Matriz base por RightsClass

| Clase | Venta/descarga | Membresía con archivo | Bundle | POD | Software/discovery | Affiliate/link autorizado | Clearance |
|---|---:|---:|---:|---:|---:|---:|---:|
| A | posible | posible | posible | sólo si derechos/formato lo permiten | sí | sí | no, salvo derecho adicional |
| B | posible con condiciones | posible con condiciones | posible con condiciones | sólo si licencia lo permite | sí | sí | sólo si falta derecho adicional |
| C | bloqueado | bloqueado | bloqueado | bloqueado | sí | sí, bajo términos válidos | pedir licencia comercial |
| D | bloqueado | bloqueado | bloqueado | bloqueado | sí, sin redistribuir archivo | sí, si el enlace es lícito | prioritario si EV positivo |
| E | bloqueado | bloqueado | bloqueado | bloqueado | sólo metadata segura | sólo después de validar destino | investigar antes de negociar |

“Posible” nunca significa automático. Debe existir AllowedMarketStatus compatible y evidencia de la edición concreta.

## 4. Obligaciones operativas para B

### CC BY

CommercialActionsAllowed puede incluir distribución y adaptación comercial.

RequiredAttribution debe capturar, cuando se haya suministrado:

- creador/licenciante;
- copyright notice;
- referencia o URI del material;
- enlace a la licencia;
- indicación de modificaciones;
- otros créditos requeridos por la licencia concreta.

Fuente: https://creativecommons.org/licenses/by/4.0/

### CC BY-SA

Añadir a las obligaciones de BY:

- detectar si el producto contiene Adapted Material;
- aplicar la misma licencia o una compatible según la licencia;
- impedir una cadena de distribución que añada restricciones incompatibles.

Fuente: https://creativecommons.org/licenses/by-sa/4.0/

### CC BY-ND

Puede permitir redistribución comercial del material no adaptado, pero no distribución del material adaptado. El sistema debe bloquear acciones que produzcan una adaptación distribuida si no existe permiso separado.

Fuente: https://creativecommons.org/licenses/by-nd/4.0/

### Licencias NC

CC BY-NC, BY-NC-SA y BY-NC-ND no deben alimentar productos que exploten comercialmente el material licenciado sin permiso separado.

Fuentes:
- https://creativecommons.org/licenses/by-nc/4.0/
- https://creativecommons.org/licenses/by-nc-sa/4.0/
- https://creativecommons.org/licenses/by-nc-nd/4.0/

### Otras condiciones

Para licencias editoriales o contratos directos, RequiredAttribution y CommercialActionsAllowed deben derivarse del texto contractual concreto. No se deben proyectar reglas de Creative Commons sobre una licencia que no sea CC.

## 5. AllowedMarketStatus

Valores operativos:

- ALLOWED: evidencia suficiente para la acción concreta en ese mercado.
- ALLOWED_WITH_CONDITIONS: permitido si se cumplen obligaciones registradas.
- BLOCKED: prohibido por licencia, copyright vigente sin licencia, takedown, expiración o condición incumplida.
- REVIEW_REQUIRED: falta evidencia suficiente o la regla territorial es compleja.

Ejemplo conceptual:

| Mercado | Status | Motivo |
|---|---|---|
| Chile | ALLOWED | obra + edición reutilizables |
| EE. UU. | REVIEW_REQUIRED | obra extranjera antigua: revisar URAA/formalidades |
| UE | ALLOWED_WITH_CONDITIONS | licencia comercial con atribución |
| México | BLOCKED | plazo/titular vigente o licencia no cubre México |

Si existe al menos un BLOCKED o REVIEW_REQUIRED mientras otro mercado está habilitado, GeoRestrictionRequired debe ser true para distribución digital directa.

## 6. CommercialActionsAllowed / Blocked

Vocabulario sugerido:

Acciones directas:

- SELL_DOWNLOAD
- MEMBER_ACCESS_FILE
- THEMATIC_BUNDLE
- PRINT_ON_DEMAND
- DISTRIBUTE_UNMODIFIED
- DISTRIBUTE_ADAPTED
- COMMERCIAL_TDM_OR_AI
- CREATE_NEW_EDITION

Acciones indirectas:

- CATALOG_DISCOVERY
- SOFTWARE_LOCAL_COLLECTION
- BIBLIOGRAPHY
- RESEARCH_SERVICE
- LINK_AUTHORIZED_SOURCE
- AFFILIATE_AUTHORIZED_SOURCE
- DEMAND_MEASUREMENT
- RIGHTS_OUTREACH_CANDIDATE

Cada acción debe evaluarse separadamente. Permiso para distribución no implica automáticamente permiso para adaptación, POD, IA o territorios adicionales.

## 7. Sistema de priorización de clearance

### 7.1 Scores comerciales

DemandScore, ScarcityScore y StrategicValueScore se calculan de 0 a 100.

Sugerencia inicial:

- DemandScore: 40% de la prioridad comercial.
- ScarcityScore: 20%.
- StrategicValueScore: 20%.
- RightsClarityScore: 20%.

Luego se aplica una penalización por coste y complejidad.

No son pesos jurídicos. Son parámetros comerciales sujetos a recalibración.

### 7.2 Clearance Priority Score

Modelo inicial:

BaseValueScore =
0.40 × DemandScore
+ 0.20 × ScarcityScore
+ 0.20 × StrategicValueScore
+ 0.20 × RightsClarityScore.

PenaltyScore =
CostPenalty + OperationalComplexityPenalty + GeoFragmentationPenalty.

ClearancePriorityScore = BaseValueScore − PenaltyScore.

El sistema no debe transformar una puntuación alta en permiso. Sólo decide qué caso investigar o negociar primero.

### 7.3 Economic gate

Antes de pagar/licenciar:

ExpectedContribution =
ExpectedRevenue
− variable delivery/payment cost
− royalty
− amortized fixed license/guarantee
− expected rights administration cost
− expected support cost.

Una licencia entra a negociación avanzada sólo si:

- ExpectedContribution es positiva bajo escenario base;
- el escenario conservador no produce una pérdida material no aceptada;
- el coste de clearance está dentro del presupuesto;
- la cadena de titularidad parece verificable;
- el mercado objetivo es suficientemente grande.

## 8. Reglas concretas de decisión

1. Licenciar primero demanda alta + derechos claros + coste razonable.
2. No invertir inicialmente en demanda baja + clearance complejo.
3. Agrupar títulos de un mismo titular cuando una negociación de catálogo reduzca coste por título.
4. Priorizar licencias no exclusivas salvo que la exclusividad tenga valor económico demostrable.
5. Comprar sólo los territorios y formatos que generan valor esperado; evitar derechos globales innecesarios.
6. Evitar mínimos garantizados altos antes de tener demanda observada.
7. Para C, preguntar por licencia comercial sólo cuando la señal de demanda justifique el coste.
8. Para E, invertir primero en evidencia, no en negociación.
9. Para A/B, priorizar activos que reduzcan costes de atribución y geo-control sin sacrificar valor.
10. Recalcular RecommendedAction cuando cambien demanda, evidencia o condiciones de licencia.

## 9. RecommendedAction

Valores sugeridos:

- DIRECT_MONETIZE_A
- DIRECT_MONETIZE_B_WITH_CONTROLS
- SOFTWARE_DISCOVERY_ONLY
- LINK_OR_AFFILIATE_ONLY
- REQUEST_COMMERCIAL_RELICENSE
- RIGHTS_CLEARANCE_PRIORITY_HIGH
- RIGHTS_CLEARANCE_PRIORITY_MEDIUM
- RIGHTS_CLEARANCE_DEFER
- MANUAL_RIGHTS_RESEARCH
- GEO_RESTRICT_AND_MONETIZE_ELSEWHERE
- BLOCK_TAKEDOWN
- BLOCK_EXPIRED_EVIDENCE

## 10. Ejemplos sintéticos

Estos ejemplos no representan libros reales.

### Ejemplo A

RightsClass: A.
AllowedMarkets: Chile, UE.
EE. UU.: REVIEW_REQUIRED por regla histórica pendiente.
México: ALLOWED.
RecommendedAction: GEO_RESTRICT_AND_MONETIZE_ELSEWHERE hasta completar EE. UU.

### Ejemplo B-SA

RightsClass: B.
Licencia: CC BY-SA 4.0.
Acción: bundle sin adaptación.
RequiredAttribution: sí.
ShareAlike: sólo relevante si existe material adaptado.
RecommendedAction: DIRECT_MONETIZE_B_WITH_CONTROLS.

### Ejemplo C

RightsClass: C.
Licencia: CC BY-NC 4.0.
CommercialActionsBlocked: SELL_DOWNLOAD, MEMBER_ACCESS_FILE, POD.
CommercialActionsAllowed: CATALOG_DISCOVERY, SOFTWARE_LOCAL_COLLECTION.
RecommendedAction: SOFTWARE_DISCOVERY_ONLY y, si demanda alta, REQUEST_COMMERCIAL_RELICENSE.

### Ejemplo D

RightsClass: D.
DemandScore 90, ScarcityScore 80, RightsClarityScore 85.
Titular/editor identificable.
RecommendedAction: RIGHTS_CLEARANCE_PRIORITY_HIGH.

### Ejemplo E

RightsClass: E.
Traducción moderna no identificada con claridad.
RecommendedAction: MANUAL_RIGHTS_RESEARCH.
Cualquier monetización directa: bloqueada.

## 11. Integridad y auditoría

Toda decisión debe poder reconstruirse a partir de:

- snapshot de derechos;
- evidencia;
- fecha;
- mercado;
- acción;
- licencia;
- versión de reglas;
- cambio de estado;
- actor que aprobó el cambio.

Los cambios nunca deben sobreescribir silenciosamente un estado anterior. Debe conservarse historial.

## 12. Fuentes de reglas de licencia y territorialidad

- WIPO/Berna: https://www.wipo.int/en/web/treaties/ip/berne/summary_berne
- Creative Commons: https://creativecommons.org/licenses/
- Chile: https://www.bcn.cl/leychile/navegar?idNorma=28933
- U.S. Copyright Office: https://www.copyright.gov/circs/circ15a.pdf
- UE: https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32006L0116
- México: https://www.diputados.gob.mx/LeyesBiblio/pdf/LFDA.pdf
