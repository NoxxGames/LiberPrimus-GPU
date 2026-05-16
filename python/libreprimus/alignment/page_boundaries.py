"""Tentative LP2 page-boundary candidate inference."""

from __future__ import annotations

import json
from pathlib import Path

from libreprimus.alignment.models import PageBoundaryCandidate, PastebinTranscriptAlignment
from libreprimus.legacy_pastebin.infer_anchors import PARABLE_WORD
from libreprimus.legacy_pastebin.models import LegacyPastebinAnchor, LegacyPastebinLinePair, SOURCE_ID
from libreprimus.transcript_sources.models import RTKD_SOURCE_ID, TranscriptLineRecord


def _best_line(alignment: PastebinTranscriptAlignment | None) -> int | None:
    if alignment is None or alignment.best_match is None:
        return None
    return alignment.best_match.transcript_physical_line_start or alignment.best_match.transcript_physical_line_number


def _strong_alignment(alignment: PastebinTranscriptAlignment | None) -> bool:
    if alignment is None or alignment.best_match is None:
        return False
    return alignment.best_match.confidence in {"exact", "high"} and (
        alignment.best_match.neighborhood_supported or alignment.best_match.match_pass in {"physical_line_exact_raw", "logical_line_exact_raw"}
    )


def _nearby_alignment_counts(
    alignments: list[PastebinTranscriptAlignment],
    transcript_line: int,
    *,
    window: int = 5,
) -> tuple[int, int]:
    aligned = 0
    no_match = 0
    for alignment in alignments:
        best_line = _best_line(alignment)
        if best_line is None:
            no_match += 1
            continue
        if abs(best_line - transcript_line) <= window and _strong_alignment(alignment):
            aligned += 1
    return aligned, no_match


def _alignment_confidence_for_marker(aligned_count: int) -> str:
    if aligned_count >= 2:
        return "high"
    if aligned_count == 1:
        return "medium"
    return "low"


