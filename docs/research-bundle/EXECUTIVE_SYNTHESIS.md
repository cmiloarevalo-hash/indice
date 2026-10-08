# Executive Synthesis — Rights + Market + International Structure

Fecha de corte: 2026-10-08.

## 1. Respuesta ejecutiva

### Cómo funcionará la clasificación de derechos

Work Item #10 Phase A implementa un modelo conservador de dos capas:

1. derechos de la obra subyacente;
2. derechos de la edición/archivo concreto.

Cada capa toma uno de cinco estados normalizados:
- OPEN_COMMERCIAL;
- COMMERCIAL_WITH_CONDITIONS;
- NONCOMMERCIAL_ONLY;
- RIGHTS_RESERVED_OR_PERMISSION_REQUIRED;
- UNCERTAIN.

Combinación:
- cualquier UNCERTAIN → E_UNCERTAIN_MANUAL_REVIEW;
- cualquier RIGHTS_RESERVED/PERMISSION → D_RIGHTS_RESERVED_OR_PERMISSION_REQUIRED;
- cualquier NONCOMMERCIAL_ONLY → C_NONCOMMERCIAL_ONLY;
- cualquier COMMERCIAL_WITH_CONDITIONS → B_COMMERCIAL_WITH_CONDITIONS;
- sólo ambas OPEN_COMMERCIAL → A_COMMERCIAL_REUSE_CONFIRMED.

A/B/C/D necesitan EvidenceURL trazable; sin evidencia se degrada a E.

El motor no decide derechos por nombre de archivo, antigüedad o presencia en Internet. Phase B debe aplicar evidencia real a los 28,781 registros; #15 no lo hace.

## 2. Competidores que importan realmente

### Directo

OBSERVED 2026-10-08:
Libra Esoterica es el comparable más cercano:
- 93,815 catalog records;
- 44,119 public full texts;
- US$9/month o US$79/year;
- research AI, semantic search, cross-book correlation y citations.

Fuente:
https://libraesoterica.com/pro
https://libraesoterica.com/about

### Workflow substitutes

Readwise, Zotero, Consensus, Elicit y Logos demuestran que usuarios pagan por workflow, research, organización y citations incluso sin que el producto posea todo el contenido.

Benchmarks OBSERVED:
- Readwise Full: US$12.99/month o US$119.88/year;
- Consensus Pro: US$20/month o US$144/year;
- Consensus Deep: US$65/month o US$540/year;
- Logos: desde ~US$12.50/month annualized;
- Zotero: US$20–120/year por storage tiers.

Fuentes:
https://readwise.io/pricing
https://consensus.app/pricing/
https://www.logos.com/pricing
https://www.zotero.org/storage

### Cultural authority substitutes

Philosophical Research Society y Embassy of the Free Mind muestran willingness-to-pay por membresía, acceso cultural y patronazgo, pero no prueban SaaS demand.

## 3. Cuánto cobran y qué implica

Banda individual observada:
- niche membership/research entry: ~US$7–13/month;
- general reading: ~US$12–29/month;
- research AI: ~US$20–65/month;
- specialist/institutional: custom o mucho más alto.

Conclusión: el pricing inicial no debería intentar maximizar ARPU antes de demostrar retention.

## 4. Tamaño de mercado plausible

### Dato observado

Instituto Cervantes Anuario 2025:
- 635,743,644 potential Spanish speakers.

Fuente consultada 2026-10-08:
https://cvc.cervantes.es/lengua/anuario/anuario_25/

### ESTIMATE top-down

HYPOTHESIS: 0.05%–0.25% del universo hispanohablante presenta interés suficientemente alto para una herramienta especializada.

Resultado:
- ~318k–1.59M personas;
- a US$79/year: ~US$25M–126M theoretical niche TAM.

Confidence: LOW-MEDIUM.

### Bottom-up

HYPOTHESIS blended ARPU: US$85/year.

Planning SOM:
- 1,000 paid users → US$85k ARR;
- 3,000 → US$255k ARR;
- 10,000 → US$850k ARR;
- 30,000 → US$2.55M ARR.

No son forecasts.

### Comparable ceiling

Scribd declara 140M+ reach y Libra Esoterica fija el anchor US$79/year. Usar una fracción diminuta de reach generalista sólo como sanity check produce ~US$1.1M–5.5M ARR, pero es LOW-CONFIDENCE y no un market share esperado.

## 5. Segmentos más atractivos

Prioridad inicial:

1. investigadores/coleccionistas esotéricos hispanohablantes;
2. académicos/posgrado en religión, historia de ideas y humanidades;
3. bibliotecas, special collections y centros de estudio;
4. practicantes avanzados que buscan fuentes;
5. digital-humanities researchers;
6. escritores/podcasters research-heavy;
7. anticuarios/rare-book collectors;
8. docentes/course creators;
9. editoriales/traductores con legacy catalogs;
10. lectores generales.

Los primeros tres maximizan pain + necesidad de organización/provenance + potencial willingness-to-pay.

## 6. Pricing inicial recomendado

HYPOTHESIS para validation, no precio aprobado:

- Free: US$0.
- Pro Individual: US$8.99/month o US$79/year.
- Research/AI: US$14.99/month o US$149/year.
- Institutional pilot: US$1,500–5,000/year, custom.

