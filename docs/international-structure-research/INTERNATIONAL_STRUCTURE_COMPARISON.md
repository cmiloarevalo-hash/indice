# International Structure Comparison

Fecha de corte: 2026-10-08.

## Regla de lectura

- FACT = fuente oficial.
- ESTIMATE = coste/modelo no fijado por autoridad.
- HYPOTHESIS = supuesto de decisión.
- LEGAL/TAX REVIEW REQUIRED = depende de residencia, source rules, PE, CFC, treaty, sustancia o clasificación de ingresos.

No es asesoría tributaria personalizada y no autoriza formar entidades.

## Comparación ejecutiva

| Opción | Tax / residencia | Indirect tax | Reporting / riesgos | Pagos | Coste fijo aproximado |
|---|---|---|---|---|---|
| Chile persona/SpA | founder residente: renta mundial; SpA bajo régimen Chile aplicable; General 27%, Pro Pyme 12.5% 2025–27 si califica | IVA Chile; exportación sólo si requisitos/Aduanas | SII/contabilidad; CFC sólo si añade foreign entities | PSP o MoR | portal SpA sin tasa; US$600–2,400/año compliance ESTIMATE |
| US LLC foreign-owned disregarded | federal disregarded por defecto; owner/source/ECI/FDAP/treaty mandan | state sales tax + foreign VAT según ventas, salvo MoR | Form 5472 + pro forma 1120 puede aplicar; multa US$25k; Chile/CFC | alta practicidad US | Delaware LLC annual tax US$300; total US$800–3k/año ESTIMATE |
| US C-Corp | 21% federal sobre taxable income + state; shareholder Chile sigue análisis | sales tax nexus + foreign VAT | Form 1120/state; dividend/treaty/Chile/CFC | alta; investor-friendly | DE annual report US$50 + franchise tax min US$175/400 según método; US$1.5k–5k+/año ESTIMATE |
| Estonia OÜ/e-Residency | OÜ Estonia resident; e-residency no cambia personal residence; 22/78 sobre net distributed profits desde 2025 | EU VAT/OSS según ventas | annual report; management abroad puede crear foreign PE/tax | buena operación EU | application €150; OÜ €265; contact/accounting; ~€600 DIY o ~€1,300 first-year example |
| Chile + Merchant of Record | income tax Chile no desaparece | MoR asume indirect-tax stack para covered transactions | Chile reporting continúa; dependencia contractual MoR | máxima simplicidad global | Paddle 5% + US$0.50/checkout; Stripe Managed Payments +3.5% sobre processing |

## 1. Chile

FACT:
- residentes/domiciliados: renta mundial;
- CFC art. 41 G puede afectar controlled foreign passive income;
- General Semi Integrado 27%;
- Pro Pyme General 12.5% para años comerciales 2025–27 si califica;
- IVA digital 19%;
- export services exemption no es automática.

Fuentes:
- https://www.sii.cl/normativa_legislacion/leyimpuestoalarenta.pdf
- https://www.sii.cl/normativa_legislacion/circulares/2025/circu11.pdf
- https://www.sii.cl/preguntas_frecuentes/declaracion_renta/001_140_8809.htm
- https://www.sii.cl/preguntas_frecuentes/declaracion_renta/001_140_8385.htm
- https://www.sii.cl/destacados/iva_digital/
- https://www.sii.cl/destacados/exportador_servicios/

## 2. United States LLC

FACT:
- single-member domestic LLC default federal classification: disregarded unless election;
- foreign-owned U.S. disregarded entity can require Form 5472 + pro forma 1120;
- Form 5472 failure penalty starts at US$25,000;
- FDAP U.S.-source non-ECI usually 30% gross absent treaty reduction;
- ECI is taxed on a net basis under applicable rules.

Sources:
- https://www.irs.gov/businesses/small-businesses-self-employed/single-member-limited-liability-companies
- https://www.irs.gov/instructions/i5472
- https://www.irs.gov/individuals/international-taxpayers/effectively-connected-income-eci
- https://www.irs.gov/individuals/international-taxpayers/fixed-determinable-annual-or-periodical-fdap-income

FACT — Delaware:
domestic LLC annual tax US$300 and no annual report.

Source:
https://corp.delaware.gov/taxfaq/

## 3. United States C-Corp

FACT:
federal corporate tax rate is 21% of taxable income.

Source:
https://www.irs.gov/instructions/i1120

FACT — Delaware:
- non-exempt domestic corporation annual report fee: US$50;
- franchise-tax minimum US$175 using Authorized Shares Method;
- US$400 minimum using Assumed Par Value Capital Method.

Source:
https://corp.delaware.gov/paytaxes/

Best commercial rationale:
U.S. investors, employee equity, U.S. enterprise contracting or real U.S. operations.

## 4. Chile–United States treaty

FACT:
entered into force 19-12-2023, with 2024 effect dates.

Source:
https://home.treasury.gov/news/press-releases/jy2003

Treaty eligibility for transparent entities and owner structures needs **LEGAL/TAX REVIEW REQUIRED**.

## 5. Estonia OÜ/e-Residency

FACT:
- e-resident is not an Estonian tax resident merely by holding e-Residency;
- Estonian company is resident in Estonia;
- management/business abroad can trigger foreign-country taxation/PE;
- distributed profits taxed at 22/78 of net distribution from 2025.

Sources:
- https://www.emta.ee/en/private-client/foreigner-non-resident/tax-residency
- https://www.emta.ee/en/business-client/registration-business/non-residents-e-residents/tax-liabilities-companies
- https://emta.ee/en/business-client/taxes-and-payment/income-and-social-taxes/income-tax-and-basic-exemption

Estonia is not a Chile tax bypass.

## 6. Merchant of Record

OBSERVED — 2026-10-08:

Paddle:
- 5% + US$0.50 per Checkout transaction;
- no standard monthly fee;
- includes payments/billing/global indirect tax/fraud/chargebacks/buyer support.

Source:
https://www.paddle.com/pricing

Stripe Managed Payments:
- +3.5% per successful Managed Payments transaction on top of standard processing;
- indirect-tax compliance, fraud/disputes and support are included for covered transactions.

Source:
https://stripe.com/managed-payments

MoR does not remove Chile income tax/CFC/reporting.

## 7. Recommendation by stage

### Pre-revenue

HYPOTHESIS:
do not form foreign entity merely for “optimization”.

Default:
minimal Chile-compatible setup while validating product and WTP.

### Initial revenue

HYPOTHESIS:
Chile SpA + MoR is the leading baseline when founder/management are in Chile.

Why:
- avoids duplicate corporate reporting;
- respects Chile worldwide-income reality;
- MoR reduces indirect-tax/chargeback surface.

### Expansion

Trigger-based, not revenue-only:

- U.S. fundraising / enterprise / operations → model C-Corp;
- concrete U.S. payments/contracts benefit without VC → evaluate LLC carefully;
- EU substance/team/contracts → evaluate OÜ;
- MoR fee becomes material → quote custom pricing and compare self-merchant stack.

Every transition: **LEGAL/TAX REVIEW REQUIRED**.

## 8. No universal optimum

Missing founder facts can materially change the answer. DECISION_MATRIX.md lists categories needed for later professional review without collecting sensitive data under #15.
