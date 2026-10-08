# Rights Classification Phase A — Methodology

Fecha de corte: 2026-10-08.

## Purpose

This Phase A defines a conservative, reusable methodology for Work Item #10 without classifying any real library record.

The classifier operates on **structured evidence**. It does not infer permission from filenames, age, availability on the Internet, repository presence, or commercial convenience.

## Decision unit

Every decision separates:

1. underlying work rights;
2. concrete edition/file rights.

Final CommercialUseClass is assigned only after both layers are evaluated.

## Final classes

- A_COMMERCIAL_REUSE_CONFIRMED
- B_COMMERCIAL_WITH_CONDITIONS
- C_NONCOMMERCIAL_ONLY
- D_RIGHTS_RESERVED_OR_PERMISSION_REQUIRED
- E_UNCERTAIN_MANUAL_REVIEW

## Conservative combination rule

Each layer receives one normalized status:

- OPEN_COMMERCIAL
- COMMERCIAL_WITH_CONDITIONS
- NONCOMMERCIAL_ONLY
- RIGHTS_RESERVED_OR_PERMISSION_REQUIRED
- UNCERTAIN

Combination:

1. if either layer is UNCERTAIN → E;
2. else if either layer is RIGHTS_RESERVED_OR_PERMISSION_REQUIRED → D;
3. else if either layer is NONCOMMERCIAL_ONLY → C;
4. else if either layer is COMMERCIAL_WITH_CONDITIONS → B;
5. else both layers are OPEN_COMMERCIAL → A.

A/B/C/D require at least one traceable EvidenceURL. If evidence is absent, final class is E.

## License normalization

Recognized evidence examples:

- Public domain / patrimonio cultural común: potentially OPEN_COMMERCIAL, only after jurisdiction and edition are verified.
- CC0 / Public Domain Mark: potentially OPEN_COMMERCIAL when evidence applies to the concrete material.
- CC BY: COMMERCIAL_WITH_CONDITIONS.
- CC BY-SA: COMMERCIAL_WITH_CONDITIONS.
- CC BY-ND: COMMERCIAL_WITH_CONDITIONS; derivative distribution restricted.
- CC BY-NC / BY-NC-SA / BY-NC-ND: NONCOMMERCIAL_ONLY.
- Explicit reserved copyright / permission required: RIGHTS_RESERVED_OR_PERMISSION_REQUIRED.
- Unknown, contradictory, ambiguous, orphaned, edition mismatch: UNCERTAIN.

Creative Commons sources:
- https://creativecommons.org/licenses/
- https://creativecommons.org/public-domain/

## Evidence priority

Highest to lower authority:

1. official law / treaty text;
2. license or rights statement attached to the concrete edition;
3. rights-holder / publisher official source;
4. Creative Commons legal/deed source matching the license;
5. official copyright / authority / bibliographic registry;
6. institutional repository with explicit item-level rights statement;
7. secondary bibliographic source;
8. heuristic metadata.

Heuristic metadata can assist research but cannot by itself produce A/B/C/D.

## Public-domain rule

Do not infer public domain solely from publication year.

For Chile baseline, Work Item #10 requires Ley 17.336 and the general life + 70 rule plus applicable special rules:
https://www.bcn.cl/leychile/navegar?idNorma=28933

Foreign works require jurisdiction-specific analysis. Work Item #11 strategy head is reference context for Chile / US / EU / Mexico.

## Internet availability rule

Finding a copy at Internet Archive, Google Books, Scribd, PDFDrive, mirrors or another public URL does not establish commercial reuse rights.

## Derivative-edition rule

A public-domain underlying text can still have a protected:

- translation;
- introduction;
- annotations;
- illustrations;
- cover;
- editorial selection;
- other edition-specific material.

Therefore A requires both layers to be commercially reusable.

## Confidence and manual review

Suggested Confidence values:

- HIGH: primary/authoritative evidence directly covers the concrete work/edition and relevant jurisdiction.
- MEDIUM: strong evidence exists but one material fact still requires corroboration.
- LOW: evidence is indirect, heuristic or incomplete.

Any LOW/MEDIUM automated inference remains ManualReviewRequired=true until corroborated.

E always requires manual review.

## Phase A scope

Included:
- decision engine;
- output schemas;
- synthetic fixtures;
- tests;
- evidence rules.

Excluded:
- access to books_index.csv;
- access to corpus;
- classification of 28,781 real records;
- OCR/full text;
- rights-holder outreach;
- commercial exploitation.

Phase B remains a later real-catalog operation.
