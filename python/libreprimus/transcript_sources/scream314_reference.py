"""Parser for secondary scream314 Liber Primus markdown references."""

from __future__ import annotations

import re
from pathlib import Path

from libreprimus.legacy_pastebin.loader import compute_sha256
from libreprimus.transcript_sources.models import (
    SCREAM314_SOURCE_ID,
    Scream314ReferenceRecord,
    Scream314ReferenceSummary,
)

PAGE_LABEL_RE = re.compile(r"\b\d{1,3}\.jpg\b", re.IGNORECASE)
PART_RE = re.compile(r"\bLP[12]\b", re.IGNORECASE)
METHOD_KEYWORDS = ("vigenere", "gematria", "atbash", "prime", "totient", "phi", "caesar", "key")


def _reference_kind(line: str, page_label: str | None, part_label: str | None, keywords: list[str]) -> str | None:
    stripped = line.strip()
    if page_label is not None:
        return "page_label"
    if "pages long" in stripped.lower() and part_label is not None:
        return "page_count_statement"
    if stripped.startswith("#") and ("solved" in stripped.lower() or "liber primus" in stripped.lower()):
        return "section_title"
    if keywords:
        return "method_keyword"
    return None


def parse_scream314_reference(path: Path) -> tuple[list[Scream314ReferenceRecord], Scream314ReferenceSummary]:
    """Extract page-label and solved-section context without treating markdown as corpus."""
    resolved = path.resolve()
    source_sha256 = compute_sha256(resolved)
    text = resolved.read_text(encoding="utf-8-sig")
    records: list[Scream314ReferenceRecord] = []
    lp2_statement: str | None = None

    for line_number, raw_text in enumerate(text.splitlines(), start=1):
        page_match = PAGE_LABEL_RE.search(raw_text)
        part_match = PART_RE.search(raw_text)
        keywords = [keyword for keyword in METHOD_KEYWORDS if keyword in raw_text.lower()]
        kind = _reference_kind(
            raw_text,
            page_match.group(0) if page_match else None,
            part_match.group(0).upper() if part_match else None,
            keywords,
        )
        if kind is None:
            continue
        if kind == "page_count_statement" and part_match and part_match.group(0).upper() == "LP2":
            lp2_statement = raw_text.strip()
        solved_section_title = raw_text.strip("# ").strip() if raw_text.lstrip().startswith("#") else None
        records.append(
            Scream314ReferenceRecord(
                record_type="scream314_reference_record",
                source_id=SCREAM314_SOURCE_ID,
                source_sha256=source_sha256,
                source_local_path=str(path.as_posix()),
                physical_line_number=line_number,
                raw_text=raw_text,
                reference_kind=kind,
                page_label=page_match.group(0) if page_match else None,
                part_label=part_match.group(0).upper() if part_match else None,
                solved_section_title=solved_section_title,
                method_keywords=keywords,
                trusted_as_canonical=False,
            )
        )

    summary = Scream314ReferenceSummary(
        record_type="scream314_reference_summary",
        source_id=SCREAM314_SOURCE_ID,
        source_sha256=source_sha256,
        source_local_path=str(path.as_posix()),
        physical_line_count=len(text.splitlines()),
        reference_record_count=len(records),
        page_label_count=sum(1 for record in records if record.page_label is not None),
        lp2_page_count_statement=lp2_statement,
        trusted_as_canonical=False,
        canonical_corpus_active=False,
    )
    return records, summary
