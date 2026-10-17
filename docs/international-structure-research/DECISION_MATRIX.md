# International Structure Decision Matrix

Fecha de corte: 2026-10-08.

## 1. Método

Scores 1–5. 5 = mejor.

Pesos HYPOTHESIS:
- simplicidad 25%;
- coste fijo/variable 15%;
- acceso pagos 15%;
- escalabilidad 15%;
- riesgo fiscal/claridad 15%;
- reporting burden 10%;
- facilidad para licensing/international counterparties 5%.

Estos scores no son asesoría legal.

## 2. Matriz

| Opción | Simplicidad | Coste | Pagos | Escala | Fiscal clarity | Reporting | Licensing | Score ponderado |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Chile SpA + MoR | 5 | 4 | 5 | 4 | 4 | 4 | 3 | 4.35 |
| Chile direct/self-merchant | 3 | 4 | 3 | 4 | 4 | 3 | 3 | 3.45 |
| US LLC foreign-owned | 2 | 3 | 5 | 4 | 2 | 1 | 4 | 2.80 |
| US C-Corp | 2 | 2 | 5 | 5 | 3 | 2 | 5 | 3.10 |
| Estonia OÜ | 3 | 3 | 4 | 4 | 2 | 3 | 4 | 3.20 |

La puntuación cambia si aparecen inversionistas US, equipo EU, substantial US operations o facts personales diferentes.

## 3. Economic comparison assumptions

These illustrations compare operating/compliance overhead, not final tax liability.

OBSERVED / ESTIMATE inputs:
- Paddle standard MoR: 5% + US$0.50 per checkout.
- HYPOTHESIS average order value: US$79, implying ~5.63% standard effective MoR fee before refunds, FX and custom pricing.
- Chile SpA small-company accounting/compliance: US$600–2,400/year ESTIMATE; actual quote required.
- U.S. foreign-owned LLC recurring state/agent/tax-compliance stack: US$1,000–3,000/year ESTIMATE. Delaware official pages reviewed on 2026-10-08 conflict on the LLC annual tax (US$300 in Tax FAQ vs US$400 on the franchise-tax page), so the exact state amount must be revalidated before formation.
- U.S. C-Corp recurring state/agent/tax-compliance stack: US$1,500–5,000/year ESTIMATE; federal/state tax liability excluded.
- Estonia OÜ first-year official rough cost: approximately €600 DIY or €1,300 with accounting support; later cost depends on service providers and activity.

Illustrative non-tax overhead:

| Gross revenue | Paddle standard fee estimate | Chile SpA + MoR | US LLC + MoR | US C-Corp + MoR | Estonia OÜ + MoR |
|---:|---:|---:|---:|---:|---:|
| US$25k | ~US$1.4k | ~US$2.0k–3.8k | ~US$2.4k–4.4k | ~US$2.9k–6.4k | ~US$1.4k + €0.6k–1.3k |
| US$100k | ~US$5.6k | ~US$6.2k–8.0k | ~US$6.6k–8.6k | ~US$7.1k–10.6k | ~US$5.6k + €0.6k–1.3k |
| US$500k | ~US$28.2k | ~US$28.8k–30.6k | ~US$29.2k–31.2k | ~US$29.7k–33.2k | ~US$28.2k + €0.6k–1.3k |

These figures exclude:
- corporate income tax;
- owner-level tax;
- withholding;
- VAT/sales tax not covered by MoR;
- payroll;
- legal advice;
- foreign-tax-credit effects;
- banking/FX;
- custom high-volume MoR discounts.

They are therefore operational comparisons, not after-tax profit models.

## 4. Escenario US$25k revenue/año

HYPOTHESIS:
- AOV US$79;
- Paddle standard 5% + $0.50;
- ~US$1.4k variable MoR.

Recomendación:
- evitar foreign entity sólo por tax;
- Chile baseline + MoR;
- minimizar fixed compliance;
- validar product-market fit.

LEGAL/TAX REVIEW REQUIRED antes de escoger persona vs SpA/regimen.

## 5. Escenario US$100k/año

MoR ESTIMATE: ~US$5.6k a pricing estándar Paddle/AOV79.

Recomendación:
- Chile SpA + MoR sigue baseline;
- cotizar fees;
- formalizar accounting/rights registry;
- considerar foreign entity sólo si existe razón contractual/payment/investor real.

US LLC disregarded no es default recomendado debido a Form 5472/pro-forma 1120 + Chile complexity.

## 6. Escenario US$500k/año

MoR ESTIMATE: ~US$28.2k a pricing estándar/AOV79 antes de high-volume discount.

Recomendación:
- negociar custom MoR;
- comparar self-merchant + tax stack;
- evaluar C-Corp si US investors/enterprise/operations;
- evaluar OÜ si EU operations sustanciales;
- modelar PE/CFC/withholding/treaty con asesoría.

No crear second entity sólo por alcanzar un revenue threshold.

## 7. Recomendación por etapa

### Pre-revenue

1. no foreign company;
2. no EIN/e-Residency/VAT registrations;
3. validar WTP;
4. mantener arquitectura portable para aceptar MoR futuro.

### Initial revenue

Baseline: Chile SpA + MoR.

Razones:
- menor reporting cross-border;
- founder/management presumiblemente Chile para diseño;
- worldwide-income/CFC obliga a considerar Chile de todos modos;
- MoR resuelve buena parte de indirect tax.

### International expansion

Decision trigger, no fecha:
- US fundraising/enterprise/physical operations → model US C-Corp;
- EU substance/partners/team → model Estonia/EU vehicle;
- self-merchant economics > MoR savings net of compliance → evaluate own merchant.

## 8. Failure modes

Chile:
- escoger régimen/tax treatment incorrecto;
- asumir export VAT sin Customs qualification.

US LLC:
- perder Form 5472 deadline;
- tratar disregarded como “no tax anywhere”;
- crear USTB/ECI;
- ignorar Chile CFC.

US C-Corp:
- double-layer tax/dividend;
- state nexus;
- treaty LOB failure;
- overhead before need.

Estonia:
- confundir e-Residency con personal tax residence;
- PE/dual residence in Chile;
- CFC;
- admin/treaty assumptions.

MoR:
- creer que el MoR resuelve income tax;
- margin erosion;
- prohibited/restricted product policy;
- dependency/provider risk.

## 9. Datos que faltan para recomendación definitiva

No solicitar estos datos en #15; deben revisarse con profesional en Work Item futuro:

- residencia/domicilio fiscal real del fundador;
- ciudadanía/visas y días físicos por país;
- lugar efectivo de management;
- ownership percentages;
- entidades relacionadas;
- empleados/contractors y ubicación;
- composición de ingresos: SaaS, venta de contenido, royalties, licensing, research;
- customer mix B2C/B2B y países;
- IP ownership;
- dividend/reinvestment policy;
- funding/investor plans;
- banking/payment eligibility;
- treaty-benefit/LOB facts;
- foreign tax credits;
- expected payroll.

## 10. Decisión que puede tomarse ahora

Diseñar producto y checkout para que la entidad/MoR sea intercambiable y comenzar con el menor número de jurisdicciones.

Decisión que no debe tomarse ahora:
formar entidad extranjera por supuesta optimización sin facts y asesoría.
