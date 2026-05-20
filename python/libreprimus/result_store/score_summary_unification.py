"""Stage 4P score-summary compatibility views."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cpu_batch.input_streams import stable_json_sha256
from libreprimus.result_store.normalization import build_unified_result_records
from libreprimus.result_store.stage4p_export import read_jsonl, resolve_repo_path, write_jsonl
from libreprimus.result_store.unified_models import (
    STAGE4P_OUTPUT_DIR,
    UNIFIED_SCORE_JSONL,
)
from libreprimus.scoring_consolidation.cpu_batch_integration import score_summary_from_cpu_batch_result


def build_unified_score_summaries(
    manifest_path: Path,
    *,
    out_dir: Path = STAGE4P_OUTPUT_DIR,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Write unified result and score-summary records."""

    resolved_out = resolve_repo_path(out_dir)
    _, result_records, warnings = build_unified_result_records(manifest_path, out_dir=out_dir)
    score_records = [_score_record_from_result(record) for record in result_records]
    score_records = sorted(score_records, key=lambda item: str(item["unified_score_id"]))
    write_jsonl(resolved_out / UNIFIED_SCORE_JSONL, score_records)
    return score_records, warnings


def _score_record_from_result(result: dict[str, Any]) -> dict[str, Any]:
    if (
        result.get("result_source_kind") == "cpu_batch_result"
        and result.get("source_record_type") == "cpu_batch_result_record"
        and result.get("source_presence_status") == "local_generated_present"
    ):
        payload = _raw_cpu_batch_payload(result)
        if payload:
            score = score_summary_from_cpu_batch_result(payload)
            return _wrap_score(result, score, [])
    return _wrap_score(
        result,
        {
            "score_status": "scoring_not_available",
            "confidence_label": "scoring_not_available",
            "score_components": {},
        },
        ["No Stage 4I-compatible score payload is available for this result surface."],
    )


def _raw_cpu_batch_payload(result: dict[str, Any]) -> dict[str, Any] | None:
    source = resolve_repo_path(Path(str(result["source_path"])))
    index = int(result.get("source_payload_index", 0))
    records = read_jsonl(source)
    if index >= len(records):
        return None
    return records[index]


def _wrap_score(
    result: dict[str, Any],
    score: dict[str, Any],
    warnings: list[str],
) -> dict[str, Any]:
    score_status = str(score.get("score_status", "scoring_not_available"))
    confidence_label = str(score.get("confidence_label", "scoring_not_available"))
    score_id = "stage4p-score-" + stable_json_sha256(
        [result.get("unified_result_id"), score_status, confidence_label]
    )[:20]
    record = {
        "record_type": "unified_score_summary_record",
        "unified_score_id": score_id,
        "unified_result_id": result.get("unified_result_id"),
        "source_stage_id": result.get("source_stage_id"),
        "source_path": result.get("source_path"),
        "result_source_kind": result.get("result_source_kind"),
        "input_stream_id": score.get("input_stream_id", result.get("input_stream_id", "unknown")),
        "candidate_id": score.get("candidate_id", result.get("candidate_id", "unknown")),
        "transform_family": score.get("transform_family", result.get("transform_family", "unknown")),
        "score_status": score_status
        if score_status in {"scored", "scoring_not_available", "calibration_not_available", "scorer_error"}
        else "scoring_not_available",
        "score_value": score.get("score_value"),
        "score_components": score.get("score_components", {}),
        "calibration_profile_id": score.get("calibration_profile_id"),
        "confidence_label": confidence_label
        if confidence_label
        in {
            "positive_control_like",
            "plausible_lead",
            "weak_lead",
            "noisy",
            "inconclusive",
            "garbage",
            "negative_control_like",
            "scoring_not_available",
            "calibration_not_available",
        }
        else "scoring_not_available",
        "score_interpretation": "triage_only",
        "no_solve_claim": True,
        "solve_claim": False,
        "cuda_used": False,
        "new_scorer_added": False,
        "warnings": warnings,
    }
    return {key: value for key, value in record.items() if value is not None}
