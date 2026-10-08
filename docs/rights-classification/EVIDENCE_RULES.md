# Evidence Rules and Source Policy

Fecha de corte: 2026-10-08.

## Core rule

No A/B/C/D classification without at least one traceable evidence source. No evidence means E.

## Evidence source classes

### P1 — primary legal / licensing authority

Examples:
- WIPO / treaty text;
- national legislation;
- U.S. Copyright Office;
- EUR-Lex;
- Creative Commons legal code/deed.

Use for jurisdiction rules and license meaning.

### P2 — item-level primary rights evidence

Examples:
- license notice in the concrete edition;
- publisher / rights-holder page identifying license;
- rights statement supplied by the rights holder.

Preferred for deciding concrete edition status.

### P3 — official/institutional registry

Examples:
- copyright registry;
- national library authority record;
- institutional repository with explicit rights statement.

Useful for identity, dates and item-level rights when explicit.

### P4 — secondary bibliographic evidence

Useful for author/date identification, not sufficient alone for commercial permission.

### P5 — heuristic / discovery source

Filename, search result snippet, mirror presence, age estimate.

Never sufficient for A/B/C/D.

## Evidence conflict

If authoritative sources conflict, classify E and create a manual-review reason.

## Minimum evidence by class

A:
- evidence for underlying work;
- evidence for edition/file;
- jurisdiction basis;
- no unresolved conflict.

B:
- same as A;
- exact license/conditions captured.

C:
- evidence of NC restriction or equivalent no-commercial term.

D:
- evidence of reserved rights / current protection / permission requirement.

E:
- used whenever the above evidence threshold is not met.

## Creative Commons operational mapping

- CC0: potentially A if all relevant rights/material are covered.
- Public Domain Mark: potentially A if item identity and jurisdiction facts align.
- CC BY: B, attribution.
- CC BY-SA: B, attribution + ShareAlike for adaptations.
- CC BY-ND: B, attribution + no distribution of adaptations.
- CC BY-NC variants: C.

Sources:
- https://creativecommons.org/licenses/
- https://creativecommons.org/public-domain/cc0/
- https://creativecommons.org/public-domain/mark/1.0/

## Audit requirements

Every decision should retain:

- EvidenceURLs;
- EvidenceNotes;
- classification timestamp;
- classifier version;
- manual reviewer when confirmed;
- reason for class change.

Never silently overwrite accepted historical classification state.
