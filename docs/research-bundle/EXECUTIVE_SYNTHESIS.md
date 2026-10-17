# Executive Synthesis — Rights, Market and International Structure

Research cutoff: 2026-10-08.

This synthesis consolidates Work Item #10 Phase A, Work Item #13 and Work Item #14 under Work Item #15. It is a research deliverable only. It does not authorize sales, publication, outreach, company formation, tax registrations, payments, licensing or deployment.

## 1. Executive recommendation

Biblioteca Desktop should be developed first as **Spanish-first, private/local-first specialist research software**, not as a promise to redistribute the full 28,781-book corpus.

The rights framework must fail closed: direct monetization requires sufficient evidence for both the underlying work and the concrete edition/file. Uncertain or unsupported cases are E, never implicit permission.

The closest direct competitor is Libra Esoterica. The strongest workflow substitutes are Readwise, Logos, JSTOR, Zotero, Consensus and Elicit. Specialist cultural memberships such as PRS, Embassy of the Free Mind, Theosophical Society and Internet Sacred Text Archive show willingness to pay for niche access/community, but do not prove SaaS demand.

Initial prices to test:
- Free: US$0;
- Pro: US$9/month or US$79/year;
- Research/AI: US$19/month or approximately US$189/year;
- Institutional: US$1,500–3,000/year pilot.

These are HYPOTHESES, not approved commercial prices.

Working market ranges:
- TAM: US$10M–50M/year, ESTIMATE, LOW confidence;
- SAM: US$3M–18M/year, ESTIMATE, LOW-MEDIUM confidence;
- first 24–36 month SOM validation band: US$138k–414k annualized, HYPOTHESIS, LOW confidence.

Entity/tax recommendation by stage:
- pre-revenue: no foreign entity solely for tax optimization;
- initial revenue: evaluate Chile operating structure, likely SpA if a separate entity is needed, plus Merchant of Record;
- expansion: evaluate U.S. C-Corp only for U.S. fundraising/enterprise/operations needs; evaluate Estonia OÜ only for substantive EU operational reasons;
- foreign-owned U.S. disregarded LLC is not the default recommendation because Form 5472/pro-forma 1120 and Chile CFC/source/ECI analysis add meaningful compliance.

Every entity recommendation remains LEGAL/TAX REVIEW REQUIRED.

## 2. How rights classification works

### Decision unit

Each record is evaluated as two independent layers:

1. underlying work rights;
2. concrete edition/file rights.

A public-domain text does not automatically free a modern translation, introduction, annotations, illustrations, cover, edited compilation or scan/edition with separate protectable contributions.

### Final classes

- A_COMMERCIAL_REUSE_CONFIRMED
- B_COMMERCIAL_WITH_CONDITIONS
- C_NONCOMMERCIAL_ONLY
- D_RIGHTS_RESERVED_OR_PERMISSION_REQUIRED
- E_UNCERTAIN_MANUAL_REVIEW

### Conservative combination

- any UNCERTAIN layer -> E;
- otherwise any RIGHTS_RESERVED_OR_PERMISSION_REQUIRED layer -> D;
- otherwise any NONCOMMERCIAL_ONLY layer -> C;
- otherwise any COMMERCIAL_WITH_CONDITIONS layer -> B;
- only two OPEN_COMMERCIAL layers -> A.

A/B/C/D require traceable evidence. If evidence is missing, the output is E.

### Evidence priority

1. official legislation/treaty;
2. item-level license/rights notice attached to the concrete edition;
3. rights-holder/publisher official source;
4. Creative Commons official materials;
5. official registry or institutional rights statement;
6. bibliographic/authority data;
7. secondary sources;
8. heuristics only for discovery.

Filename, age or Internet availability cannot create permission.

### Phase A tooling verification

OBSERVED on 2026-10-08:
- reusable Python classifier;
- standard library only;
- synthetic fixtures only;
- 9 tests executed;
- 9 passed;
- 0 failed.

No real catalog or book was accessed or classified.

## 3. Competitors that matter most

### Direct benchmark — Libra Esoterica

OBSERVED on 2026-10-08:
- 93,815 catalog records;
- 44,119 public full texts;
- 48 libraries/archives;
- US$9/month or US$79/year;
- AI research console, semantic search, cross-book correlation and passage citations.

