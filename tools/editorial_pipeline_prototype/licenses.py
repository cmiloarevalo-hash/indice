"""Conservative parsing of declared licence identifiers (not a proof of grant).

This module interprets licence semantics only. It never establishes that a
licence covers a particular work, translation, edition, file or territory.
Those facts require independent evidence and human review.
"""
from __future__ import annotations

from dataclasses import dataclass
import re
from urllib.parse import urlparse


@dataclass(frozen=True)
class LicenseTerms:
    identifier: str
    recognized: bool
    commercial: bool | None
    adaptation: bool | None
    attribution: bool
    share_alike: bool
    noncommercial: bool
    no_derivatives: bool
    legal_basis: str = "LICENSE"


_UNKNOWN = LicenseTerms(
    "UNKNOWN", False, None, None, False, False, False, False, "UNKNOWN"
)
_ALLOWED_CC = {
    "BY", "BY-SA", "BY-ND", "BY-NC", "BY-NC-SA", "BY-NC-ND"
}
# CC licensing has real version differences; 1.0 is not assumed for all suites.
_SUPPORTED_VERSIONS = {"1.0", "2.0", "2.5", "3.0", "4.0"}
_CC_URL = re.compile(
    r"^https?://(?:www\.)?creativecommons\.org/licenses/"
    r"(by(?:-nc)?(?:-sa|-nd)?)/(\d+(?:\.\d+)?)/?$",
    re.IGNORECASE,
)
_CC0_URL = re.compile(
    r"^https?://(?:www\.)?creativecommons\.org/publicdomain/zero/1\.0/?$",
    re.IGNORECASE,
)
_PDM_URL = re.compile(
    r"^https?://(?:www\.)?creativecommons\.org/publicdomain/mark/1\.0/?$",
    re.IGNORECASE,
)


def parse_license(raw: str | None) -> LicenseTerms:
    """Parse exact known families; malformed, future, and unknown stay UNKNOWN.

    A CC deed URL is a *licence definition*, not evidence that a rights-holder
    applied it to the edition. No machine parsing overrides evidence checks.
    """
    if not isinstance(raw, str) or not raw.strip():
        return _UNKNOWN
    value = raw.strip()
    if _CC0_URL.fullmatch(value):
        value = "CC0-1.0"
    elif _PDM_URL.fullmatch(value):
        value = "PUBLIC-DOMAIN-MARK"
    else:
        url = _CC_URL.fullmatch(value)
        if url:
            value = "CC-" + url.group(1).upper() + "-" + url.group(2)

    value = re.sub(r"[\s_]+", "-", value.upper())
    value = re.sub(r"-+", "-", value).strip("-")

    if value in ("CC0", "CC0-1.0"):
        return LicenseTerms("CC0-1.0", True, True, True, False, False, False, False)

    # Reserved is an observed claim. A conclusion still needs a scoped source.
    if value in ("ALL-RIGHTS-RESERVED", "PERMISSION-REQUIRED"):
        return LicenseTerms(value, True, False, False, False, False, False, False, "RESERVED")

    if value in ("PUBLIC-DOMAIN-MARK", "PDM"):
        # PDM merely marks the object: it is NOT an open grant or a CL term
        # determination. Do not infer commercial use or adaptations from it.
        return LicenseTerms("PUBLIC-DOMAIN-MARK", False, None, None,
                            False, False, False, False, "STATUS_CLAIM")

    if value in ("PUBLIC-DOMAIN", "PUBLIC-DOMAIN-CLAIM"):
        # This is a non-licence status claim for synthetic tests; Phase A
        # still requires separate work AND specific-edition evidence.
        return LicenseTerms("PUBLIC-DOMAIN-CLAIM", True, True, True,
                            False, False, False, False, "STATUS_CLAIM")

    # No substring searching: "CC-BY-NC-4.0" MUST NOT fall through as BY.
    match = re.fullmatch(r"(?:CC-)?(BY(?:-(?:NC|SA|ND)){0,2})(?:-(\d+(?:\.\d+)?))?", value)
    if not match:
        return _UNKNOWN
    family, version = match.groups()
    parts = family.split("-")
    if family not in _ALLOWED_CC:
        return _UNKNOWN
    if version is not None and version not in _SUPPORTED_VERSIONS:
        return _UNKNOWN
    nc = "NC" in parts
    nd = "ND" in parts
    sa = "SA" in parts
    canonical = "CC-" + family + (("-" + version) if version else "")
    return LicenseTerms(canonical, True, not nc, not nd, True, sa, nc, nd)


def license_conflict(
    terms: LicenseTerms,
    *,
    edition_status: str,
    derivative_permission: str,
) -> bool:
    """Detect contradictions, not grant new rights from claimed flags.

    Legal exceptions or additional permissions need a distinct, authenticated
    grant model; generic caller-supplied YES cannot override NC or ND.
    """
    if not terms.recognized or terms.identifier == "UNKNOWN":
        return True

    if terms.legal_basis == "RESERVED":
        return edition_status != "RIGHTS_RESERVED_OR_PERMISSION_REQUIRED"

    if terms.commercial is False:
        if edition_status != "NONCOMMERCIAL_ONLY":
            if terms.legal_basis != "RESERVED":
                return True
    elif terms.commercial is True:
        if edition_status in ("NONCOMMERCIAL_ONLY", "RIGHTS_RESERVED_OR_PERMISSION_REQUIRED"):
            return True
        # BY/SA terms carry affirmative obligations; a claimed unconditional A
        # cannot silently override attribution or ShareAlike.
        if terms.legal_basis == "LICENSE" and (terms.attribution or terms.share_alike):
            if edition_status != "COMMERCIAL_WITH_CONDITIONS":
                return True

    if terms.no_derivatives and derivative_permission == "YES":
        return True
    if derivative_permission not in ("YES", "NO", "UNKNOWN"):
        return True
    return False
