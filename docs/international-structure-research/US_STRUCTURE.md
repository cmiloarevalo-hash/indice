# United States Structure — Foreign-Owned LLC vs C-Corp

Fecha de corte: 2026-10-08.

## 1. Single-member LLC

FACT. Una domestic LLC con un solo miembro se trata por defecto como disregarded entity para federal income tax, salvo elección de tratamiento corporativo.

Fuente:
https://www.irs.gov/businesses/small-businesses-self-employed/single-member-limited-liability-companies

No significa “tax free”.

### Foreign-owned disregarded entity reporting

FACT. Una foreign-owned U.S. disregarded entity sujeta a section 6038A debe presentar Form 5472 adjunto a un pro forma Form 1120 cuando existen las condiciones/reportable transactions.

Fuente:
https://www.irs.gov/instructions/i5472

FACT. La multa inicial por failure to file Form 5472 es US$25,000; después de notice y 90 días pueden acumularse multas adicionales de US$25,000 por cada periodo de 30 días.

Fuente:
https://www.irs.gov/instructions/i5472

Este es un failure mode material para una LLC “simple”.

### Delaware state baseline

FACT. Delaware LLCs pagan un annual tax de US$300 y no presentan annual report.

Fuente:
https://corp.delaware.gov/taxfaq/

ESTIMATE total recurring con registered agent + bookkeeping/tax prep: US$1,000–3,000/año.

## 2. ECI, FDAP y foreign-source

### ECI

FACT. IRS: si una foreign person está engaged in U.S. trade or business, income efectivamente conectado puede estar sujeto a US tax sobre base neta con deductions.

Fuente:
https://www.irs.gov/individuals/international-taxpayers/effectively-connected-income-eci

### FDAP

FACT. U.S.-source FDAP no ECI —incluyendo típicamente interés, dividendos, rents, royalties— está generalmente sujeto a 30% gross withholding o una tasa menor por treaty.

Fuente:
https://www.irs.gov/individuals/international-taxpayers/fixed-determinable-annual-or-periodical-fdap-income

### Foreign-source

La residencia de la LLC no decide por sí sola el source de todos los ingresos. Services, royalties, software/content characterization, lugar de actividades y treaty pueden cambiar el resultado.

LEGAL/TAX REVIEW REQUIRED antes de afirmar “no U.S. tax”.

## 3. C-Corp

FACT. Form 1120 instructions: federal corporate income tax = 21% de taxable income.

Fuente:
https://www.irs.gov/instructions/i1120

Delaware:
- non-exempt corporation annual report fee US$50;
- minimum franchise tax US$175 bajo Authorized Shares Method o US$400 mínimo bajo Assumed Par Value Capital Method.

Fuente:
https://corp.delaware.gov/paytaxes/

ESTIMATE recurring total con agent/tax/accounting: US$1,500–5,000/año para estructura pequeña simple.

## 4. Dividendos / owner chileno

Una C-Corp puede pagar dividendos sujetos a U.S. withholding. El convenio Chile–US puede reducir ciertos source-country rates si se cumplen requisitos y limitation-on-benefits.

Fuente:
https://home.treasury.gov/news/press-releases/jy2003

LEGAL/TAX REVIEW REQUIRED:
- treaty residence;
- LOB;
- ownership;
- dividend classification;
- Chile foreign tax credits/final taxation.

## 5. CFC chilena

Un owner residente/domiciliado en Chile debe analizar art. 41 G para entidad extranjera controlada, en especial si rentas se califican pasivas.

Fuente:
https://www.sii.cl/destacados/reforma_tributaria/41g_renta017.html

No asumir que C-Corp o LLC retiene earnings fuera de Chile sin impacto CFC.

## 6. LLC vs C-Corp

| Factor | Foreign-owned disregarded LLC | C-Corp |
|---|---|---|
| federal entity tax form | owner/source dependent; no regular 1120 por entidad disregarded, pero 5472/pro-forma rules pueden aplicar | 1120; 21% federal corporate tax |
| Form 5472 trap | alto | puede aplicar a 25% foreign-owned corporation y related transactions |
| fundraising US | medio | alto |
| admin | medio | alto |
| conceptual pass-through | sí federal income tax, sujeto a reglas | no |
| Chile complexity | alta | alta |
| recommendation | sólo con razón operativa concreta | preferred if US VC/enterprise requires it |

## 7. Recomendación

No formar LLC sólo por Stripe/banking o supuesto “0% tax” sin modelar source/ECI/Chile/5472.

Considerar C-Corp cuando:
- se prevé inversión US;
- stock/options;
- enterprise customers exigen US counterparty;
- operación real US.

Para negocio bootstrapped desde Chile con consumidores globales, Chile entity + MoR suele ser administrativamente más simple como baseline.

LEGAL/TAX REVIEW REQUIRED antes de cualquier formación/election.