Source:
https://libraesoterica.com/pro

Strategic implication:
Biblioteca Desktop should not compete on raw title count. The differentiation is Spanish depth, private/local operation, rights evidence, edition awareness and traceable research workflow.

### Workflow/research substitutes

OBSERVED examples:
- Readwise: US$12.99 month-to-month or US$119.88/year;
- Logos: Premium/Pro/Max US$9.99/14.99/19.99 monthly; US$99.99/149.99/199.99 annual;
- JSTOR JPASS: US$19.50/month or US$199/year;
- Zotero: core free, storage from free to US$120/year;
- Consensus: Pro US$20/month or US$144/year; Deep US$65/month or US$540/year;
- Elicit: Basic free; Plus US$11/user/month annual; Pro US$39/user/month annual on the observed pricing page.

Sources:
- https://readwise.io/pricing/reader
- https://desktop.logos.com/configure/subscriptions
- https://www.jstor.org/jpass
- https://www.zotero.org/storage/
- https://help.consensus.app/en/articles/10087865-subscription-plans
- https://elicit.com/pricing

These products validate willingness to pay for research workflow independently from owning the underlying content corpus.

### Specialist cultural/community substitutes

OBSERVED:
- PRS: US$7/month Initiate, US$10/month Scribe;
- Embassy of the Free Mind: €100/year Pearl, €500 Ruby, €1,000 Diamond, €10,000 Opal;
- Theosophical Society: US$120/year standard, US$60 discounted, US$240 supporting;
- Internet Sacred Text Archive: free base, US$3/month ad-free, US$10/month Supporter.

Sources:
- https://www.prs.org/membership.html
- https://www.embassyofthefreemind.com/membership
- https://www.theosophical.org/membership
- https://sacred-texts.com/subscribe

## 4. Plausible market size

No official source measures “Spanish esoteric research-library software.” Market sizing is triangulation, not observed market share.

### Observed adjacent anchors

AAP, published 2026-08-10:
- U.S. publishing 2025: US$33.4B;
- Trade consumer books: US$21.7B;
- Religious Presses: US$2.2B.

Source:
https://publishers.org/news/aap-statshot-annual-report-publishing-revenues-totaled-33-4-billion-for-calendar-year-2025/

Instituto Cervantes 2025:
- 635,743,644 potential Spanish speakers;
- 519,115,258 native proficiency;
- 24,560,143 learners.

Source:
https://observatoriodelespanol.cervantes.org/wp-content/uploads/2025/10/Spanish_a_language_to_the_world_2025.pdf

U.S. adjacent-interest signal:
- Census 2025 population estimate: 341,784,857;
- under 18: 21.1%;
- derived adults: approximately 269.7M;
- Pew 2025: 30% of U.S. adults consult astrology/horoscopes, tarot or fortune tellers at least annually;
- derived adjacent-interest ceiling: approximately 80.9M adults.

Sources:
- https://www.census.gov/quickfacts/fact/table/US/COM100223
- https://www.pewresearch.org/religion/2025/05/21/3-in-10-americans-consult-astrology-tarot-cards-or-fortune-tellers/

The 80.9M calculation is an ESTIMATE of adjacent interest, not potential subscribers. Pew reports much of this participation is casual.

### Working model

ESTIMATE / LOW confidence:
- TAM US$10M–50M/year.

ESTIMATE / LOW-MEDIUM confidence:
- SAM US$3M–18M/year.

HYPOTHESIS / LOW confidence:
- first 24–36 month SOM validation band US$138k–414k annualized.

Illustrative SOM construction:
- 1,000–3,000 Pro users at US$9/month;
- 10–30 institutions at a HYPOTHETICAL US$3,000 ACV.

These are planning bands, not forecasts.

## 5. Most attractive customer segments

### P1 — Spanish-speaking esoteric researchers and collectors

Why:
- strongest fit with the existing desktop/local architecture;
- fragmented personal collections create an immediate search/catalog pain;
- value does not depend on redistribution rights for the real corpus.

### P1 — academics and postgraduate researchers in religion/history of ideas

Why:
- high value from provenance, citations, editions and relationship graphs;
- potential institutional route where individual budgets are limited.

