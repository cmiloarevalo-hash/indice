# Rights Classification Output Schemas

Fecha de corte: 2026-10-08.

## Full classification dataset

Required columns:

1. RelativePath
2. Name
3. Extension
4. DetectedTitle
5. DetectedAuthor
6. PublicationYear
7. AuthorDeathYear
8. UnderlyingWorkStatus
9. EditionFileStatus
10. CommercialUseClass
11. License
12. AttributionRequired
13. DerivativeRestrictions
14. JurisdictionBasis
15. EvidenceURLs
16. EvidenceNotes
17. Confidence
18. ManualReviewRequired

Recommended additional durable fields:

- RecordId
- EvidenceVersion
- ReviewedAt
- Reviewer
- CountryOfOrigin
- FirstPublicationYear
- EditionPublicationYear
- Translator
- Publisher
- RightsHolder
- AllowedMarkets
- GeoRestrictionRequired
- SourceSnapshotId
- SourceCatalogSHA256
- ClassifierVersion

## commercial_candidates.csv

Contains only A/B.

Minimum columns:

- RecordId
- RelativePath
- DetectedTitle
- DetectedAuthor
- CommercialUseClass
- License
- AttributionRequired
- DerivativeRestrictions
- JurisdictionBasis
- EvidenceURLs
- EvidenceNotes
- Confidence
- ManualReviewRequired
- AllowedMarkets
- GeoRestrictionRequired

Rule: no C/D/E row can enter this output.

## manual_review_queue.csv

Contains D/E.

Minimum columns:

- RecordId
- RelativePath
- DetectedTitle
- DetectedAuthor
- CommercialUseClass
- BlockingReason
- UnderlyingWorkStatus
- EditionFileStatus
- EvidenceURLs
- EvidenceNotes
- Confidence
- RecommendedResearchStep

Rule: D means permission/license required; E means unresolved evidence.

## Evidence serialization

EvidenceURLs is serialized as a semicolon-delimited list of URLs in CSV output.

EvidenceNotes must distinguish:
- OBSERVED: directly supported by evidence;
- INFERENCE: derived reasoning;
- UNKNOWN: missing fact.

## Integrity for future private metadata repository

Per Work Item #10 amendment, future accepted snapshots should preserve:

- row count;
- SHA-256 per catalog/result file;
- source snapshot date;
- accepted corpus/index digest when available;
- immutable historical snapshots.

Actual catalog/results belong in the separate PRIVATE metadata repository, not the public application repository.
