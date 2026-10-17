# Evidence Rules and Source Policy

Fecha de corte: 2026-10-08.

## Core rule

No A/B/C/D classification unless **both rights layers are independently evidenced**:

1. the underlying work has at least one traceable, nonblank evidence source; and
2. the concrete edition/file has at least one traceable, nonblank evidence source.

Evidence present only for one layer cannot be reused as a substitute for missing evidence in the other layer. If either layer lacks evidence, classify E_UNCERTAIN_MANUAL_REVIEW.

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
- independent evidence for underlying work;
- independent evidence for edition/file;
- jurisdiction basis;
- no unresolved conflict.

B:
- independent evidence for both layers;
- exact license/conditions captured.

C:
- independent evidence for both layers;
- evidence establishing the NC restriction or equivalent no-commercial term on the applicable layer.

D:
- independent evidence for both layers;
- evidence establishing reserved rights / current protection / permission requirement on the applicable layer.

E:
- used whenever either layer lacks evidence, is uncertain, or has unresolved conflicting evidence.

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

- layer-specific EvidenceURLs;
- EvidenceNotes;
- classification timestamp;
- classifier version;
- manual reviewer when confirmed;
- reason for class change.

Never silently overwrite accepted historical classification state.
