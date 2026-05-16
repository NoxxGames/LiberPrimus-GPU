"""Pastebin-to-transcript signature alignment."""

from __future__ import annotations

from collections import Counter
from collections.abc import Sequence
from pathlib import Path
from time import perf_counter

from libreprimus.alignment.models import (
    AlignmentCandidate,
    GlyphVariantObservation,
    PastebinTranscriptAlignment,
    Stage0DAlignmentSummary,
    Stage0DFollowupAlignmentSummary,
    TranscriptViewRecord,
)
from libreprimus.alignment.boundary_audit import audit_page_boundaries
from libreprimus.alignment.gap_analysis import build_gap_diagnostics
from libreprimus.alignment.page_boundaries import infer_page_boundaries
from libreprimus.alignment.signatures import (
    DOCUMENTED_VARIANT_MAP,
    build_signature_index,
    pastebin_signature,
    transcript_signature,
    transcript_view_signature,
)
from libreprimus.legacy_pastebin.export import extract_legacy_pastebin
from libreprimus.legacy_pastebin.gematria_validation import PRIME_TO_ENTRY
from libreprimus.legacy_pastebin.models import SOURCE_ID, LegacyPastebinExtraction, LegacyPastebinLinePair
from libreprimus.transcript_sources.models import RTKD_SOURCE_ID, TranscriptLineRecord
from libreprimus.transcript_sources.rtkd_master import parse_rtkd_master
from libreprimus.transcript_sources.views import build_transcript_views

BASELINE_NONE_COUNT = 153


def _candidate_from_signature(signatures: list, match_pass: str, confidence: str, score: float, variant: bool) -> list[AlignmentCandidate]:
    return [
        AlignmentCandidate(
            transcript_physical_line_number=signature.source_index,
            match_pass=match_pass,
            confidence=confidence,
            confidence_score=score,
            variant_mapping_applied=variant,
            neighborhood_supported=False,
            transcript_view_name="physical_line_view",
            transcript_physical_line_start=signature.source_index,
            transcript_physical_line_end=signature.source_index,
            confidence_reason=match_pass,
        )
        for signature in signatures
    ]


def _line_range_for_offsets(
    stream_view: TranscriptViewRecord,
    start_offset: int,
    end_offset: int,
) -> tuple[int | None, int | None]:
    offsets = [
        item
        for item in stream_view.offset_map
        if isinstance(item.get("stream_offset"), int) and start_offset <= int(item["stream_offset"]) <= end_offset
    ]
    if not offsets:
        return None, None
    return int(offsets[0]["physical_line_number"]), int(offsets[-1]["physical_line_number"])


def _candidate_from_view(
    view: TranscriptViewRecord,
    match_pass: str,
    confidence: str,
    score: float,
    *,
    variant: bool,
    start_offset: int | None = None,
    end_offset: int | None = None,
    stream_view: TranscriptViewRecord | None = None,
    reason: str = "",
) -> AlignmentCandidate:
    physical_start = view.source_line_start
    physical_end = view.source_line_end
    if stream_view is not None and start_offset is not None and end_offset is not None:
        physical_start, physical_end = _line_range_for_offsets(stream_view, start_offset, end_offset)
    line_number = physical_start or 0
    logical_start = view.view_record_index if view.view_name == "logical_line_view" else None
    logical_end = view.view_record_index if view.view_name == "logical_line_view" else None
    return AlignmentCandidate(
        transcript_physical_line_number=line_number,
        match_pass=match_pass,
        confidence=confidence,
        confidence_score=score,
        variant_mapping_applied=variant,
        neighborhood_supported=False,
        transcript_view_name=view.view_name,
        transcript_offset_start=start_offset if start_offset is not None else view.source_offset_start,
        transcript_offset_end=end_offset if end_offset is not None else view.source_offset_end,
        transcript_logical_line_start=logical_start,
        transcript_logical_line_end=logical_end,
        transcript_physical_line_start=physical_start,
        transcript_physical_line_end=physical_end,
        confidence_reason=reason or match_pass,
    )


def _subsequence_matches(pastebin_sig, indexes: dict[str, dict[object, list]], *, normalized: bool) -> list:
    sequence = pastebin_sig.normalized_rune_sequence if normalized else pastebin_sig.raw_rune_sequence
    if not sequence:
        return []
    ngram_size = min(8, len(sequence))
    key = (ngram_size, sequence[:ngram_size])
    candidate_signatures = indexes["normalized_subsequence" if normalized else "raw_subsequence"].get(key, [])
    attr = "normalized_rune_sequence" if normalized else "raw_rune_sequence"
    return [signature for signature in candidate_signatures if sequence in getattr(signature, attr)]


def _build_subsequence_index(transcript_signatures, attr: str) -> dict[tuple[int, str], list]:
    index: dict[tuple[int, str], list] = {}
    for signature in transcript_signatures:
        sequence = getattr(signature, attr)
        for ngram_size in range(1, min(8, len(sequence)) + 1):
            seen: set[str] = set()
            for start in range(0, len(sequence) - ngram_size + 1):
                ngram = sequence[start : start + ngram_size]
                if ngram in seen:
                    continue
                seen.add(ngram)
                index.setdefault((ngram_size, ngram), []).append(signature)
    return index