### P1 B2B — libraries, special collections and research centers

Why:
- privacy/local deployment;
- provenance and rights registry;
- specialist discovery;
- potentially higher contract value.

Tradeoff:
slower procurement and stronger support/security requirements.

Secondary segments:
advanced practitioners, digital-humanities researchers, research-heavy creators, rare-book collectors/dealers, educators, publishers/translators and general-interest readers.

## 6. Initial pricing

HYPOTHESIS for future validation:

### Free
US$0.

Purpose:
acquisition and activation through local import/catalog/search.

### Pro
US$9/month or US$79/year.

Evidence:
- exact Libra Esoterica direct anchor;
- close to PRS/Sacred Texts/Theosophical specialist membership pricing;
- below Readwise monthly pricing.

### Research / AI
US$19/month or approximately US$189/year.

Evidence:
- near JSTOR JPASS US$19.50/month;
- near Consensus Pro US$20/month;
- below higher research tiers.

Launch gate:
reliable citations, visible provenance, privacy and controlled inference cost.

### Institutional
US$1,500–3,000/year pilot.

HYPOTHESIS only. Institutional willingness-to-pay requires customer discovery.

## 7. Recommended positioning

Primary positioning:

**Spanish-first, rights-aware and private-first esoteric research software: organize a local collection, discover relationships among authors/topics/editions and research with traceable sources without handing the whole library to an opaque cloud service.**

Alternative if #10 Phase B produces a large A/B subset:

**Rights-cleared Spanish esoteric digital library with citation-first research.**

Alternative if user-owned collections dominate value:

**The private operating system for personal esoteric and occult-research libraries.**

## 8. International structure by stage

### Pre-revenue

Recommendation:
do not create a foreign company solely for tax.

Chile baseline:
Article 3 of the Chilean Income Tax Law generally taxes residents/domiciliaries on worldwide income. Article 41 G can attribute certain passive income from controlled foreign entities; SII includes royalties among passive categories.

Primary sources:
- https://www.bcn.cl/leychile/Navegar?idNorma=6368
- https://www.sii.cl/destacados/reforma_tributaria/41g_renta017.html

### Initial revenue — illustrative US$25k–100k/year

Baseline to evaluate:
Chile SpA + Merchant of Record.

Why:
- local operating/tax center matches management in Chile for the working scenario;
- avoids a foreign annual entity stack solely for checkout;
- MoR delegates much indirect-tax, fraud, dispute and transaction-support work.

OBSERVED MoR pricing:
- Paddle: 5% + US$0.50 per checkout transaction;
- Stripe Managed Payments: +3.5% per successful transaction plus standard Stripe processing.

Sources:
- https://www.paddle.com/pricing
- https://stripe.com/managed-payments

At a HYPOTHETICAL US$79 average order value, Paddle standard formula is about 5.63% before refunds, FX and custom pricing:
- US$25k gross -> approximately US$1.4k;
- US$100k -> approximately US$5.6k;
- US$500k -> approximately US$28.2k.

These are ESTIMATES, not quotes.

### Expansion — illustrative US$500k+ / institutional / fundraising

Re-evaluate based on the actual trigger rather than a revenue threshold alone.

#### U.S. C-Corp

Evaluate when there is:
- U.S. venture fundraising;
- stock/options requirement;
- substantial U.S. operations;
- enterprise counterparties requiring a U.S. corporation.

Federal corporate tax baseline is 21%, plus state taxation where applicable. Owner-level Chile taxation and treaty treatment remain separate.

#### Foreign-owned single-member U.S. LLC

Not the default tax recommendation.

IRS baseline:
- domestic single-member LLC is disregarded by default unless it elects corporate treatment;
- foreign-owned U.S. disregarded entity may require Form 5472 with pro-forma Form 1120;
- Form 5472 failure penalty begins at US$25,000.

Sources:
- https://www.irs.gov/businesses/small-businesses-self-employed/single-member-limited-liability-companies
- https://www.irs.gov/instructions/i5472

ECI/FDAP/source treatment remains fact-dependent:
- https://www.irs.gov/individuals/international-taxpayers/effectively-connected-income-eci
- https://www.irs.gov/individuals/international-taxpayers/fixed-determinable-annual-or-periodical-fdap-income

