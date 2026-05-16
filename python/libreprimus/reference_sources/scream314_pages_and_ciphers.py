"""Extract small method-reference notes from mirrored scream314 pages_and_ciphers."""

from __future__ import annotations

from pathlib import Path
import re

from libreprimus.profiles.gematria_profile import compute_sha256
from libreprimus.reference_sources.models import ReferenceMethodNote

REFERENCE_SOURCE_ID = "scream314-cicada3301-pages-and-ciphers"


KEY_PATTERNS = {
    "DIVINITY": re.compile(r"\bDIVINITY\b", re.IGNORECASE),
    "FIRFUMFERENFE": re.compile(r"\bFIRFUMFERENFE\b", re.IGNORECASE),
}


def _method_family(text: str) -> str | None:
    lowered = text.lower()
    if (
        "vigenere" in lowered
        or "vignere" in lowered
        or "divinity" in lowered
        or "firfumferenfe" in lowered
    ):
        return "vigenere"
    if "reversed gematria" in lowered or "reverse gematria" in lowered:
        return "reverse_gematria"
    if "default gematria" in lowered:
        return "direct_translation"
    if "shift 3 down reversed gematria" in lowered:
        return "rotated_reverse_gematria"
    if "phi" in lowered and "prime" in lowered:
        return "prime_minus_one_stream"
    return None


def _key_candidate(text: str) -> str | None:
    for key, pattern in KEY_PATTERNS.items():
        if pattern.search(text):
            return key
    return None


def _rotation_candidate(text: str) -> int | None:
    match = re.search(r"shift\s+(\d+)\s+down\s+reversed\s+gematria", text, re.IGNORECASE)
    return int(match.group(1)) if match else None


def _skip_rule_candidate(text: str) -> str | None:
    lowered = text.lower()
    if "clear text f" in lowered and "needs to be skipped" in lowered:
        return "cleartext_f_pass_through"
    return None


def _page_label_candidate(text: str) -> str | None:
    match = re.search(r"\b\d{2}\.jpg(?:-\d{2}\.jpg)?\b", text)
    return match.group(0) if match else None


def extract_method_notes(path: Path) -> list[ReferenceMethodNote]:
    """Scan mirrored markdown/html table text for concise method notes."""
    source_sha256 = compute_sha256(path)
    lines = path.read_text(encoding="utf-8").splitlines()
    notes: list[ReferenceMethodNote] = []
    keywords = [
        "reversed Gematria",
        "reverse Gematria",
        "default Gematria",
        "DIVINITY",
        "FIRFUMFERENFE",
        "clear text F",
        "Shift up forward Gematria",
        "Shift 3 down reversed Gematria",
    ]
    for index, line in enumerate(lines, start=1):
        if not any(keyword.lower() in line.lower() for keyword in keywords):
            continue
        excerpt = re.sub(r"\s+", " ", line).strip()
        if len(excerpt) > 300:
            excerpt = excerpt[:297] + "..."
        notes.append(
            ReferenceMethodNote(
                record_type="reference_method_note",
                reference_source_id=REFERENCE_SOURCE_ID,
                source_sha256=source_sha256,
                source_local_path=str(path),
                line_number_start=index,
                line_number_end=index,
                method_family_candidate=_method_family(line),
                key_candidate=_key_candidate(line),
                rotation_candidate=_rotation_candidate(line),
                skip_rule_candidate=_skip_rule_candidate(line),
                page_label_candidate=_page_label_candidate(line),
                raw_excerpt=excerpt,
                trusted_as_canonical=False,
                notes=["Small excerpt retained for method provenance only."],
            )
        )
    return notes