def _build_stream_index(sequence: str) -> dict[tuple[int, str], list[int]]:
    index: dict[tuple[int, str], list[int]] = {}
    if not sequence:
        return index
    for ngram_size in range(1, min(12, len(sequence)) + 1):
        for start in range(0, len(sequence) - ngram_size + 1):
            index.setdefault((ngram_size, sequence[start : start + ngram_size]), []).append(start)
    return index


def _stream_positions(sequence: str, target: str, index: dict[tuple[int, str], list[int]]) -> list[int]:
    if not target:
        return []
    ngram_size = min(12, len(target))
    starts = index.get((ngram_size, target[:ngram_size]), [])
    return [start for start in starts if sequence.startswith(target, start)]


def _view_indexes(views: dict[str, list[TranscriptViewRecord]]) -> dict[str, dict[object, list[TranscriptViewRecord]]]:
    logical_views = [view for view in views.get("logical_line_view", []) if view.rune_count]
    indexes: dict[str, dict[object, list[TranscriptViewRecord]]] = {
        "logical_raw": {},
        "logical_normalized": {},
        "logical_decimal": {},
    }
    for view in logical_views:
        indexes["logical_raw"].setdefault(view.flattened_rune_sequence, []).append(view)
        indexes["logical_normalized"].setdefault(view.normalized_rune_sequence, []).append(view)
        indexes["logical_decimal"].setdefault(tuple(view.decimal_index_sequence), []).append(view)
    return indexes


def _select_physical_candidates(pastebin_sig, indexes: dict[str, dict[object, list]]) -> tuple[list[AlignmentCandidate], str | None]:
    exact_matches = indexes["raw"].get(pastebin_sig.raw_rune_sequence, [])
    if len(exact_matches) == 1:
        return _candidate_from_signature(exact_matches, "exact_raw_rune_sequence", "high", 0.94, False), None
    if len(exact_matches) > 1:
        return _candidate_from_signature(exact_matches, "exact_raw_rune_sequence", "low", 0.55, False), "Exact raw physical-line sequence is ambiguous."

    normalized_matches = indexes["normalized"].get(pastebin_sig.normalized_rune_sequence, [])
    if len(normalized_matches) == 1:
        variant = pastebin_sig.raw_rune_sequence != pastebin_sig.normalized_rune_sequence
        return _candidate_from_signature(normalized_matches, "documented_variant_normalized", "high", 0.9, variant), None
    if len(normalized_matches) > 1:
        return _candidate_from_signature(normalized_matches, "documented_variant_normalized", "low", 0.5, True), "Variant-normalized physical-line sequence is ambiguous."

    decimal_key = tuple(pastebin_sig.decimal_index_sequence)
    decimal_matches = indexes["decimal"].get(decimal_key, [])
    if len(decimal_matches) == 1:
        variant = pastebin_sig.raw_rune_sequence != pastebin_sig.normalized_rune_sequence
        return _candidate_from_signature(decimal_matches, "decimal_index_sequence", "medium", 0.78, variant), None
    if len(decimal_matches) > 1:
        return _candidate_from_signature(decimal_matches, "decimal_index_sequence", "low", 0.45, True), "Decimal-index physical-line sequence is ambiguous."

    raw_subsequence_matches = _subsequence_matches(pastebin_sig, indexes, normalized=False)
    if len(raw_subsequence_matches) == 1:
        return _candidate_from_signature(raw_subsequence_matches, "exact_raw_rune_subsequence", "medium", 0.68, False), None
    if len(raw_subsequence_matches) > 1:
        return _candidate_from_signature(raw_subsequence_matches, "exact_raw_rune_subsequence", "low", 0.4, False), "Raw physical-line subsequence match is ambiguous."

    normalized_subsequence_matches = _subsequence_matches(pastebin_sig, indexes, normalized=True)
    if len(normalized_subsequence_matches) == 1:
        variant = pastebin_sig.raw_rune_sequence != pastebin_sig.normalized_rune_sequence
        return _candidate_from_signature(normalized_subsequence_matches, "documented_variant_normalized_subsequence", "medium", 0.65, variant), None
    if len(normalized_subsequence_matches) > 1:
        return _candidate_from_signature(normalized_subsequence_matches, "documented_variant_normalized_subsequence", "low", 0.35, True), "Variant-normalized physical-line subsequence match is ambiguous."

    return [], None