def infer_page_boundaries(
    line_pairs: list[LegacyPastebinLinePair],
    transcript_records: list[TranscriptLineRecord],
    alignments: list[PastebinTranscriptAlignment],
    anchors: list[LegacyPastebinAnchor] | None = None,
) -> list[PageBoundaryCandidate]:
    """Infer tentative non-canonical page-boundary candidates."""
    boundaries: list[PageBoundaryCandidate] = []
    if not line_pairs or not transcript_records:
        return boundaries

    transcript_sha = transcript_records[0].source_sha256
    pastebin_sha = line_pairs[0].source_sha256
    alignment_by_pair = {alignment.pastebin_pair_index: alignment for alignment in alignments}

    # Explicit transcript source markers are recorded as boundary candidates only.
    matched_lines = {_best_line(alignment) for alignment in alignments if _best_line(alignment) is not None}
    for record in transcript_records:
        if record.has_page_marker and record.stripped_text == "%":
            next_matched = min((line for line in matched_lines if line is not None and line > record.physical_line_number), default=None)
            aligned_nearby, no_match_count = _nearby_alignment_counts(alignments, record.physical_line_number)
            confidence = _alignment_confidence_for_marker(aligned_nearby)
            evidence = ["explicit rtkd percent page marker"]
            if aligned_nearby:
                evidence.append("nearby strong alignment evidence")
            else:
                evidence.append("no nearby strong alignment evidence")
            boundaries.append(
                PageBoundaryCandidate(
                    record_type="lp2_page_boundary_candidate",
                    source_id=SOURCE_ID,
                    pastebin_source_sha256=pastebin_sha,
                    transcript_source_id=RTKD_SOURCE_ID,
                    transcript_source_sha256=transcript_sha,
                    candidate_local_page_index=record.inferred_local_page_candidate,
                    candidate_page_label=None,
                    start_pair_index=None,
                    end_pair_index=None,
                    start_transcript_line=record.physical_line_number,
                    end_transcript_line=next_matched,
                    confidence=confidence,
                    canonical_page_boundary=False,
                    evidence=evidence,
                    explicit_marker=True,
                    anchor_supported=False,
                    aligned_pair_count_near_boundary=aligned_nearby,
                    no_match_count_near_boundary=no_match_count,
                    downgraded_from_previous_policy=confidence != "high",
                    warnings=[
                        "Source marker is not activated as a canonical page boundary in Stage 0D-followup.",
                        "Boundary confidence is downgraded unless local alignment evidence supports it.",
                    ],
                )
            )

    for line_pair in line_pairs:
        if PARABLE_WORD not in line_pair.rune_words:
            continue
        alignment = alignment_by_pair.get(line_pair.pair_index)
        best_line = _best_line(alignment)
        evidence = ["Parable anchor matched"]
        aligned_count = 1 if _strong_alignment(alignment) else 0
        confidence = "low"
        if alignment is not None and alignment.best_match is not None:
            evidence.append("consecutive alignment neighborhood" if alignment.best_match.neighborhood_supported else "aligned to rtkd transcript line")
            confidence = "high" if _strong_alignment(alignment) else "medium"
        if anchors and any(anchor.pair_index == line_pair.pair_index and anchor.page_label_candidate == "57.jpg" for anchor in anchors):
            evidence.append("Stage 0C final-page anchor")
        boundaries.append(
            PageBoundaryCandidate(
                record_type="lp2_page_boundary_candidate",
                source_id=SOURCE_ID,
                pastebin_source_sha256=pastebin_sha,
                transcript_source_id=RTKD_SOURCE_ID,
                transcript_source_sha256=transcript_sha,
                candidate_local_page_index=57,
                candidate_page_label="57.jpg",
                start_pair_index=max(0, line_pair.pair_index - 4),
                end_pair_index=line_pair.pair_index,
                start_transcript_line=best_line - 4 if best_line is not None else None,
                end_transcript_line=best_line,
                confidence=confidence,
                canonical_page_boundary=False,
                evidence=evidence,
                explicit_marker=False,
                anchor_supported=True,
                aligned_pair_count_near_boundary=aligned_count,
                no_match_count_near_boundary=sum(1 for item in alignments if item.best_match is None),
                downgraded_from_previous_policy=confidence != "high",
                warnings=["Final-page anchor is non-authoritative and does not finalize page boundaries."],
            )
        )

    if not boundaries:
        boundaries.append(
            PageBoundaryCandidate(
                record_type="lp2_page_boundary_candidate",
                source_id=SOURCE_ID,
                pastebin_source_sha256=pastebin_sha,
                transcript_source_id=RTKD_SOURCE_ID,
                transcript_source_sha256=transcript_sha,
                candidate_local_page_index=None,
                candidate_page_label=None,
                start_pair_index=None,
                end_pair_index=None,
                start_transcript_line=None,
                end_transcript_line=None,
                confidence="none",
                canonical_page_boundary=False,
                evidence=["no explicit marker or anchor signal emitted"],
                explicit_marker=False,
                anchor_supported=False,
                aligned_pair_count_near_boundary=0,
                no_match_count_near_boundary=sum(1 for item in alignments if item.best_match is None),
                downgraded_from_previous_policy=False,
                warnings=["Stage 0D could not infer page boundaries for this input."],
            )
        )
    return boundaries


def read_alignment_records(path: Path) -> list[dict]:
    """Read generated alignment JSONL records for CLI boundary inference."""
    records: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                records.append(json.loads(stripped))
    return records


def infer_boundaries_from_alignment_file(path: Path) -> list[dict]:
    """Fallback boundary summary from generated alignment records."""
    records = read_alignment_records(path)
    candidates: list[dict] = []
    for record in records:
        best_match = record.get("best_match")
        if best_match and best_match.get("confidence") in {"exact", "high"} and record.get("pastebin_pair_index") is not None:
            continue
    candidates.append(
        {
            "record_type": "lp2_page_boundary_candidate",
            "source_id": SOURCE_ID,
            "candidate_local_page_index": None,
            "candidate_page_label": None,
            "confidence": "none",
            "canonical_page_boundary": False,
            "evidence": ["standalone alignment-file inference requires full transcript context"],
            "warnings": ["Run stage0d-smoke for full boundary inference."],
        }
    )
    return candidates