#### Estonia OÜ / e-Residency

Evaluate only for a real EU operating reason.

OBSERVED:
- e-Residency application: €150;
- OÜ registration: €265;
- contact person: €200–400/year;
- accounting from €50/month;
- official rough first-year total: about €600 DIY or €1,300 with accounting support;
- distributed profits taxed at company level at 22/78 from 2025.

Sources:
- https://learn.e-resident.gov.ee/hc/en-gb/articles/360000625118-Costs-fees
- https://www.emta.ee/en/business-client/taxes-and-payment/income-and-social-taxes/income-tax-and-basic-exemption

e-Residency does not change personal tax residence. Foreign management can create PE/dual-residence issues.

LEGAL/TAX REVIEW REQUIRED for all options.

## 9. VAT, sales tax and treaty baseline

OBSERVED:
- Chile applies 19% VAT to relevant remote digital services supplied by nonresidents;
- Chile export-of-services VAT treatment is conditional and not every foreign SaaS sale is automatically exempt;
- Non-Union OSS can simplify EU B2C service VAT reporting for qualifying non-EU suppliers;
- ViDA was adopted in 2025 and phases changes through 2035;
- Chile-U.S. income-tax treaty entered into force 2023-12-19; withholding provisions became effective 2024-02-01 and other taxes from tax years beginning 2024-01-01.

Sources:
- https://www.sii.cl/destacados/iva_digital/
- https://www.sii.cl/destacados/exportador_servicios/
- https://vat-one-stop-shop.ec.europa.eu/one-stop-shop/register-oss_en
- https://taxation-customs.ec.europa.eu/taxation/vat/vat-digital-age-vida_en
- https://www.irs.gov/publications/p901

Treaty benefits, PE, source, CFC, foreign-tax-credit and income classification remain LEGAL/TAX REVIEW REQUIRED.

## 10. Decisions that can be made now

1. Use the conservative A/B/C/D/E evidence engine.
2. Keep underlying-work and concrete-edition rights separate.
3. Build a viable software/research product without assuming the real corpus is commercially distributable.
4. Lead with Spanish-first + private/local + rights-aware positioning.
5. Design Free / Pro / Research / Institutional packaging.
6. Use US$79/year as the first Pro willingness-to-pay anchor.
7. Keep Research/AI separately metered/priced.
8. Design checkout so a future MoR can be inserted without restructuring core product logic.
9. Keep copyright rights status independent from entity jurisdiction.
10. Do not form a foreign company before a concrete operational trigger.
11. Use wishlist/demand signals for restricted titles without redistributing them.
12. Prioritize customer discovery with researchers/collectors, academics and institutions.
13. Build evidence/versioning/attribution/geo controls before commercial content delivery.

## 11. Decisions that must wait for Work Item #10 Phase B

Do not decide from Phase A:

- actual A/B/C/D/E counts across 28,781 records;
- size of commercial-download catalog;
- specific bundles;
- POD candidates;
- real-title licensing priorities;
- title-level rights-clearance cost;
- geo-restricted catalog by jurisdiction;
- content-membership value based on real rights coverage;
- content revenue assumptions;
- marketing claims about commercially accessible rare books.

Phase B is the evidence gate between a software-first business thesis and any concrete commercial-content catalog.

## 12. Main unknowns

- real willingness-to-pay;
- Free-to-paid conversion;
- retention;
- CAC;
- local/private premium;
- AI versus metadata/graph value;
- institutional ACV;
- actual proportion of A/B after Phase B;
- title-level licensing economics;
- exact founder/entity tax facts;
- actual need for a foreign entity.

## 13. Overall recommendation

Proceed conceptually as a **software-first, rights-aware research product**.

Do not make viability contingent on commercializing the entire historical corpus.

Use Work Item #10 Phase B to determine how much lawful content monetization can be layered on top of software value.

For operating structure, prefer minimum complexity until customer geography, revenue, fundraising, staffing or licensing contracts justify something more complex. Chile + MoR is the leading initial-revenue baseline for evaluation; U.S. C-Corp and Estonia OÜ are conditional expansion tools, not tax shortcuts.

No commercial/entity execution is authorized by Work Item #15.