def _select_physical_exact_candidates(pastebin_sig, indexes: dict[str, dict[object, list]]) -> tuple[list[AlignmentCandidate], str | None]:
    exact_matches = indexes["raw"].get(pastebin_sig.raw_rune_sequence, [])
    if len(exact_matches) == 1:
        return _candidate_from_signature(exact_matches, "physical_line_exact_raw", "high", 0.94, False), None
    if len(exact_matches) > 1:
        return _candidate_from_signature(exact_matches, "physical_line_exact_raw", "low", 0.55, False), "Exact raw physical-line sequence is ambiguous."

    normalized_matches = indexes["normalized"].get(pastebin_sig.normalized_rune_sequence, [])
    if len(normalized_matches) == 1:
        variant = pastebin_sig.raw_rune_sequence != pastebin_sig.normalized_rune_sequence
        return _candidate_from_signature(normalized_matches, "physical_line_documented_variant_normalized", "high", 0.9, variant), None
    if len(normalized_matches) > 1:
        return _candidate_from_signature(normalized_matches, "physical_line_documented_variant_normalized", "low", 0.5, True), "Variant-normalized physical-line sequence is ambiguous."

    decimal_matches = indexes["decimal"].get(tuple(pastebin_sig.decimal_index_sequence), [])
    if len(decimal_matches) == 1:
        variant = pastebin_sig.raw_rune_sequence != pastebin_sig.normalized_rune_sequence
        return _candidate_from_signature(decimal_matches, "physical_line_decimal_index", "medium", 0.78, variant), None
    if len(decimal_matches) > 1:
        return _candidate_from_signature(decimal_matches, "physical_line_decimal_index", "low", 0.45, True), "Decimal-index physical-line sequence is ambiguous."
    return [], None


def _select_followup_candidates(
    pastebin_sig,
    indexes: dict[str, object],
) -> tuple[list[AlignmentCandidate], str | None]:
    physical_candidates, physical_warning = _select_physical_exact_candidates(pastebin_sig, indexes["physical"])  # type: ignore[index]
    if physical_candidates:
        return physical_candidates, physical_warning

    view_indexes = indexes["views"]  # type: ignore[assignment]
    logical_raw = view_indexes["logical_raw"].get(pastebin_sig.raw_rune_sequence, [])  # type: ignore[index]
    if len(logical_raw) == 1:
        return [
            _candidate_from_view(logical_raw[0], "logical_line_exact_raw", "high", 0.9, variant=False, reason="unique logical-line raw match")
        ], None
    if len(logical_raw) > 1:
        return [
            _candidate_from_view(view, "logical_line_exact_raw", "low", 0.48, variant=False, reason="ambiguous logical-line raw match")
            for view in logical_raw
        ], "Logical-line raw sequence is ambiguous."

    logical_normalized = view_indexes["logical_normalized"].get(pastebin_sig.normalized_rune_sequence, [])  # type: ignore[index]
    if len(logical_normalized) == 1:
        variant = pastebin_sig.raw_rune_sequence != pastebin_sig.normalized_rune_sequence
        return [
            _candidate_from_view(logical_normalized[0], "logical_line_documented_variant_normalized", "high", 0.86, variant=variant, reason="unique logical-line normalized match")
        ], None
    if len(logical_normalized) > 1:
        return [
            _candidate_from_view(view, "logical_line_documented_variant_normalized", "low", 0.44, variant=True, reason="ambiguous logical-line normalized match")
            for view in logical_normalized
        ], "Logical-line normalized sequence is ambiguous."

    logical_decimal = view_indexes["logical_decimal"].get(tuple(pastebin_sig.decimal_index_sequence), [])  # type: ignore[index]
    if len(logical_decimal) == 1:
        return [
            _candidate_from_view(logical_decimal[0], "logical_line_decimal_index", "medium", 0.76, variant=True, reason="unique logical-line decimal-index match")
        ], None
    if len(logical_decimal) > 1:
        return [
            _candidate_from_view(view, "logical_line_decimal_index", "low", 0.42, variant=True, reason="ambiguous logical-line decimal-index match")
            for view in logical_decimal
        ], "Logical-line decimal-index sequence is ambiguous."

    stream_view = indexes["stream_view"]  # type: ignore[assignment]
    if stream_view is not None:
        raw_positions = _stream_positions(indexes["raw_stream"], pastebin_sig.raw_rune_sequence, indexes["raw_stream_index"])  # type: ignore[arg-type,index]
        if len(raw_positions) == 1:
            start = raw_positions[0]
            end = start + len(pastebin_sig.raw_rune_sequence) - 1
            return [
                _candidate_from_view(
                    stream_view,
                    "stream_subsequence_exact",
                    "high",
                    0.88,
                    variant=False,
                    start_offset=start,
                    end_offset=end,
                    stream_view=stream_view,
                    reason="unique stream-subsequence raw match",
                )
            ], None
        if len(raw_positions) > 1:
            return [
                _candidate_from_view(
                    stream_view,
                    "stream_subsequence_exact",
                    "low",
                    0.4,
                    variant=False,
                    start_offset=start,
                    end_offset=start + len(pastebin_sig.raw_rune_sequence) - 1,
                    stream_view=stream_view,
                    reason="ambiguous stream-subsequence raw match",
                )
                for start in raw_positions[:20]
            ], "Raw stream-subsequence sequence is ambiguous."

        normalized_positions = _stream_positions(indexes["normalized_stream"], pastebin_sig.normalized_rune_sequence, indexes["normalized_stream_index"])  # type: ignore[arg-type,index]
        if len(normalized_positions) == 1:
            start = normalized_positions[0]
            end = start + len(pastebin_sig.normalized_rune_sequence) - 1
            variant = pastebin_sig.raw_rune_sequence != pastebin_sig.normalized_rune_sequence
            return [
                _candidate_from_view(
                    stream_view,
                    "stream_subsequence_documented_variant_normalized",
                    "high",
                    0.84,
                    variant=variant,
                    start_offset=start,
                    end_offset=end,
                    stream_view=stream_view,
                    reason="unique stream-subsequence normalized match",
                )
            ], None
        if len(normalized_positions) > 1:
            return [
                _candidate_from_view(
                    stream_view,
                    "stream_subsequence_documented_variant_normalized",
                    "low",
                    0.38,
                    variant=True,
                    start_offset=start,
                    end_offset=start + len(pastebin_sig.normalized_rune_sequence) - 1,
                    stream_view=stream_view,
                    reason="ambiguous stream-subsequence normalized match",
                )
                for start in normalized_positions[:20]
            ], "Normalized stream-subsequence sequence is ambiguous."

        decimal_positions = _stream_positions(indexes["decimal_stream"], ",".join(map(str, pastebin_sig.decimal_index_sequence)), indexes["decimal_stream_index"])  # type: ignore[arg-type,index]
        if len(decimal_positions) == 1:
            decimal_start = decimal_positions[0]
            # Convert comma-string start to rune offset by counting separators before the match.
            prefix = indexes["decimal_stream"][:decimal_start]  # type: ignore[index]
            start = 0 if not prefix else str(prefix).count(",") + 1
            end = start + len(pastebin_sig.decimal_index_sequence) - 1
            return [
                _candidate_from_view(
                    stream_view,
                    "stream_subsequence_decimal_index",
                    "medium",
                    0.78,
                    variant=True,
                    start_offset=start,
                    end_offset=end,
                    stream_view=stream_view,
                    reason="unique stream-subsequence decimal-index match",
                )
            ], None
        if len(decimal_positions) > 1:
            return [], "Decimal-index stream-subsequence sequence is ambiguous."

    return [], "No deterministic transcript match found."