Racional:
- Pro iguala el annual anchor de Libra Esoterica;
- Research queda debajo de Consensus Pro mensual y crea espacio para inference cost;
- Institutional requiere customer discovery antes de cotizar.

## 7. Posicionamiento recomendado

Principal:

“Biblioteca de investigación esotérica en español, rights-aware y private-first: organiza tu colección local, descubre relaciones entre autores/temas y trabaja con fuentes trazables sin entregar tu biblioteca a la nube.”

Defensibilidad:
- Spanish-first;
- local/private;
- rights-aware por edición y mercado;
- author/topic/tradition graph;
- citation-first research;
- mezcla futura de biblioteca propia + metadata + A/B rights-cleared.

Alternativas:
1. sistema operativo privado para bibliotecas personales esotéricas;
2. biblioteca digital rights-cleared con research/citations.

## 8. Estructura societaria/tributaria por etapa

### Principios observados

Chile:
- residente/domiciliado tributa por renta de cualquier origen bajo art. 3 LIR;
- art. 41 G puede atribuir passive income de controlled foreign entities; SII incluye royalties.

Fuentes:
https://www.bcn.cl/leychile/navegar?idNorma=6368
https://www.sii.cl/destacados/reforma_tributaria/41g_renta017.html

US LLC:
- single-member LLC es disregarded por defecto para federal income tax;
- foreign-owned US DE puede requerir Form 5472 + pro forma 1120;
- failure-to-file penalty inicial Form 5472 = US$25,000.

Fuentes:
https://www.irs.gov/businesses/small-businesses-self-employed/single-member-limited-liability-companies
https://www.irs.gov/instructions/i5472

Estonia:
- e-Residency no cambia personal tax residence;
- una OÜ puede crear PE/dual-residence issues donde realmente se gestiona;
- distributed profits están gravados a nivel company a 22/78 desde 2025.

Fuentes:
https://learn.e-resident.gov.ee/hc/en-gb/articles/360001518878-Responsibilities-of-e-residents
https://learn.e-resident.gov.ee/hc/en-gb/articles/360002542297-Permanent-Establishment-Dual-Residence
https://emta.ee/en/business-client/taxes-and-payment/income-and-social-taxes/taxation-dividends

### Pre-revenue

Recomendación:
- no foreign entity;
- no EIN;
- no e-Residency;
- no VAT registration;
- validar WTP y product-market fit.

### Ingresos iniciales

Baseline recomendado:
Chile SpA + Merchant of Record, sujeto a LEGAL/TAX REVIEW REQUIRED.

Motivo:
- reduce cross-border reporting;
- no intenta ignorar Chile worldwide income;
- MoR delega buena parte de indirect tax/fraud/chargebacks.

Paddle OBSERVED:
5% + US$0.50 por checkout.
Fuente 2026-10-08:
https://www.paddle.com/pricing

### Expansión

No usar revenue threshold automático.

Considerar:
- US C-Corp si US venture/investors/enterprise/real operations;
- Estonia OÜ si EU operations/sustancia crean razón real;
- own merchant si savings netos superan compliance.

A US$500k gross revenue con AOV HYPOTHESIS US$79, Paddle standard cost ESTIMATE es ~US$28.2k/year antes de volume pricing. Eso justifica cotizar y comparar, no obliga a migrar.

## 9. Decisiones que podemos tomar ahora

1. Mantener derechos como gate de contenido: A/B directo; C/D/E no redistribuibles sin cambio de evidencia/licencia.
2. Construir negocio inicial alrededor de software/discovery, no ventas de PDFs.
3. Adoptar Free + Pro US$79/year como primer pricing test.
4. Reservar Research/AI como tier separado.
5. Posicionar Spanish-first + private/local + rights-aware.
6. Diseñar wishlist de D/E para medir licensing demand sin distribuir.
7. Mantener arquitectura de checkout compatible con MoR.
8. No crear foreign entity antes de una razón operacional verificable.
9. Diseñar evidence/versioning/geo/attribution desde el inicio.
10. Orientar first customer discovery a researchers/collectors, academics e institutions.

## 10. Qué debe esperar #10 Phase B

No decidir todavía:

- cuántos de 28,781 son A/B;
- tamaño real del commercial catalog;
- bundles/títulos a vender;
- revenue de contenido;
- titulares a licenciar;
- prioridad de clearance por título real;
- qué mercados pueden recibir cada edición;
- claims de “largest rights-cleared Spanish esoteric library”;
- cuánto valor incremental aporta contenido frente a software.

Phase B debe producir la distribución real A/B/C/D/E antes de comprometer monetización de corpus.

## 11. Riesgos principales

1. confundir obra libre con edición libre;
2. sobreestimar nicho a partir de audience generalista;
3. construir AI caro antes de validar WTP;
4. depender de derechos D/E para el core product;
5. formar una estructura extranjera prematura;
6. fallar compliance Form 5472 en US LLC;
7. asumir e-Residency como tax residency;
8. confundir MoR indirect-tax handling con income-tax solution.

## 12. Next gates

Antes de commercial operation:
- #10 Phase B;
- professional legal/tax review de estructura elegida;
- product/WTP validation;
- explicit Work Item para payments/sales/outreach.

Work Item #15 no ejecuta ninguno de esos actos.
