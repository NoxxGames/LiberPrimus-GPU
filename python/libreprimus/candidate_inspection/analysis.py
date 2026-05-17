"""Analyze bounded candidate outputs without publishing full candidate dumps."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from statistics import mean, median
from typing import Any

from libreprimus.candidate_inspection.loader import load_stage_outputs
from libreprimus.candidate_inspection.models import InspectionSummary
from libreprimus.scoring.minimal_triage import score_text
from libreprimus.scoring.validation import validate_minimal_triage_score


def inspect_results(results_dir: Path, *, top_n: int = 25, rerank: bool = False) -> InspectionSummary:
    records, top_records, summary = load_stage_outputs(results_dir)
    if not records:
        raise ValueError("No candidate records found.")
    top_slice = top_records[:top_n] if top_records else sorted(records, key=_existing_score, reverse=True)[:top_n]
    refined_records = rerank_candidates(records) if rerank else []
    refined_top = refined_records[0] if refined_records else None
    top_candidate = top_slice[0]
    diagnostics = _diagnostics(top_candidate)
    qualitative = _qualitative_label(top_candidate, refined_top)
    return InspectionSummary(
        results_dir=str(results_dir),
        run_id=str(summary.get("run_id", top_candidate.get("run_id", ""))),
        candidate_count=len(records),
        top_n=len(top_slice),
        top_candidate=_candidate_summary(top_candidate),
        refined_top_candidate=_candidate_summary(refined_top) if refined_top else None,
        transform_family_counts=dict(Counter(str(record.get("transform_family", "")) for record in records)),
        top_transform_family_counts=dict(Counter(str(record.get("transform_family", "")) for record in top_slice)),
        score_distribution=_score_distribution(records),
        score_gaps=_score_gaps(top_slice),
        diagnostics=diagnostics,
        qualitative_label=qualitative,
        recommendation=_recommendation(qualitative),
        warnings=_warnings(top_candidate, diagnostics),
    )


def rerank_candidates(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    reranked: list[dict[str, Any]] = []
    for record in records:
        updated = dict(record)
        score = validate_minimal_triage_score(score_text(str(record.get("output_normalized_text", ""))))
        updated["score_summary"] = score
        features = dict(updated.get("ranking_features", {}))
        features.update(
            {
                "total_score": score["total_score"],
                "length_normalized_score": score["length_normalized_score"],
                "common_word_hit_count": score["common_word_hit_count"],
                "separator_aware_word_count": score["separator_aware_word_count"],
                "impossible_bigram_count": score["impossible_bigram_count"],
                "confidence_label": score["confidence_label"],
            }
        )
        updated["ranking_features"] = features
        reranked.append(updated)
    return sorted(
        reranked,
        key=lambda record: (
            float(record["score_summary"]["length_normalized_score"]),
            float(record["score_summary"]["total_score"]),
            int(record["score_summary"]["separator_aware_word_count"]),
            -int(record["candidate_index"]),
        ),
        reverse=True,
    )


def _existing_score(record: dict[str, Any]) -> float:
    return float(record.get("score_summary", {}).get("total_score", 0.0))


def _candidate_summary(record: dict[str, Any] | None) -> dict[str, Any]:
    if not record:
        return {}
    score = dict(record.get("score_summary", {}))
    return {
        "candidate_index": record.get("candidate_index"),
        "transform_family": record.get("transform_family"),
        "transform_parameters": record.get("transform_parameters", {}),
        "output_sha256": record.get("output_sha256"),
        "total_score": score.get("total_score"),
        "length_normalized_score": score.get("length_normalized_score"),
        "confidence_label": score.get("confidence_label", "unlabeled"),
        "vowel_ratio": score.get("vowel_ratio"),
        "common_word_hits": score.get("common_word_hits", []),
        "separator_aware_word_count": score.get("separator_aware_word_count", 0),
        "impossible_bigram_hits": score.get("impossible_bigram_hits", []),
        "negative_features": score.get("negative_features", []),
    }


def _score_distribution(records: list[dict[str, Any]]) -> dict[str, float]:
    scores = [_existing_score(record) for record in records]
    return {
        "min": round(min(scores), 6),
        "max": round(max(scores), 6),
        "mean": round(mean(scores), 6),
        "median": round(median(scores), 6),
    }


def _score_gaps(top_records: list[dict[str, Any]]) -> dict[str, float]:
    scores = [_existing_score(record) for record in top_records]
    top = scores[0] if scores else 0.0
    second = scores[1] if len(scores) > 1 else top
    tenth = scores[9] if len(scores) > 9 else scores[-1] if scores else top
    return {
        "top1_minus_top2": round(top - second, 6),
        "top1_minus_top10": round(top - tenth, 6),
    }


def _diagnostics(record: dict[str, Any]) -> dict[str, Any]:
    text = str(record.get("output_normalized_text", ""))
    score = dict(record.get("score_summary", {}))
    return {
        "normalized_length": len(text),
        "space_count": text.count(" "),
        "separator_count": sum(1 for char in text if not char.isalnum() and not char.isspace()),
        "vowel_ratio": score.get("vowel_ratio"),
        "common_word_hit_count": score.get("common_word_hit_count"),
        "repeated_character_penalty": score.get("repeated_character_penalty"),
        "entropy": score.get("entropy"),
        "unknown_symbol_count": score.get("unknown_symbol_count"),
        "confidence_label": score.get("confidence_label", "unlabeled"),
    }


def _qualitative_label(top_candidate: dict[str, Any], refined_top: dict[str, Any] | None) -> str:
    candidate = refined_top or top_candidate
    score = dict(candidate.get("score_summary", {}))
    label = str(score.get("confidence_label", ""))
    if label in {"lead", "weak_lead"}:
        return "promising"
    if label == "garbage":
        return "obviously_garbage"
    if "no_separator_context" in score.get("negative_features", []):
        return "weak_noisy"
    return "inconclusive"


def _recommendation(label: str) -> str:
    if label in {"weak_noisy", "obviously_garbage", "inconclusive"}:
        return "Queue reverse-direction Caesar plus affine and keep refined scoring."
    return "Inspect refined top lead before widening the queue."


def _warnings(top_candidate: dict[str, Any], diagnostics: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    if diagnostics["space_count"] == 0 and diagnostics["separator_count"] == 0:
        warnings.append("top_candidate_has_no_separator_or_space_context")
    if not top_candidate.get("score_summary", {}).get("common_word_hits"):
        warnings.append("top_candidate_has_no_common_word_hits")
    return warnings