def _build_alignment_indexes(
    transcript_records: Sequence[TranscriptLineRecord],
    views: dict[str, list[TranscriptViewRecord]] | None,
) -> dict[str, object]:
    transcript_signatures = [transcript_signature(record) for record in transcript_records if record.rune_count]
    physical = {
        "raw": build_signature_index(transcript_signatures, "raw_rune_sequence"),
        "normalized": build_signature_index(transcript_signatures, "normalized_rune_sequence"),
        "decimal": build_signature_index(transcript_signatures, "decimal_index_sequence"),
        "raw_subsequence": _build_subsequence_index(transcript_signatures, "raw_rune_sequence"),
        "normalized_subsequence": _build_subsequence_index(transcript_signatures, "normalized_rune_sequence"),
    }
    if not views:
        return {"physical": physical, "transcript_signatures": transcript_signatures}

    logical_signatures = [transcript_view_signature(view) for view in views.get("logical_line_view", []) if view.rune_count]
    stream_view = views.get("rune_stream_view", [None])[0]
    raw_stream = stream_view.flattened_rune_sequence if stream_view else ""
    normalized_stream = stream_view.normalized_rune_sequence if stream_view else ""
    decimal_stream = ",".join(map(str, stream_view.decimal_index_sequence)) if stream_view else ""
    return {
        "physical": physical,
        "views": _view_indexes(views),
        "logical_signatures": logical_signatures,
        "stream_view": stream_view,
        "raw_stream": raw_stream,
        "normalized_stream": normalized_stream,
        "decimal_stream": decimal_stream,
        "raw_stream_index": _build_stream_index(raw_stream),
        "normalized_stream_index": _build_stream_index(normalized_stream),
        "decimal_stream_index": _build_stream_index(decimal_stream),
    }


def _pair_distance(current: AlignmentCandidate, other: AlignmentCandidate | None, *, previous: bool) -> int | None:
    if other is None:
        return None
    if current.transcript_offset_start is not None and other.transcript_offset_end is not None and previous:
        return current.transcript_offset_start - other.transcript_offset_end - 1
    if current.transcript_offset_end is not None and other.transcript_offset_start is not None and not previous:
        return other.transcript_offset_start - current.transcript_offset_end - 1
    line_start = current.transcript_physical_line_start or current.transcript_physical_line_number
    other_line = other.transcript_physical_line_end if previous else other.transcript_physical_line_start
    if other_line is None:
        other_line = other.transcript_physical_line_number
    return line_start - other_line if previous else other_line - line_start


def _supported_by_distance(distance: int | None) -> bool:
    return distance is not None and -2 <= distance <= 240


