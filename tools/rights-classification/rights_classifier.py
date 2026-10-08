"""Conservative rights-classification engine for Work Item #10 Phase A.

This module operates only on structured evidence supplied by callers.
It does not inspect or infer rights from real corpus content.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class LayerStatus(str, Enum):
    OPEN_COMMERCIAL = "OPEN_COMMERCIAL"
    COMMERCIAL_WITH_CONDITIONS = "COMMERCIAL_WITH_CONDITIONS"
    NONCOMMERCIAL_ONLY = "NONCOMMERCIAL_ONLY"
    RIGHTS_RESERVED_OR_PERMISSION_REQUIRED = "RIGHTS_RESERVED_OR_PERMISSION_REQUIRED"
    UNCERTAIN = "UNCERTAIN"


class CommercialUseClass(str, Enum):
    A = "A_COMMERCIAL_REUSE_CONFIRMED"
    B = "B_COMMERCIAL_WITH_CONDITIONS"
    C = "C_NONCOMMERCIAL_ONLY"
    D = "D_RIGHTS_RESERVED_OR_PERMISSION_REQUIRED"
    E = "E_UNCERTAIN_MANUAL_REVIEW"


@dataclass(frozen=True)
class LayerAssessment:
    status: LayerStatus
    evidence_urls: tuple[str, ...] = ()
    notes: str = ""
    license_id: str = ""


@dataclass(frozen=True)
class ClassificationDecision:
    commercial_use_class: CommercialUseClass
    confidence: str
    manual_review_required: bool
    blocking_reason: str
    evidence_urls: tuple[str, ...]


def _normalized_evidence_urls(layer: LayerAssessment) -> tuple[str, ...]:
    return tuple(url.strip() for url in layer.evidence_urls if url.strip())


def _unique_urls(layers: Iterable[LayerAssessment]) -> tuple[str, ...]:
    seen: set[str] = set()
    result: list[str] = []
    for layer in layers:
        for url in _normalized_evidence_urls(layer):
            if url not in seen:
                seen.add(url)
                result.append(url)
    return tuple(result)


def classify(
    underlying: LayerAssessment,
    edition: LayerAssessment,
    *,
    confidence: str = "HIGH",
) -> ClassificationDecision:
    """Combine underlying-work and concrete-edition assessments conservatively."""

    layers = (underlying, edition)
    urls = _unique_urls(layers)

    if any(layer.status is LayerStatus.UNCERTAIN for layer in layers):
        return ClassificationDecision(
            CommercialUseClass.E,
            "LOW" if confidence == "HIGH" else confidence,
            True,
            "Underlying work or concrete edition remains uncertain.",
            urls,
        )

    if not _normalized_evidence_urls(underlying):
        return ClassificationDecision(
            CommercialUseClass.E,
            "LOW",
            True,
            "Underlying work lacks traceable evidence.",
            urls,
        )

    if not _normalized_evidence_urls(edition):
        return ClassificationDecision(
            CommercialUseClass.E,
            "LOW",
            True,
            "Concrete edition/file lacks traceable evidence.",
            urls,
        )

    if any(
        layer.status is LayerStatus.RIGHTS_RESERVED_OR_PERMISSION_REQUIRED
        for layer in layers
    ):
        return ClassificationDecision(
            CommercialUseClass.D,
            confidence,
            True,
            "Reserved rights or permission requirement exists.",
            urls,
        )

    if any(layer.status is LayerStatus.NONCOMMERCIAL_ONLY for layer in layers):
        return ClassificationDecision(
            CommercialUseClass.C,
            confidence,
            True,
            "At least one rights layer prohibits commercial use.",
            urls,
        )

    if any(
        layer.status is LayerStatus.COMMERCIAL_WITH_CONDITIONS
        for layer in layers
    ):
        return ClassificationDecision(
            CommercialUseClass.B,
            confidence,
            confidence != "HIGH",
            "Commercial reuse is conditional.",
            urls,
        )

    return ClassificationDecision(
        CommercialUseClass.A,
        confidence,
        confidence != "HIGH",
        "Both rights layers support commercial reuse with independent evidence.",
        urls,
    )


def status_from_license(license_id: str) -> LayerStatus:
    """Normalize common license labels without deciding item identity/jurisdiction."""

    value = license_id.strip().upper().replace("_", "-")

    if value in {"CC0", "PUBLIC-DOMAIN", "PUBLIC-DOMAIN-MARK", "PDM"}:
        return LayerStatus.OPEN_COMMERCIAL

    if value in {"CC-BY", "CC-BY-SA", "CC-BY-ND"}:
        return LayerStatus.COMMERCIAL_WITH_CONDITIONS

    if value in {"CC-BY-NC", "CC-BY-NC-SA", "CC-BY-NC-ND"}:
        return LayerStatus.NONCOMMERCIAL_ONLY

    if value in {"ALL-RIGHTS-RESERVED", "PERMISSION-REQUIRED"}:
        return LayerStatus.RIGHTS_RESERVED_OR_PERMISSION_REQUIRED

    return LayerStatus.UNCERTAIN
