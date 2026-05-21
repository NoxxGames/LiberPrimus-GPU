"""Score-summary preflight records for future solved-fixture-safe Gematria CUDA output."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml
from libreprimus.gematria_cuda_parity_reporting.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_cuda_parity_reporting.models import (
    COMMON_POLICY_FLAGS,
    OUTPUT_DIR,
    SCORE_PREFLIGHT_JSON,
    SCORE_PREFLIGHT_PATH,
    STAGE4I_LABELS_PATH,
    STAGE5H_SCORE_PLAN_PATH,
)

SCORE_STATUS_VALUES = ("scored", "scoring_not_available", "calibration_not_available", "scorer_error")


def build_score_summary_preflight(
    *,
    score_plan_path: Path = STAGE5H_SCORE_PLAN_PATH,
    labels_path: Path = STAGE4I_LABELS_PATH,
    score_preflight_out: Path = SCORE_PREFLIGHT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    score_plan_records = read_record_set(score_plan_path)
    score_plan = score_plan_records[0] if score_plan_records else {}
    label_payload = read_yaml(labels_path)
    labels = [str(record.get("label")) for record in label_payload.get("records", []) if isinstance(record, dict)]
    record: dict[str, Any] = {
        "record_type": "gematria_cuda_score_summary_preflight_record",
        "score_summary_preflight_id": "stage5k-gematria-cuda-score-summary-preflight-v0",
        "score_plan_path": str(score_plan_path),
        "confidence_label_source": str(labels_path),
        "score_summary_contract": "stage4i",
        "score_interpretation": "triage_only",
        "required_output_token_hash": True,
        "output_text_hash_policy": str(score_plan.get("output_text_hash_policy", "optional_after_transliteration_policy_exists")),
        "score_status_values": list(SCORE_STATUS_VALUES),
        "allowed_confidence_labels": labels,
        "confidence_labels_triage_only": True,
        "future_cuda_output_requirements": [
            "compare CUDA output_token_hash against CPU/native output_token_hash",
            "cite Stage 4O parity expectation where available",
            "record scoring_not_available instead of inventing score semantics",
        ],
        "notes": [
            "Stage 5K adds no new scorer and does not reinterpret confidence labels as solve evidence.",
            "Output text hashes remain optional until transliteration policy is explicit.",
        ],
        **COMMON_POLICY_FLAGS,
    }
    records = [record]
    write_record_set(score_preflight_out, records)
    write_report(out_dir, SCORE_PREFLIGHT_JSON, {"records": records})
    return records