def _upgrade_candidate(candidate: AlignmentCandidate, previous_distance: int | None, next_distance: int | None) -> AlignmentCandidate:
    supported = _supported_by_distance(previous_distance) or _supported_by_distance(next_distance)
    confidence = candidate.confidence
    score = candidate.confidence_score
    if supported and candidate.confidence == "high" and candidate.match_pass in {
        "physical_line_exact_raw",
        "logical_line_exact_raw",
        "stream_subsequence_exact",
    }:
        confidence = "exact"
        score = max(score, 0.96)
    elif supported and candidate.confidence == "medium" and "decimal" in candidate.match_pass:
        confidence = "high"
        score = max(score, 0.84)
    elif not supported and candidate.match_pass.startswith("stream_subsequence") and candidate.confidence == "high":
        confidence = "medium"
        score = min(score, 0.8)
    return AlignmentCandidate(
        transcript_physical_line_number=candidate.transcript_physical_line_number,
        match_pass=candidate.match_pass,
        confidence=confidence,
        confidence_score=score,
        variant_mapping_applied=candidate.variant_mapping_applied,
        neighborhood_supported=supported,
        transcript_view_name=candidate.transcript_view_name,
        transcript_offset_start=candidate.transcript_offset_start,
        transcript_offset_end=candidate.transcript_offset_end,
        transcript_logical_line_start=candidate.transcript_logical_line_start,
        transcript_logical_line_end=candidate.transcript_logical_line_end,
        transcript_physical_line_start=candidate.transcript_physical_line_start,
        transcript_physical_line_end=candidate.transcript_physical_line_end,
        confidence_reason=candidate.confidence_reason,
        previous_pair_distance=previous_distance,
        next_pair_distance=next_distance,
    )


def _gap_reason_for(line_pair: LegacyPastebinLinePair, best_match: AlignmentCandidate | None) -> str:
    if line_pair.empty_pair:
        return "empty_pair"
    if best_match is None:
        if any(glyph in DOCUMENTED_VARIANT_MAP for word in line_pair.rune_words for glyph in word):
            return "glyph_variant_possible"
        return "unknown"
    if "exact_raw" in best_match.match_pass or best_match.match_pass == "stream_subsequence_exact":
        return "matched_exact"
    if "variant" in best_match.match_pass or best_match.variant_mapping_applied:
        return "matched_variant_normalized"
    if "decimal" in best_match.match_pass:
        return "matched_decimal_index"
    if "logical_line" in best_match.match_pass:
        return "segmentation_mismatch_possible"
    if "stream_subsequence" in best_match.match_pass:
        return "stream_subsequence_match_possible"
    return "unknown"


def _with_neighborhood_support(
    records: list[PastebinTranscriptAlignment],
    line_pairs: Sequence[LegacyPastebinLinePair],
) -> list[PastebinTranscriptAlignment]:
    best_by_pair = {record.pastebin_pair_index: record.best_match for record in records if record.best_match is not None}
    pair_by_index = {line_pair.pair_index: line_pair for line_pair in line_pairs}
    updated: list[PastebinTranscriptAlignment] = []
    for record in records:
        if record.best_match is None:
            updated.append(
                PastebinTranscriptAlignment(
                    record_type=record.record_type,
                    source_id=record.source_id,
                    pastebin_source_sha256=record.pastebin_source_sha256,
                    transcript_source_id=record.transcript_source_id,
                    transcript_source_sha256=record.transcript_source_sha256,
                    pastebin_pair_index=record.pastebin_pair_index,
                    pastebin_rune_line_number=record.pastebin_rune_line_number,
                    pastebin_prime_line_number=record.pastebin_prime_line_number,
                    pastebin_rune_count=record.pastebin_rune_count,
                    transcript_candidate_count=record.transcript_candidate_count,
                    best_match=None,
                    all_candidates=record.all_candidates,
                    trusted_as_canonical=record.trusted_as_canonical,
                    canonical_page_boundary=record.canonical_page_boundary,
                    gap_reason=_gap_reason_for(pair_by_index[record.pastebin_pair_index], None),
                    warnings=record.warnings,
                )
            )
            continue
        previous_distance = _pair_distance(record.best_match, best_by_pair.get(record.pastebin_pair_index - 1), previous=True)
        next_distance = _pair_distance(record.best_match, best_by_pair.get(record.pastebin_pair_index + 1), previous=False)
        best = _upgrade_candidate(record.best_match, previous_distance, next_distance)
        all_candidates = [
            _upgrade_candidate(candidate, previous_distance, next_distance)
            if candidate == record.best_match
            else candidate
            for candidate in record.all_candidates
        ]
        updated.append(
            PastebinTranscriptAlignment(
                record_type=record.record_type,
                source_id=record.source_id,
                pastebin_source_sha256=record.pastebin_source_sha256,
                transcript_source_id=record.transcript_source_id,
                transcript_source_sha256=record.transcript_source_sha256,
                pastebin_pair_index=record.pastebin_pair_index,
                pastebin_rune_line_number=record.pastebin_rune_line_number,
                pastebin_prime_line_number=record.pastebin_prime_line_number,
                pastebin_rune_count=record.pastebin_rune_count,
                transcript_candidate_count=record.transcript_candidate_count,
                best_match=best,
                all_candidates=all_candidates,
                trusted_as_canonical=record.trusted_as_canonical,
                canonical_page_boundary=record.canonical_page_boundary,
                gap_reason=_gap_reason_for(pair_by_index[record.pastebin_pair_index], best),
                warnings=record.warnings,
            )
        )
    return updated


