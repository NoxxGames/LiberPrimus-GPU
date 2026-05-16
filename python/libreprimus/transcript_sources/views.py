"""Deterministic transcript views for Stage 0D-followup alignment."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

from libreprimus.alignment.models import TranscriptViewRecord, TranscriptViewsSummary
from libreprimus.alignment.signatures import decimal_indices_for_glyphs, normalize_glyph_sequence
from libreprimus.legacy_pastebin.gematria_validation import RUNE_TO_ENTRY
from libreprimus.transcript_sources.models import TranscriptLineRecord

LINE_TERMINATOR = "/"


def _separator_profile(records: Iterable[TranscriptLineRecord]) -> dict[str, int]:
    profile: dict[str, int] = {}
    for record in records:
        for key, value in record.separator_counts.items():
            profile[key] = profile.get(key, 0) + value
    return profile


def _line_rune_columns(raw_text: str) -> list[int]:
    return [index + 1 for index, char in enumerate(raw_text) if "\u16a0" <= char <= "\u16ff"]


def _view_record(
    *,
    source_id: str,
    source_sha256: str,
    view_name: str,
    view_record_index: int,
    raw_text_span: str,
    rune_sequence: str,
    source_line_start: int | None,
    source_line_end: int | None,
    source_offset_start: int | None,
    source_offset_end: int | None,
    separator_profile: dict[str, int] | None = None,
    raw_marker_text: str | None = None,
    offset_map: list[dict[str, int | str | None]] | None = None,
) -> TranscriptViewRecord:
    return TranscriptViewRecord(
        record_type="transcript_view_record",
        source_id=source_id,
        source_sha256=source_sha256,
        view_name=view_name,
        view_record_index=view_record_index,
        raw_text_span=raw_text_span,
        flattened_rune_sequence=rune_sequence,
        normalized_rune_sequence=normalize_glyph_sequence(rune_sequence),
        decimal_index_sequence=decimal_indices_for_glyphs(rune_sequence),
        rune_count=len(rune_sequence),
        source_line_start=source_line_start,
        source_line_end=source_line_end,
        source_offset_start=source_offset_start,
        source_offset_end=source_offset_end,
        separator_profile=separator_profile or {},
        trusted_as_canonical=False,
        raw_marker_text=raw_marker_text,
        offset_map=offset_map or [],
    )


def build_physical_line_view(records: Sequence[TranscriptLineRecord]) -> list[TranscriptViewRecord]:
    """Return one view record per physical transcript line."""
    views: list[TranscriptViewRecord] = []
    stream_offset = 0
    for index, record in enumerate(records):
        rune_sequence = "".join(record.rune_glyphs)
        columns = _line_rune_columns(record.raw_text)
        offset_map: list[dict[str, int | str | None]] = []
        for local_index, glyph in enumerate(record.rune_glyphs):
            offset_map.append(
                {
                    "stream_offset": stream_offset + local_index,
                    "physical_line_number": record.physical_line_number,
                    "source_column": columns[local_index] if local_index < len(columns) else None,
                    "glyph": glyph,
                }
            )
        views.append(
            _view_record(
                source_id=record.source_id,
                source_sha256=record.source_sha256,
                view_name="physical_line_view",
                view_record_index=index,
                raw_text_span=record.raw_text,
                rune_sequence=rune_sequence,
                source_line_start=record.physical_line_number,
                source_line_end=record.physical_line_number,
                source_offset_start=stream_offset if rune_sequence else None,
                source_offset_end=stream_offset + len(rune_sequence) - 1 if rune_sequence else None,
                separator_profile=record.separator_counts,
                raw_marker_text=record.page_marker_raw,
                offset_map=offset_map,
            )
        )
        stream_offset += len(rune_sequence)
    return views


def build_rune_stream_view(records: Sequence[TranscriptLineRecord]) -> list[TranscriptViewRecord]:
    """Return one flattened transcript rune stream with source offset mapping."""
    if not records:
        return []
    glyphs: list[str] = []
    offset_map: list[dict[str, int | str | None]] = []
    for record in records:
        columns = _line_rune_columns(record.raw_text)
        for local_index, glyph in enumerate(record.rune_glyphs):
            offset_map.append(
                {
                    "stream_offset": len(glyphs),
                    "physical_line_number": record.physical_line_number,
                    "source_column": columns[local_index] if local_index < len(columns) else None,
                    "glyph": glyph,
                    "page_marker_raw": record.page_marker_raw,
                }
            )
            glyphs.append(glyph)
    return [
        _view_record(
            source_id=records[0].source_id,
            source_sha256=records[0].source_sha256,
            view_name="rune_stream_view",
            view_record_index=0,
            raw_text_span="<flattened rune stream>",
            rune_sequence="".join(glyphs),
            source_line_start=records[0].physical_line_number,
            source_line_end=records[-1].physical_line_number,
            source_offset_start=0 if glyphs else None,
            source_offset_end=len(glyphs) - 1 if glyphs else None,
            separator_profile=_separator_profile(records),
            offset_map=offset_map,
        )
    ]


def build_logical_line_view(records: Sequence[TranscriptLineRecord]) -> list[TranscriptViewRecord]:
    """Split transcript rune text on documented line terminators while preserving source spans."""
    views: list[TranscriptViewRecord] = []
    buffer_glyphs: list[str] = []
    buffer_raw: list[str] = []
    buffer_offsets: list[dict[str, int | str | None]] = []
    line_start: int | None = None
    stream_offset = 0
    record_index = 0

    def flush(end_line: int | None) -> None:
        nonlocal record_index, buffer_glyphs, buffer_raw, buffer_offsets, line_start
        if not buffer_glyphs and not buffer_raw:
            return
        views.append(
            _view_record(
                source_id=records[0].source_id,
                source_sha256=records[0].source_sha256,
                view_name="logical_line_view",
                view_record_index=record_index,
                raw_text_span="\n".join(buffer_raw),
                rune_sequence="".join(buffer_glyphs),
                source_line_start=line_start,
                source_line_end=end_line,
                source_offset_start=buffer_offsets[0]["stream_offset"] if buffer_offsets else None,
                source_offset_end=buffer_offsets[-1]["stream_offset"] if buffer_offsets else None,
                separator_profile={},
                offset_map=buffer_offsets,
            )
        )
        record_index += 1
        buffer_glyphs = []
        buffer_raw = []
        buffer_offsets = []
        line_start = None

    for record in records:
        if record.has_page_marker or record.has_section_marker:
            flush(record.physical_line_number - 1)
        segment_raw: list[str] = []
        for column, char in enumerate(record.raw_text, start=1):
            if char == LINE_TERMINATOR:
                if segment_raw:
                    buffer_raw.append("".join(segment_raw))
                    segment_raw = []
                flush(record.physical_line_number)
                continue
            segment_raw.append(char)
            if "\u16a0" <= char <= "\u16ff":
                if line_start is None:
                    line_start = record.physical_line_number
                buffer_offsets.append(
                    {
                        "stream_offset": stream_offset,
                        "physical_line_number": record.physical_line_number,
                        "source_column": column,
                        "glyph": char,
                    }
                )
                buffer_glyphs.append(char)
                stream_offset += 1
        if segment_raw and (record.rune_count or buffer_glyphs):
            buffer_raw.append("".join(segment_raw))
    flush(records[-1].physical_line_number if records else None)
    return views


def build_page_marker_view(records: Sequence[TranscriptLineRecord]) -> list[TranscriptViewRecord]:
    """Collect explicit page and section marker records without canonicalizing them."""
    marker_records = [record for record in records if record.has_page_marker or record.has_section_marker]
    views: list[TranscriptViewRecord] = []
    for index, record in enumerate(marker_records):
        views.append(
            _view_record(
                source_id=record.source_id,
                source_sha256=record.source_sha256,
                view_name="page_marker_view",
                view_record_index=index,
                raw_text_span=record.raw_text,
                rune_sequence="".join(record.rune_glyphs),
                source_line_start=record.physical_line_number,
                source_line_end=record.physical_line_number,
                source_offset_start=None,
                source_offset_end=None,
                separator_profile=record.separator_counts,
                raw_marker_text=record.page_marker_raw or record.stripped_text,
            )
        )
    return views


def build_lp2_candidate_span_view(
    records: Sequence[TranscriptLineRecord],
    pastebin_stream: str | None = None,
) -> list[TranscriptViewRecord]:
    """Return a candidate LP2 span if the Pastebin rune stream is found contiguously."""
    if not records or not pastebin_stream:
        return []
    stream = build_rune_stream_view(records)
    if not stream:
        return []
    raw_stream = stream[0].flattened_rune_sequence
    offset = raw_stream.find(pastebin_stream)
    normalized = normalize_glyph_sequence(raw_stream)
    normalized_pastebin = normalize_glyph_sequence(pastebin_stream)
    variant_match = False
    if offset < 0:
        offset = normalized.find(normalized_pastebin)
        variant_match = offset >= 0
    if offset < 0:
        return []
    end_offset = offset + len(pastebin_stream) - 1
    offset_map = [
        item
        for item in stream[0].offset_map
        if isinstance(item.get("stream_offset"), int) and offset <= int(item["stream_offset"]) <= end_offset
    ]
    if offset_map:
        start_line = int(offset_map[0]["physical_line_number"])  # type: ignore[arg-type]
        end_line = int(offset_map[-1]["physical_line_number"])  # type: ignore[arg-type]
    else:
        start_line = None
        end_line = None
    return [
        _view_record(
            source_id=records[0].source_id,
            source_sha256=records[0].source_sha256,
            view_name="lp2_candidate_span_view",
            view_record_index=0,
            raw_text_span="normalized variant candidate span" if variant_match else "raw candidate span",
            rune_sequence=raw_stream[offset : end_offset + 1],
            source_line_start=start_line,
            source_line_end=end_line,
            source_offset_start=offset,
            source_offset_end=end_offset,
            separator_profile={},
            offset_map=offset_map,
        )
    ]


def build_transcript_views(
    records: Sequence[TranscriptLineRecord],
    pastebin_stream: str | None = None,
) -> tuple[dict[str, list[TranscriptViewRecord]], TranscriptViewsSummary]:
    """Build all Stage 0D-followup transcript views."""
    if not records:
        summary = TranscriptViewsSummary(
            record_type="transcript_views_summary",
            source_id="unknown",
            source_sha256="",
            physical_line_count=0,
            logical_line_count=0,
            stream_rune_count=0,
            explicit_marker_count=0,
            candidate_lp2_span_found=False,
            trusted_as_canonical=False,
        )
        return {}, summary

    views = {
        "physical_line_view": build_physical_line_view(records),
        "rune_stream_view": build_rune_stream_view(records),
        "logical_line_view": build_logical_line_view(records),
        "page_marker_view": build_page_marker_view(records),
        "lp2_candidate_span_view": build_lp2_candidate_span_view(records, pastebin_stream),
    }
    stream = views["rune_stream_view"][0] if views["rune_stream_view"] else None
    summary = TranscriptViewsSummary(
        record_type="transcript_views_summary",
        source_id=records[0].source_id,
        source_sha256=records[0].source_sha256,
        physical_line_count=len(records),
        logical_line_count=len(views["logical_line_view"]),
        stream_rune_count=stream.rune_count if stream else 0,
        explicit_marker_count=len(views["page_marker_view"]),
        candidate_lp2_span_found=bool(views["lp2_candidate_span_view"]),
        trusted_as_canonical=False,
    )
    return views, summary


def canonical_glyph_set() -> set[str]:
    """Return the legacy validation rune glyph set used for transcript diagnostics."""
    return set(RUNE_TO_ENTRY)
