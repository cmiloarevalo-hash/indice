# VAT, Sales Tax and Merchant of Record

Fecha de corte: 2026-10-08.

## 1. Merchant of Record

Un MoR se convierte contractualmente en seller/merchant para las transacciones cubiertas y asume componentes de payments e indirect-tax compliance definidos por el proveedor.

No elimina income tax, CFC, PE ni reporting de la empresa que recibe payouts.

## 2. Paddle

OBSERVED:
- 5% + US$0.50 por Checkout transaction;
- no setup/monthly fees estándar;
- incluye payments, billing, global tax/regulatory compliance, fraud, chargebacks y buyer support;
- custom pricing disponible para high volume.

Fuente:
https://www.paddle.com/pricing

## 3. Stripe Managed Payments

OBSERVED:
- añade 3.5% por successful Managed Payments transaction sobre standard Stripe processing fees;
- incluye global indirect tax, fraud, dispute responses y transaction-level support;
- no setup fee ni monthly minimum estándar.

Fuente:
https://stripe.com/managed-payments

Como el processing fee depende del país/método, no usar 3.5% como coste all-in.

## 4. MoR vs own merchant

| Factor | MoR | Own merchant |
|---|---|---|
| VAT/sales tax | delega cálculo/collection/remittance para covered sales | responsabilidad propia/Tax SaaS |
| chargebacks/fraud | mayor delegación | propia |
| invoices | proveedor gestiona parte importante | propia |
| checkout control | menor | mayor |
| variable fee | mayor | potencialmente menor a escala |
| tax registrations | muchas indirectas delegadas | pueden multiplicarse |
| income tax | sigue siendo propio | propio |
| flexibility | menor | mayor |

## 5. UE — B2C services y OSS

FACT. Non-Union OSS permite a un taxable person no establecido en UE registrar en un Estado miembro y declarar allí B2C services cuyo lugar de imposición sea UE, en vez de múltiples registros.

Fuentes:
https://vat-one-stop-shop.ec.europa.eu/one-stop-shop/register-oss_en
https://europa.eu/youreurope/business/finance-and-tax/vat/one-stop-shop/index_en.htm

Para electronic services B2C, la regla de place-of-supply suele llevar VAT al lugar del consumidor; clasificación concreta debe revisarse.

LEGAL/TAX REVIEW REQUIRED.

## 6. ViDA

FACT. ViDA fue adoptado 11-03-2025 y entró en vigor 14-04-2025, con rollout hasta 2035.

Timeline Comisión:
- 01-01-2027: clarificaciones OSS/IOSS;
- 01-07-2028: elementos de Single VAT Registration y platform rules relevantes;
- 01-07-2030: cross-border B2B Digital Reporting Requirements;
- 01-01-2035: alignment de domestic digital reporting.

Fuente:
https://taxation-customs.ec.europa.eu/taxation/vat/vat-digital-age-vida_en

## 7. Ventas a Chile desde extranjero

FACT. SII Digital VAT aplica a no residentes que prestan servicios remotos gravados a beneficiarios en Chile; ejemplos incluyen software, plataformas y contenido digital.

Fuente:
https://www.sii.cl/destacados/iva_digital/

MoR puede encargarse del indirect tax si la venta está dentro de su cobertura contractual, pero no reemplaza Chile income-tax/CFC analysis de supplier/owner.

## 8. Exportación desde Chile

FACT. SII art. 12 E N°16: ciertos servicios a no residentes están exentos cuando son calificados exportación por Aduanas y utilizados en el extranjero según requisitos.

Fuente:
https://www.sii.cl/destacados/exportador_servicios/

No asumir exención para todo SaaS/research.

## 9. Economic fee illustration

HYPOTHESIS: average order value US$79 (annual Pro anchor).

Paddle standard effective fee:
5% + 0.50/79 = ~5.63%.

| Gross revenue | Approx Paddle cost at 5.63% |
|---:|---:|
| US$25,000 | ~US$1,408 |
| US$100,000 | ~US$5,633 |
| US$500,000 | ~US$28,165 |

ESTIMATE, excluye refunds, special/invoice fees, FX y custom volume pricing.

Implicación:
- a US$25k–100k, el MoR fee puede ser un coste racional a cambio de compliance;
- a US$500k, ~US$28k/año justifica cotizar custom pricing y comparar self-merchant + tax stack.

## 10. Recomendación

Pre-revenue/initial revenue: MoR reduce surface de indirect tax.

Scale: re-evaluar cuando savings potencial de self-merchant exceda tax-engineering/accounting/support/compliance incremental.