def build_alignment_records(
    pastebin_extraction: LegacyPastebinExtraction,
    transcript_records: list[TranscriptLineRecord],
    transcript_views: dict[str, list[TranscriptViewRecord]] | None = None,
    *,
    use_followup_passes: bool = False,
) -> tuple[list[PastebinTranscriptAlignment], dict[str, float]]:
    """Align every Pastebin pair to transcript candidates using bounded signature maps."""
    timings: dict[str, float] = {}
    start = perf_counter()
    pastebin_signatures = [pastebin_signature(line_pair) for line_pair in pastebin_extraction.line_pairs]
    indexes = _build_alignment_indexes(transcript_records, transcript_views if use_followup_passes else None)
    timings["signature_build"] = (perf_counter() - start) * 1000

    start = perf_counter()
    records: list[PastebinTranscriptAlignment] = []
    for line_pair, signature in zip(pastebin_extraction.line_pairs, pastebin_signatures):
        warnings: list[str] = []
        if line_pair.empty_pair:
            candidates: list[AlignmentCandidate] = []
            warnings.append("Empty pair preserved; no transcript match attempted.")
        elif use_followup_passes:
            candidates, warning = _select_followup_candidates(signature, indexes)
            if warning is not None:
                warnings.append(warning)
        else:
            candidates, warning = _select_physical_candidates(signature, indexes["physical"])  # type: ignore[index]
            if warning is not None:
                warnings.append(warning)
            if not candidates:
                warnings.append("No deterministic transcript match found.")

        best_match = candidates[0] if candidates else None
        if candidates and len(candidates) > 1:
            best_match = sorted(
                candidates,
                key=lambda candidate: (
                    candidate.transcript_offset_start is None,
                    candidate.transcript_offset_start or 0,
                    candidate.transcript_physical_line_number,
                ),
            )[0]
        records.append(
            PastebinTranscriptAlignment(
                record_type="pastebin_transcript_alignment",
                source_id=SOURCE_ID,
                pastebin_source_sha256=pastebin_extraction.summary.source_sha256,
                transcript_source_id=RTKD_SOURCE_ID,
                transcript_source_sha256=transcript_records[0].source_sha256 if transcript_records else "",
                pastebin_pair_index=line_pair.pair_index,
                pastebin_rune_line_number=line_pair.source_rune_line_number,
                pastebin_prime_line_number=line_pair.source_prime_line_number,
                pastebin_rune_count=signature.rune_count,
                transcript_candidate_count=len(candidates),
                best_match=best_match,
                all_candidates=candidates,
                trusted_as_canonical=False,
                canonical_page_boundary=False,
                gap_reason=_gap_reason_for(line_pair, best_match),
                warnings=warnings,
            )
        )
    timings["matching"] = (perf_counter() - start) * 1000
    return _with_neighborhood_support(records, pastebin_extraction.line_pairs), timings


def glyph_variant_observations(
    line_pairs: list[LegacyPastebinLinePair],
    alignments: list[PastebinTranscriptAlignment],
    transcript_records: list[TranscriptLineRecord],
    source_sha256: str,
) -> list[GlyphVariantObservation]:
    """Summarize documented glyph variant observations without mutating raw glyphs."""
    transcript_by_line = {record.physical_line_number: record for record in transcript_records}
    occurrences: Counter[tuple[str, int]] = Counter()
    matched_transcript_glyphs: dict[tuple[str, int], set[str]] = {}

    for line_pair in line_pairs:
        for rune_word, prime_word in zip(line_pair.rune_words, line_pair.prime_words):
            for glyph, prime_value in zip(rune_word, prime_word):
                if glyph in DOCUMENTED_VARIANT_MAP:
                    key = (glyph, prime_value)
                    occurrences[key] += 1

    pair_to_alignment = {alignment.pastebin_pair_index: alignment for alignment in alignments}
    for line_pair in line_pairs:
        alignment = pair_to_alignment.get(line_pair.pair_index)
        if alignment is None or alignment.best_match is None:
            continue
        line_start = alignment.best_match.transcript_physical_line_start or alignment.best_match.transcript_physical_line_number
        line_end = alignment.best_match.transcript_physical_line_end or line_start
        transcript_glyph_set: set[str] = set()
        for line_number in range(line_start, line_end + 1):
            transcript = transcript_by_line.get(line_number)
            if transcript is not None:
                transcript_glyph_set.update(transcript.rune_glyphs)
        for rune_word, prime_word in zip(line_pair.rune_words, line_pair.prime_words):
            for glyph, prime_value in zip(rune_word, prime_word):
                if glyph in DOCUMENTED_VARIANT_MAP:
                    key = (glyph, prime_value)
                    matched_transcript_glyphs.setdefault(key, set()).update(transcript_glyph_set)

    observations: list[GlyphVariantObservation] = []
    for (glyph, prime_value), count in sorted(occurrences.items()):
        inferred = PRIME_TO_ENTRY.get(prime_value)
        if inferred is None:
            continue
        observations.append(
            GlyphVariantObservation(
                record_type="glyph_variant_observation",
                source_id=SOURCE_ID,
                source_sha256=source_sha256,
                observed_glyph=glyph,
                observed_prime_value=prime_value,
                inferred_decimal_index=inferred.decimal_index,
                inferred_canonical_glyph_candidate=inferred.rune,
                inferred_latin_label=inferred.label,
                occurrence_count=count,
                matched_transcript_glyphs=sorted(matched_transcript_glyphs.get((glyph, prime_value), set())),
                variant_policy="preserve_raw_apply_documented_normalized_view_only",
                trusted_as_canonical=False,
                warnings=[
                    "Observed glyph is not in legacy validation profile.",
                    "Alias inferred from prime value only unless transcript alignment confirms.",
                ],
            )
        )
    return observations


