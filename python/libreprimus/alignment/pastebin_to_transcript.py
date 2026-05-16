"""Pastebin-to-transcript signature alignment."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from time import perf_counter

from libreprimus.alignment.models import (
    AlignmentCandidate,
    GlyphVariantObservation,
    PastebinTranscriptAlignment,
    Stage0DAlignmentSummary,
)
from libreprimus.alignment.page_boundaries import infer_page_boundaries
from libreprimus.alignment.signatures import (
    DOCUMENTED_VARIANT_MAP,
    build_signature_index,
    pastebin_signature,
    transcript_signature,
)
from libreprimus.legacy_pastebin.export import extract_legacy_pastebin
from libreprimus.legacy_pastebin.gematria_validation import PRIME_TO_ENTRY
from libreprimus.legacy_pastebin.models import SOURCE_ID, LegacyPastebinExtraction, LegacyPastebinLinePair
from libreprimus.transcript_sources.models import RTKD_SOURCE_ID, TranscriptLineRecord
from libreprimus.transcript_sources.rtkd_master import parse_rtkd_master


def _candidate(signatures: list, match_pass: str, confidence: str, score: float, variant: bool) -> list[AlignmentCandidate]:
    return [
        AlignmentCandidate(
            transcript_physical_line_number=signature.source_index,
            match_pass=match_pass,
            confidence=confidence,
            confidence_score=score,
            variant_mapping_applied=variant,
            neighborhood_supported=False,
        )
        for signature in signatures
    ]


def _subsequence_matches(pastebin_sig, indexes: dict[str, dict[object, list]], *, normalized: bool) -> list:
    sequence = pastebin_sig.normalized_rune_sequence if normalized else pastebin_sig.raw_rune_sequence
    if not sequence:
        return []
    ngram_size = min(8, len(sequence))
    key = (ngram_size, sequence[:ngram_size])
    candidate_signatures = indexes["normalized_subsequence" if normalized else "raw_subsequence"].get(key, [])
    attr = "normalized_rune_sequence" if normalized else "raw_rune_sequence"
    return [signature for signature in candidate_signatures if sequence in getattr(signature, attr)]


def _select_candidates(pastebin_sig, indexes: dict[str, dict[object, list]]) -> tuple[list[AlignmentCandidate], str | None]:
    exact_matches = indexes["raw"].get(pastebin_sig.raw_rune_sequence, [])
    if len(exact_matches) == 1:
        return _candidate(exact_matches, "exact_raw_rune_sequence", "exact", 1.0, False), None
    if len(exact_matches) > 1:
        return _candidate(exact_matches, "exact_raw_rune_sequence", "low", 0.55, False), "Exact raw rune sequence is ambiguous."

    normalized_matches = indexes["normalized"].get(pastebin_sig.normalized_rune_sequence, [])
    if len(normalized_matches) == 1 and pastebin_sig.raw_rune_sequence != pastebin_sig.normalized_rune_sequence:
        return _candidate(normalized_matches, "documented_variant_normalized", "high", 0.92, True), None
    if len(normalized_matches) == 1:
        return _candidate(normalized_matches, "documented_variant_normalized", "high", 0.9, False), None
    if len(normalized_matches) > 1:
        return _candidate(normalized_matches, "documented_variant_normalized", "low", 0.5, True), "Variant-normalized sequence is ambiguous."

    decimal_key = tuple(pastebin_sig.decimal_index_sequence)
    decimal_matches = indexes["decimal"].get(decimal_key, [])
    if len(decimal_matches) == 1:
        variant = pastebin_sig.raw_rune_sequence != pastebin_sig.normalized_rune_sequence
        return _candidate(decimal_matches, "decimal_index_sequence", "medium", 0.8, variant), None
    if len(decimal_matches) > 1:
        return _candidate(decimal_matches, "decimal_index_sequence", "low", 0.45, True), "Decimal-index sequence is ambiguous."

    raw_subsequence_matches = _subsequence_matches(pastebin_sig, indexes, normalized=False)
    if len(raw_subsequence_matches) == 1:
        return _candidate(raw_subsequence_matches, "exact_raw_rune_subsequence", "medium", 0.78, False), None
    if len(raw_subsequence_matches) > 1:
        return _candidate(raw_subsequence_matches, "exact_raw_rune_subsequence", "low", 0.4, False), "Raw rune subsequence match is ambiguous."

    normalized_subsequence_matches = _subsequence_matches(pastebin_sig, indexes, normalized=True)
    if len(normalized_subsequence_matches) == 1:
        variant = pastebin_sig.raw_rune_sequence != pastebin_sig.normalized_rune_sequence
        return _candidate(normalized_subsequence_matches, "documented_variant_normalized_subsequence", "medium", 0.72, variant), None
    if len(normalized_subsequence_matches) > 1:
        return _candidate(normalized_subsequence_matches, "documented_variant_normalized_subsequence", "low", 0.35, True), "Variant-normalized subsequence match is ambiguous."

    return [], "No deterministic transcript match found."


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


def _with_neighborhood_support(
    records: list[PastebinTranscriptAlignment],
) -> list[PastebinTranscriptAlignment]:
    best_by_pair = {
        record.pastebin_pair_index: record.best_match.transcript_physical_line_number
        for record in records
        if record.best_match is not None
    }
    updated: list[PastebinTranscriptAlignment] = []
    for record in records:
        if record.best_match is None:
            updated.append(record)
            continue
        line = record.best_match.transcript_physical_line_number
        neighborhood_supported = (
            best_by_pair.get(record.pastebin_pair_index - 1) in {line - 1, line - 2}
            or best_by_pair.get(record.pastebin_pair_index + 1) in {line + 1, line + 2}
        )
        best = AlignmentCandidate(
            transcript_physical_line_number=record.best_match.transcript_physical_line_number,
            match_pass=record.best_match.match_pass,
            confidence=record.best_match.confidence,
            confidence_score=record.best_match.confidence_score,
            variant_mapping_applied=record.best_match.variant_mapping_applied,
            neighborhood_supported=neighborhood_supported,
        )
        all_candidates = [
            AlignmentCandidate(
                transcript_physical_line_number=candidate.transcript_physical_line_number,
                match_pass=candidate.match_pass,
                confidence=candidate.confidence,
                confidence_score=candidate.confidence_score,
                variant_mapping_applied=candidate.variant_mapping_applied,
                neighborhood_supported=neighborhood_supported
                if candidate.transcript_physical_line_number == best.transcript_physical_line_number
                else candidate.neighborhood_supported,
            )
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
                warnings=record.warnings,
            )
        )
    return updated


def build_alignment_records(
    pastebin_extraction: LegacyPastebinExtraction,
    transcript_records: list[TranscriptLineRecord],
) -> tuple[list[PastebinTranscriptAlignment], dict[str, float]]:
    """Align every Pastebin pair to transcript candidates using signature maps."""
    timings: dict[str, float] = {}
    start = perf_counter()
    pastebin_signatures = [pastebin_signature(line_pair) for line_pair in pastebin_extraction.line_pairs]
    transcript_signatures = [transcript_signature(record) for record in transcript_records if record.rune_count]
    timings["signature_build"] = (perf_counter() - start) * 1000

    start = perf_counter()
    indexes = {
        "raw": build_signature_index(transcript_signatures, "raw_rune_sequence"),
        "normalized": build_signature_index(transcript_signatures, "normalized_rune_sequence"),
        "decimal": build_signature_index(transcript_signatures, "decimal_index_sequence"),
        "raw_subsequence": _build_subsequence_index(transcript_signatures, "raw_rune_sequence"),
        "normalized_subsequence": _build_subsequence_index(transcript_signatures, "normalized_rune_sequence"),
    }
    records: list[PastebinTranscriptAlignment] = []
    for line_pair, signature in zip(pastebin_extraction.line_pairs, pastebin_signatures):
        warnings: list[str] = []
        if line_pair.empty_pair:
            candidates: list[AlignmentCandidate] = []
            warnings.append("Empty pair preserved; no transcript match attempted.")
        else:
            candidates, warning = _select_candidates(signature, indexes)
            if warning is not None:
                warnings.append(warning)
        best_match = candidates[0] if candidates else None
        if candidates and len(candidates) > 1:
            best_match = sorted(candidates, key=lambda candidate: candidate.transcript_physical_line_number)[0]
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
                warnings=warnings,
            )
        )
    timings["matching"] = (perf_counter() - start) * 1000
    return _with_neighborhood_support(records), timings


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
        transcript = transcript_by_line.get(alignment.best_match.transcript_physical_line_number)
        if transcript is None:
            continue
        transcript_glyph_set = set(transcript.rune_glyphs)
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


def align_pastebin_to_transcript(pastebin_path: Path, transcript_path: Path):
    """Run the full in-memory Stage 0D alignment pipeline."""
    elapsed: dict[str, float] = {}

    start = perf_counter()
    pastebin_extraction = extract_legacy_pastebin(pastebin_path)
    elapsed["pastebin_parse"] = (perf_counter() - start) * 1000

    start = perf_counter()
    transcript_records, transcript_summary = parse_rtkd_master(transcript_path)
    elapsed["transcript_parse"] = (perf_counter() - start) * 1000

    alignments, timing = build_alignment_records(pastebin_extraction, transcript_records)
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
        "alignments": alignments,
        "boundary_candidates": boundary_candidates,
        "glyph_variant_observations": glyph_observations,
        "summary": summary,
    }
