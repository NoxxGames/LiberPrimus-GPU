"""Parser for the rtkd master transcription candidate."""

from __future__ import annotations

import re
from pathlib import Path

from libreprimus.legacy_pastebin.loader import compute_sha256
from libreprimus.legacy_pastebin.gematria_validation import RUNE_TO_ENTRY
from libreprimus.transcript_sources.models import (
    RTKD_SOURCE_ID,
    TranscriptLineRecord,
    TranscriptSourceSummary,
)

RUNE_RE = re.compile(r"[\u16A0-\u16FF]")
PAGE_LABEL_RE = re.compile(r"\b\d{1,3}\.jpg\b", re.IGNORECASE)
SEPARATOR_CHARS = {
    "-": "word",
    ".": "clause",
    "&": "paragraph",
    "$": "segment",
    "§": "chapter",
    "/": "line",
    "%": "page",
}


def _classify_part(line_number: int) -> str | None:
    # rtkd is parsed as a single source stream in Stage 0D. This field is a
    # source-context hint only, not a canonical corpus assertion.
    if line_number > 9:
        return "liber_primus_transcript_stream"
    return "delimiter_header"


def _separator_counts(text: str) -> tuple[dict[str, int], list[str]]:
    counts = {name: 0 for name in SEPARATOR_CHARS.values()}
    counts["unknown_non_rune_symbol"] = 0
    raw_chars: list[str] = []
    for char in text:
        if char in SEPARATOR_CHARS:
            counts[SEPARATOR_CHARS[char]] += 1
            raw_chars.append(char)
        elif RUNE_RE.fullmatch(char) or char.isalnum() or char.isspace() or char == "_":
            continue
        else:
            counts["unknown_non_rune_symbol"] += 1
            raw_chars.append(char)
    return counts, raw_chars


def _line_warnings(stripped: str, rune_glyphs: list[str], separator_counts: dict[str, int]) -> list[str]:
    warnings: list[str] = []
    if rune_glyphs:
        unknown_glyphs = sorted({glyph for glyph in rune_glyphs if glyph not in RUNE_TO_ENTRY})
        if unknown_glyphs:
            glyphs = ", ".join(repr(glyph) for glyph in unknown_glyphs)
            warnings.append(f"Transcript line contains glyphs outside validation profile: {glyphs}.")
        if separator_counts["unknown_non_rune_symbol"]:
            warnings.append("Transcript line contains non-rune symbols outside the documented separator set.")
    elif stripped and separator_counts["unknown_non_rune_symbol"] and not stripped.startswith(("Word", "Clause", "Paragraph", "Segment", "Chapter", "Line", "Page", "Delimiters")):
        warnings.append("Non-rune transcript source line contains symbols outside the documented separator set.")
    return warnings


def parse_rtkd_master(path: Path) -> tuple[list[TranscriptLineRecord], TranscriptSourceSummary]:
    """Parse rtkd master text while preserving raw line text and source markers."""
    resolved = path.resolve()
    source_sha256 = compute_sha256(resolved)
    text = resolved.read_text(encoding="utf-8-sig")
    records: list[TranscriptLineRecord] = []
    source_page_counter: int | None = None

    for line_number, raw_text in enumerate(text.splitlines(), start=1):
        stripped = raw_text.strip()
        rune_glyphs = RUNE_RE.findall(raw_text)
        separator_counts, raw_separator_chars = _separator_counts(raw_text)

        has_percent_marker = stripped == "%"
        page_label_match = PAGE_LABEL_RE.search(stripped)
        has_page_marker = has_percent_marker or page_label_match is not None
        if has_percent_marker:
            source_page_counter = 0 if source_page_counter is None else source_page_counter + 1

        has_section_marker = stripped in {"&", "$", "§"} or separator_counts["paragraph"] > 0 or separator_counts["segment"] > 0 or separator_counts["chapter"] > 0
        inferred_page = source_page_counter if source_page_counter is not None else None
        page_marker_raw = stripped if has_page_marker else None
        warnings = _line_warnings(stripped, rune_glyphs, separator_counts)

        records.append(
            TranscriptLineRecord(
                record_type="transcript_line",
                source_id=RTKD_SOURCE_ID,
                source_sha256=source_sha256,
                source_local_path=str(path.as_posix()),
                physical_line_number=line_number,
                raw_text=raw_text,
                stripped_text=stripped,
                rune_glyphs=rune_glyphs,
                rune_count=len(rune_glyphs),
                separator_counts=separator_counts,
                raw_separator_characters=raw_separator_chars,
                has_page_marker=has_page_marker,
                has_section_marker=has_section_marker,
                inferred_part_candidate=_classify_part(line_number),
                inferred_local_page_candidate=inferred_page,
                page_marker_raw=page_marker_raw,
                parse_warnings=warnings,
                trusted_as_canonical=False,
            )
        )

    summary = TranscriptSourceSummary(
        record_type="transcript_source_summary",
        source_id=RTKD_SOURCE_ID,
        source_sha256=source_sha256,
        source_local_path=str(path.as_posix()),
        physical_line_count=len(records),
        rune_line_count=sum(1 for record in records if record.rune_count),
        rune_count=sum(record.rune_count for record in records),
        page_marker_count=sum(1 for record in records if record.has_page_marker),
        section_marker_count=sum(1 for record in records if record.has_section_marker),
        parse_warning_count=sum(len(record.parse_warnings) for record in records),
        trusted_as_canonical=False,
        canonical_corpus_active=False,
    )
    return records, summary