def build_stage0d_summary(
    *,
    pastebin_extraction: LegacyPastebinExtraction,
    transcript_records: list[TranscriptLineRecord],
    alignments: list[PastebinTranscriptAlignment],
    boundary_candidates: list,
    glyph_observations: list[GlyphVariantObservation],
    elapsed_milliseconds: dict[str, float],
) -> Stage0DAlignmentSummary:
    confidence_counts = Counter(
        alignment.best_match.confidence if alignment.best_match is not None else "none"
        for alignment in alignments
    )
    transcript_sha = transcript_records[0].source_sha256 if transcript_records else ""
    return Stage0DAlignmentSummary(
        record_type="stage0d_alignment_summary",
        pastebin_source_id=SOURCE_ID,
        pastebin_source_sha256=pastebin_extraction.summary.source_sha256,
        transcript_source_id=RTKD_SOURCE_ID,
        transcript_source_sha256=transcript_sha,
        transcript_physical_line_count=len(transcript_records),
        pastebin_line_pair_count=len(pastebin_extraction.line_pairs),
        alignment_record_count=len(alignments),
        exact_confidence_match_count=confidence_counts["exact"],
        high_confidence_match_count=confidence_counts["high"],
        medium_confidence_match_count=confidence_counts["medium"],
        low_confidence_match_count=confidence_counts["low"],
        no_match_count=confidence_counts["none"],
        page_boundary_candidate_count=len(boundary_candidates),
        high_confidence_boundary_count=sum(1 for boundary in boundary_candidates if boundary.confidence == "high"),
        parable_boundary_candidate_present=any(
            "Parable anchor matched" in " ".join(boundary.evidence) for boundary in boundary_candidates
        ),
        glyph_variant_observation_count=len(glyph_observations),
        glyph_variant_occurrence_count=sum(observation.occurrence_count for observation in glyph_observations),
        canonical_corpus_active=False,
        trusted_as_canonical=False,
        page_boundary_status="tentative_not_finalized",
        elapsed_milliseconds={key: round(value, 3) for key, value in elapsed_milliseconds.items()},
        warnings=[
            warning
            for alignment in alignments
            for warning in alignment.warnings
            if warning
        ],
    )


def _pastebin_stream(line_pairs: Sequence[LegacyPastebinLinePair]) -> str:
    return "".join("".join(line_pair.rune_words) for line_pair in line_pairs if not line_pair.empty_pair)


def align_pastebin_to_transcript(
    pastebin_path: Path,
    transcript_path: Path,
    *,
    use_followup_passes: bool = False,
):
    """Run the in-memory Stage 0D alignment pipeline."""
    elapsed: dict[str, float] = {}

    start = perf_counter()
    pastebin_extraction = extract_legacy_pastebin(pastebin_path)
    elapsed["pastebin_parse"] = (perf_counter() - start) * 1000

    start = perf_counter()
    transcript_records, transcript_summary = parse_rtkd_master(transcript_path)
    elapsed["transcript_parse"] = (perf_counter() - start) * 1000

    transcript_views = None
    transcript_views_summary = None
    if use_followup_passes:
        start = perf_counter()
        transcript_views, transcript_views_summary = build_transcript_views(
            transcript_records,
            pastebin_stream=_pastebin_stream(pastebin_extraction.line_pairs),
        )
        elapsed["transcript_view_build"] = (perf_counter() - start) * 1000

    alignments, timing = build_alignment_records(
        pastebin_extraction,
        transcript_records,
        transcript_views,
        use_followup_passes=use_followup_passes,
    )
    elapsed.update(timing)

    start = perf_counter()
    boundary_candidates = infer_page_boundaries(
        pastebin_extraction.line_pairs,
        transcript_records,
        alignments,
        pastebin_extraction.anchors,
    )
    elapsed["boundary_inference"] = (perf_counter() - start) * 1000

    start = perf_counter()
    glyph_observations = glyph_variant_observations(
        pastebin_extraction.line_pairs,
        alignments,
        transcript_records,
        pastebin_extraction.summary.source_sha256,
    )
    elapsed["glyph_variant_summary"] = (perf_counter() - start) * 1000

    summary = build_stage0d_summary(
        pastebin_extraction=pastebin_extraction,
        transcript_records=transcript_records,
        alignments=alignments,
        boundary_candidates=boundary_candidates,
        glyph_observations=glyph_observations,
        elapsed_milliseconds=elapsed,
    )
    return {
        "pastebin_extraction": pastebin_extraction,
        "transcript_records": transcript_records,
        "transcript_summary": transcript_summary,
        "transcript_views": transcript_views,
        "transcript_views_summary": transcript_views_summary,
        "alignments": alignments,
        "boundary_candidates": boundary_candidates,
        "glyph_variant_observations": glyph_observations,
        "summary": summary,
        "elapsed_milliseconds": elapsed,
    }


