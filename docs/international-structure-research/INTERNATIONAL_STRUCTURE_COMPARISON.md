# International Structure Comparison

Fecha de corte: 2026-10-08.

## Regla de lectura

FACT = fuente oficial.
ESTIMATE = coste operativo no fijado por autoridad.
HYPOTHESIS = supuesto para comparar escenarios.
LEGAL/TAX REVIEW REQUIRED = depende de residencia, sustancia, source rules, PE, CFC, tratado o clasificación de ingreso.

Este documento no es asesoría tributaria personalizada y no autoriza constituir ninguna entidad.

## Comparación ejecutiva

| Opción | Residencia entidad / dueño | Corporate tax | Distribuciones / withholding | IVA/VAT/sales tax | Reporting y riesgos | Pagos | Rough fixed cost |
|---|---|---|---|---|---|---|---|
| Chile persona/SpA | entidad chilena; dueño según hechos personales | régimen chileno aplicable; General Semi Integrado 27%; Pro Pyme puede tener tasas distintas/transitorias | impuestos finales dependen del propietario y régimen | IVA Chile; exportación de servicios sólo si cumple requisitos | renta mundial para residentes; CFC si controla entidad extranjera | acceso local + MoR/PSP | SpA portal $0; firma notarial si aplica; accounting US$600–2,400/año ESTIMATE |
| US LLC foreign-owned disregarded | LLC US, federalmente disregarded por defecto si single-member; dueño puede seguir residente Chile | no asumir 0%; tax depende de USTB/ECI/source/treaty | U.S.-source FDAP puede sufrir 30% o treaty; owner Chile sigue análisis Chile | US sales tax nexus + foreign VAT según ventas; MoR puede delegar indirect tax | Form 5472 + pro forma 1120 si corresponde; CFC/Chile/PE | muy práctico para US processors | Delaware $300/año state tax + agent/tax prep; US$1k–3k/año ESTIMATE |
| US C-Corp | corporation US; owner puede seguir Chile resident | federal 21% + state where applicable | dividend withholding subject domestic/treaty/LOB | sales tax nexus + foreign VAT | 1120, state filings, Chile owner/treaty/CFC analysis | muy práctico; investor-friendly | DE report $50 + franchise min $175/$400 + agent/tax prep; US$1.5k–5k/año ESTIMATE |
| Estonia OÜ/e-Residency | OÜ Estonian resident; e-Residency does NOT change personal tax residence | 22/78 on net distributed profits from 2025 | generally company-level dividend tax; recipient/home-country tax can apply | Estonian/EU VAT plus cross-border rules | PE/dual residence where managed; annual report/accounting | EU-friendly | official ~€600 first-year DIY / ~€1,300 with accounting |
| Chile seller + Merchant of Record | no extra foreign entity required | Chile entity/person tax remains | MoR payout is business income; not tax escape | MoR handles covered indirect tax as seller/MoR | Chile income/reporting still applies | easiest global checkout | Paddle 5%+$0.50/checkout; Stripe Managed Payments +3.5% plus processing |

## Fuentes oficiales principales

Chile:
- LIR art. 3 worldwide income: https://www.bcn.cl/leychile/navegar?idNorma=6368
- SII art. 41 G CFC: https://www.sii.cl/destacados/reforma_tributaria/41g_renta017.html
- Registro Empresas: https://www.registrodeempresasysociedades.cl/
- SII regímenes: https://www.sii.cl/destacados/modernizacion/tipos_regimenes_mt.html

Estados Unidos:
- IRS LLC: https://www.irs.gov/businesses/small-businesses-self-employed/single-member-limited-liability-companies
- Form 5472: https://www.irs.gov/instructions/i5472
- Form 1120: https://www.irs.gov/instructions/i1120
- ECI: https://www.irs.gov/individuals/international-taxpayers/effectively-connected-income-eci
- FDAP: https://www.irs.gov/individuals/international-taxpayers/fixed-determinable-annual-or-periodical-fdap-income
- Chile-US treaty: https://home.treasury.gov/news/press-releases/jy2003

Estonia:
- https://www.e-resident.gov.ee/taxes-in-estonia/
- https://learn.e-resident.gov.ee/hc/en-gb/articles/360002542297-Permanent-Establishment-Dual-Residence
- https://emta.ee/en/business-client/taxes-and-payment/income-and-social-taxes/taxation-dividends

MoR:
- https://www.paddle.com/pricing
- https://stripe.com/managed-payments

## Conclusión de estructura

Pre-revenue: no crear entidad extranjera sólo por “optimización”.

Ingresos iniciales: Chile/SpA + MoR es el baseline operativo más simple si el fundador efectivamente reside/gestiona desde Chile. LEGAL/TAX REVIEW REQUIRED antes de ejecución.

Expansión: considerar US C-Corp por inversionistas/enterprise/operación US, no sólo por impuestos. Estonia OÜ sólo si existe razón operativa EU y sustancia/management compatible. Una US LLC disregarded puede servir pagos/contratos, pero añade reporting y no elimina obligaciones chilenas.

No existe una estructura universalmente óptima sin datos personales/fiscales y de operación.
