"""Build Stage 5A CUDA parity scaffold records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import read_yaml, write_json, write_yaml
from libreprimus.cuda_planning.models import (
    CUDA_PLANNING_POLICY,
    PARITY_SCAFFOLD_PATH,
    PARITY_SCAFFOLD_REPORT,
    STAGE5A_OUTPUT_DIR,
    TARGET_PLAN_PATH,
)


def build_parity_scaffold(
    *,
    out_dir: Path = STAGE5A_OUTPUT_DIR,
    target_plan_path: Path = TARGET_PLAN_PATH,
    parity_scaffold_out: Path = PARITY_SCAFFOLD_PATH,
) -> list[dict[str, Any]]:
    targets = list(read_yaml(target_plan_path).get("records", []))
    records = [_scaffold_record(target) for target in targets if target.get("target_status") == "ready_for_planning"]
    records.sort(key=lambda item: str(item["scaffold_id"]))
    write_yaml(parity_scaffold_out, {"records": records})
    write_json(out_dir / PARITY_SCAFFOLD_REPORT, {"records": records})
    return records


def _scaffold_record(target: dict[str, Any]) -> dict[str, Any]:
    target_id = str(target["target_id"])
    required_hash_checks = ["output_token_hash"]
    if target.get("output_text_hash"):
        required_hash_checks.append("output_text_hash")
    if target.get("score_summary_shape_hash"):
        required_hash_checks.append("score_summary_shape_hash")
    return {
        "record_type": "cuda_parity_scaffold",
        "stage_id": "stage-5a",
        "scaffold_id": f"{target_id}-parity-scaffold",
        "target_id": target_id,
        "transform_family": target.get("transform_family"),
        "cpu_reference_path": target.get("cpu_reference_path", "python/libreprimus/cpu_batch/"),
        "fixture_source_stream": target.get("stage4o_parity_expectation_id", ""),
        "stage4o_parity_expectation_id": target.get("stage4o_parity_expectation_id", ""),
        "stage4p_unified_result_reference": target.get("stage4p_unified_result_reference", ""),
        "output_text_hash": target.get("output_text_hash", ""),
        "output_token_hash": target.get("output_token_hash", ""),
        "score_summary_shape_hash": target.get("score_summary_shape_hash", ""),
        "required_hash_checks": required_hash_checks,
        "score_summary_parity_required": True,
        "separator_behavior_requirement": "Must match Stage 4O separator behavior exactly.",
        "line_reset_behavior_requirement": "Must match Stage 4O line/reset behavior exactly.",
        "unknown_token_behavior_requirement": "Must match Stage 4O unknown-token handling exactly.",
        "expected_failure_mode": "fail_closed_on_hash_or_score_shape_mismatch",
        "future_test_name": f"test_stage5b_{target.get('transform_family')}_cpu_gpu_parity",
        "parity_scaffold_status": "planned",
        "execution_enabled": False,
        "cuda_execution_performed": False,
        **CUDA_PLANNING_POLICY,
    }
