"""Extract provenance-only tooling notes from mirrored lipeeeee/gematria files."""

from __future__ import annotations

from pathlib import Path
import re

from libreprimus.profiles.gematria_profile import compute_sha256
from libreprimus.reference_sources.models import ToolingReferenceNote

REFERENCE_SOURCE_ID = "lipeeeee-gematria"


BEHAVIOUR_KEYWORDS = {
    "gematria_sum": ["gematria sum", "gematria_sum", "get_gematria"],
    "atbash": ["atbash"],
    "vigenere": ["vigenere"],
    "running_shift": ["running shift", "running_shift"],
    "totient_stream": ["totient", "phi"],
}


def _licence_status(root: Path) -> str:
    license_path = root / "LICENSE"
    if not license_path.is_file():
        return "license_file_missing"
    text = license_path.read_text(encoding="utf-8", errors="replace").lower()
    if "mit license" in text:
        return "MIT license file mirrored"
    return "license file mirrored; review required"


def _excerpt(line: str) -> str:
    excerpt = re.sub(r"\s+", " ", line).strip()
    return excerpt[:217] + "..." if len(excerpt) > 220 else excerpt


def extract_tooling_notes(root: Path) -> list[ToolingReferenceNote]:
    """Scan mirrored files without importing or executing external code."""
    licence = _licence_status(root)
    paths = [
        root / "README.md",
        root / "lib/gematria.py",
        root / "hash.py",
    ]
    notes: list[ToolingReferenceNote] = []
    for path in paths:
        if not path.is_file():
            continue
        source_sha256 = compute_sha256(path)
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        for line_number, line in enumerate(lines, start=1):
            lowered = line.lower()
            for behaviour, keywords in BEHAVIOUR_KEYWORDS.items():
                if any(keyword in lowered for keyword in keywords):
                    notes.append(
                        ToolingReferenceNote(
                            record_type="tooling_reference_note",
                            reference_source_id=REFERENCE_SOURCE_ID,
                            source_sha256=source_sha256,
                            source_local_path=str(path),
                            line_number_start=line_number,
                            line_number_end=line_number,
                            behaviour_candidate=behaviour,
                            raw_excerpt=_excerpt(line),
                            licence_status=licence,
                            imported_as_dependency=False,
                            code_copied=False,
                            trusted_as_canonical=False,
                            notes=[
                                "Reference-only behavioural note; no external code imported or copied."
                            ],
                        )
                    )
    return notes
