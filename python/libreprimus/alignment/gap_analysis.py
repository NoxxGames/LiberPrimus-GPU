"""Alignment gap diagnostics for Stage 0D-followup."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from time import perf_counter

from libreprimus.alignment.models import (
    AlignmentGapDiagnostic,
    AlignmentGapSummary,
    PastebinTranscriptAlignment,
)
from libreprimus.alignment.signatures import DOCUMENTED_VARIANT_MAP, normalize_glyph_sequence, pastebin_signature
from libreprimus.legacy_pastebin.models import LegacyPastebinLinePair


def _hash_sequence(value: object) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _match_status(alignment: PastebinTranscriptAlignment | None) -> str:
    if alignment is None or alignment.best_match is None:
        return "none"
    return alignment.best_match.confidence


def _reason_labels(line_pair: LegacyPastebinLinePair, alignment: PastebinTranscriptAlignment | None) -> list[str]:
    if line_pair.empty_pair:
        return ["empty_pair"]
    if alignment is None or alignment.best_match is None:
        labels = ["unknown"]
        if any(glyph in DOCUMENTED_VARIANT_MAP for word in line_pair.rune_words for glyph in word):
            labels.append("glyph_variant_possible")
        if line_pair.word_count_match and line_pair.per_word_length_match:
            labels.append("stream_subsequence_match_possible")
        else:
            labels.append("segmentation_mismatch_possible")
        return labels
    best = alignment.best_match
    if best.confidence == "low":
        labels = ["duplicate_signature_ambiguous"]
    elif "logical_line" in best.match_pass:
        labels = ["segmentation_mismatch_possible"]
    elif "stream_subsequence" in best.match_pass:
        labels = ["stream_subsequence_match_possible"]
    elif "decimal" in best.match_pass:
        labels = ["matched_decimal_index"]
    elif "variant" in best.match_pass or best.variant_mapping_applied:
        labels = ["matched_variant_normalized"]
    else:
        labels = ["matched_exact"]
    if any(glyph in DOCUMENTED_VARIANT_MAP for word in line_pair.rune_words for glyph in word):
        labels.append("glyph_variant_possible")
    return labels


def _explanation(labels: list[str], alignment: PastebinTranscriptAlignment | None) -> str:
    if "empty_pair" in labels:
        return "Empty structural pair was preserved and not matched."
    if alignment is None or alignment.best_match is None:
        return "No deterministic transcript candidate survived the bounded alignment passes."
    best = alignment.best_match
    return f"Best candidate came from {best.match_pass} with {best.confidence} confidence."


def build_gap_diagnostics(
    line_pairs: list[LegacyPastebinLinePair],
    alignments: list[PastebinTranscriptAlignment],
    *,
    pastebin_source_sha256: str,
    transcript_source_id: str,
    transcript_source_sha256: str,
) -> tuple[list[AlignmentGapDiagnostic], AlignmentGapSummary]:
    """Classify alignment gaps without treating gaps as solve evidence."""
    start = perf_counter()
    by_pair = {alignment.pastebin_pair_index: alignment for alignment in alignments}
    diagnostics: list[AlignmentGapDiagnostic] = []

    for line_pair in line_pairs:
        signature = pastebin_signature(line_pair)
        alignment = by_pair.get(line_pair.pair_index)
        previous_status = _match_status(by_pair.get(line_pair.pair_index - 1))
        next_status = _match_status(by_pair.get(line_pair.pair_index + 1))
        labels = _reason_labels(line_pair, alignment)
        raw_sequence = "".join(line_pair.rune_words)
        prime_values = [value for word in line_pair.prime_words for value in word]
        diagnostics.append(
            AlignmentGapDiagnostic(
                record_type="alignment_gap_diagnostic",
                source_id="pastebin-vGMK330j",
                pastebin_source_sha256=pastebin_source_sha256,
                transcript_source_id=transcript_source_id,
                transcript_source_sha256=transcript_source_sha256,
                pair_index=line_pair.pair_index,
                rune_count=len(raw_sequence),
                word_count=len(line_pair.rune_words),
                word_length_sequence=[len(word) for word in line_pair.rune_words],
                flattened_rune_sha256=_hash_sequence(raw_sequence),
                normalized_rune_sha256=_hash_sequence(normalize_glyph_sequence(raw_sequence)),
                decimal_index_sha256=_hash_sequence(signature.decimal_index_sequence),
                first_rune=raw_sequence[0] if raw_sequence else None,
                last_rune=raw_sequence[-1] if raw_sequence else None,
                first_prime_value=prime_values[0] if prime_values else None,
                last_prime_value=prime_values[-1] if prime_values else None,
                source_rune_line_number=line_pair.source_rune_line_number,
                source_prime_line_number=line_pair.source_prime_line_number,
                previous_pair_match_status=previous_status,
                next_pair_match_status=next_status,
                empty_pair=line_pair.empty_pair,
                contains_variant_glyph=any(glyph in DOCUMENTED_VARIANT_MAP for word in line_pair.rune_words for glyph in word),
                candidate_reason_labels=labels,
                explanation=_explanation(labels, alignment),
                trusted_as_canonical=False,
            )
        )

    reason_counts = Counter(label for diagnostic in diagnostics for label in diagnostic.candidate_reason_labels)
    matched_pairs = sum(
        1
        for alignment in alignments
        if alignment.best_match is not None and alignment.best_match.confidence in {"exact", "high", "medium"}
    )
    no_match_pairs = sum(1 for alignment in alignments if alignment.best_match is None)
    low_confidence_pairs = sum(1 for alignment in alignments if alignment.best_match is not None and alignment.best_match.confidence == "low")
    subsequence_pairs = sum(
        1
        for alignment in alignments
        if alignment.best_match is not None and "stream_subsequence" in alignment.best_match.match_pass
    )
    unresolved = no_match_pairs + low_confidence_pairs
    summary = AlignmentGapSummary(
        record_type="alignment_gap_summary",
        total_pairs=len(line_pairs),
        matched_pairs=matched_pairs,
        no_match_pairs=no_match_pairs,
        low_confidence_pairs=low_confidence_pairs,
        gap_reason_counts=dict(sorted(reason_counts.items())),
        empty_pair_count=sum(1 for line_pair in line_pairs if line_pair.empty_pair),
        pairs_with_variant_glyphs=sum(
            1 for line_pair in line_pairs if any(glyph in DOCUMENTED_VARIANT_MAP for word in line_pair.rune_words for glyph in word)
        ),
        pairs_with_subsequence_matches_after_new_passes=subsequence_pairs,
        unresolved_pairs=unresolved,
        top_20_unresolved_pair_indices=[
            diagnostic.pair_index
            for diagnostic in diagnostics
            if "unknown" in diagnostic.candidate_reason_labels or "duplicate_signature_ambiguous" in diagnostic.candidate_reason_labels
        ][:20],
        timing_ms={"gap_analysis": round((perf_counter() - start) * 1000, 3)},
        trusted_as_canonical=False,
    )
    return diagnostics, summary