def build_stage0d_followup_summary(result: dict) -> Stage0DFollowupAlignmentSummary:
    """Build the Stage 0D-followup summary from generated diagnostics."""
    alignments: list[PastebinTranscriptAlignment] = result["alignments"]
    confidence_counts = Counter(
        alignment.best_match.confidence if alignment.best_match is not None else "none"
        for alignment in alignments
    )
    match_pass_counts = Counter(
        alignment.best_match.match_pass
        for alignment in alignments
        if alignment.best_match is not None
    )
    boundary_summary = result["boundary_audit_summary"]
    gap_summary = result["gap_summary"]
    transcript_views_summary = result["transcript_views_summary"]
    pastebin_extraction = result["pastebin_extraction"]
    transcript_records = result["transcript_records"]
    transcript_sha = transcript_records[0].source_sha256 if transcript_records else ""
    none_count = confidence_counts["none"]
    return Stage0DFollowupAlignmentSummary(
        record_type="stage0d_followup_alignment_summary",
        source_id=SOURCE_ID,
        pastebin_source_sha256=pastebin_extraction.summary.source_sha256,
        transcript_source_id=RTKD_SOURCE_ID,
        transcript_source_sha256=transcript_sha,
        transcript_physical_line_count=len(transcript_records),
        transcript_logical_line_count=transcript_views_summary.logical_line_count if transcript_views_summary else 0,
        transcript_rune_stream_length=transcript_views_summary.stream_rune_count if transcript_views_summary else 0,
        pastebin_line_pair_count=len(pastebin_extraction.line_pairs),
        alignment_record_count=len(alignments),
        exact_count=confidence_counts["exact"],
        high_count=confidence_counts["high"],
        medium_count=confidence_counts["medium"],
        low_count=confidence_counts["low"],
        none_count=none_count,
        baseline_none_count=BASELINE_NONE_COUNT,
        no_match_reduction=BASELINE_NONE_COUNT - none_count,
        logical_line_match_count=sum(count for key, count in match_pass_counts.items() if key.startswith("logical_line")),
        stream_subsequence_match_count=sum(count for key, count in match_pass_counts.items() if key.startswith("stream_subsequence")),
        decimal_index_match_count=sum(count for key, count in match_pass_counts.items() if "decimal" in key),
        variant_normalized_match_count=sum(
            1 for alignment in alignments if alignment.best_match is not None and alignment.best_match.variant_mapping_applied
        ),
        gap_reason_counts=gap_summary.gap_reason_counts,
        boundary_high_count=boundary_summary.high_count,
        boundary_medium_count=boundary_summary.medium_count,
        boundary_low_count=boundary_summary.low_count,
        boundary_none_count=boundary_summary.none_count,
        overgeneration_warning=boundary_summary.overgeneration_warning,
        glyph_variant_observation_count=len(result["glyph_variant_observations"]),
        canonical_corpus_active=False,
        page_boundary_status="tentative_not_canonical",
        timing_ms={key: round(value, 3) for key, value in result["elapsed_milliseconds"].items()},
        trusted_as_canonical=False,
    )


def align_pastebin_to_transcript_followup(pastebin_path: Path, transcript_path: Path) -> dict:
    """Run the complete Stage 0D-followup diagnostic alignment pipeline."""
    result = align_pastebin_to_transcript(
        pastebin_path,
        transcript_path,
        use_followup_passes=True,
    )

    start = perf_counter()
    diagnostics, gap_summary = build_gap_diagnostics(
        result["pastebin_extraction"].line_pairs,
        result["alignments"],
        pastebin_source_sha256=result["pastebin_extraction"].summary.source_sha256,
        transcript_source_id=RTKD_SOURCE_ID,
        transcript_source_sha256=result["transcript_records"][0].source_sha256 if result["transcript_records"] else "",
    )
    result["elapsed_milliseconds"]["gap_analysis"] = (perf_counter() - start) * 1000

    start = perf_counter()
    boundary_audits, boundary_audit_summary = audit_page_boundaries(result["boundary_candidates"])
    result["elapsed_milliseconds"]["boundary_audit"] = (perf_counter() - start) * 1000

    result["gap_diagnostics"] = diagnostics
    result["gap_summary"] = gap_summary
    result["boundary_audits"] = boundary_audits
    result["boundary_audit_summary"] = boundary_audit_summary
    result["summary"] = build_stage0d_followup_summary(result)
    return result
