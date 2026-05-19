"""Compatibility helpers between Stage 4H CPU batch output and Stage 4I scoring."""

from __future__ import annotations

from typing import Any

import yaml

from libreprimus.paths import repo_root
from libreprimus.scoring_consolidation.confidence_labels import map_legacy_label
from libreprimus.scoring_consolidation.models import CALIBRATION_PROFILE_ID, SCORER_ID, SCORER_VERSION


def score_summary_from_cpu_batch_result(record: dict[str, Any]) -> dict[str, Any]:
    """Convert one CPU batch result record into the Stage 4I score-summary shape."""

    score = dict(record.get("score_summary") or {})
    status = str(score.get("score_status", "scoring_not_available"))
    if status == "scoring_disabled":
        status = "scoring_not_available"
    label = map_legacy_label(str(score.get("confidence_label", status)))
    if status != "scored" and label not in {"scoring_not_available", "calibration_not_available"}:
        label = "scoring_not_available"
    record_out = {
        "record_type": "score_summary_record",
        "scorer_id": str(score.get("scorer_id", SCORER_ID)),
        "scorer_version": str(score.get("scorer_version", SCORER_VERSION)),
        "input_stream_id": str(record.get("input_stream_id", "unknown")),
        "candidate_id": str(record.get("candidate_id", "unknown")),
        "transform_family": str(record.get("transform_family", "unknown")),
        "score_status": status if status in {"scored", "scoring_not_available", "calibration_not_available", "scorer_error"} else "scoring_not_available",
        "score_value": score.get("length_normalized_score", score.get("total_score")),
        "score_components": _score_components(score),
        "calibration_profile_id": str(score.get("calibration_profile_id", CALIBRATION_PROFILE_ID)),
        "confidence_label": label,
        "null_percentile": score.get("null_percentile"),
        "positive_control_distance": score.get("positive_control_distance"),
        "negative_control_distance": score.get("negative_control_distance"),
        "crib_hits": list(score.get("crib_hits", [])),
        "notes": ["CPU batch score summary compatibility view; scoring remains triage only."],
        "solve_claim": False,
        "trusted_as_canonical": False,
        "cuda_used": False,
    }
    return {key: value for key, value in record_out.items() if value is not None}


def check_cpu_batch_summary(summary_path: str | None = None) -> dict[str, Any]:
    """Check that the committed Stage 4H summary can reference Stage 4I scoring."""

    path = repo_root() / (summary_path or "data/research/stage4h-cpu-batch-api-summary.yaml")
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) if path.is_file() else {}
    cpu_summary = payload.get("cpu_batch_summary", {}) if isinstance(payload, dict) else {}
    scoring_available = int(cpu_summary.get("scoring_available_count", 0))
    scoring_unavailable = int(cpu_summary.get("scoring_unavailable_count", 0))
    required_fields = set(payload.get("parity_contract", {}).get("required_result_fields", [])) if isinstance(payload, dict) else set()
    missing_required = sorted({"score_summary", "output_text_hash", "output_token_hash"} - required_fields)
    compatible = scoring_available >= 0 and not missing_required
    return {
        "record_type": "cpu_batch_score_compatibility",
        "cpu_batch_summary": str(path.relative_to(repo_root())) if path.is_file() else str(path),
        "scoring_available_count": scoring_available,
        "scoring_unavailable_count": scoring_unavailable,
        "required_field_missing": missing_required,
        "compatible": compatible,
        "notes": ["Stage 4H result records carry score_summary and output hashes required for score parity."],
        "solve_claim": False,
        "cuda_used": False,
    }


def _score_components(score: dict[str, Any]) -> dict[str, Any]:
    return {
        key: score[key]
        for key in (
            "total_score",
            "length_normalized_score",
            "common_word_hit_count",
            "vowel_ratio",
            "entropy",
            "positive_features",
            "negative_features",
        )
        if key in score
    }
