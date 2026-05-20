"""Build Stage 5A CUDA target-plan records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import write_json, write_yaml
from libreprimus.cuda_planning.loaders import (
    load_stage4o_parity_expectations,
    load_stage4p_unified_results,
    load_stage4q_readiness,
)
from libreprimus.cuda_planning.models import (
    CUDA_PLANNING_POLICY,
    NON_TARGETS_PATH,
    NON_TARGETS_REPORT,
    STAGE5A_OUTPUT_DIR,
    TARGET_PLAN_PATH,
    TARGET_PLAN_REPORT,
)
from libreprimus.cuda_planning.non_targets import build_non_target_records

FAMILY_ALIASES = {
    "p56_prime_minus_one": "prime_minus_one_stream",
    "vigenere": "vigenere_explicit_key",
}


def build_target_plan(
    *,
    out_dir: Path = STAGE5A_OUTPUT_DIR,
    target_plan_out: Path = TARGET_PLAN_PATH,
    non_targets_out: Path = NON_TARGETS_PATH,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Build target records from Stage 4Q readiness records."""

    parity_by_family = _records_by_family(load_stage4o_parity_expectations())
    unified_by_parity = {
        str(record.get("parity_expectation_id")): str(record.get("unified_result_id"))
        for record in load_stage4p_unified_results()
        if record.get("parity_expectation_id")
    }
    target_records = [
        _target_record(record, parity_by_family, unified_by_parity)
        for record in load_stage4q_readiness()
    ]
    target_records.sort(key=lambda item: str(item["target_id"]))
    non_targets = build_non_target_records()
    write_yaml(target_plan_out, {"records": target_records})
    write_yaml(non_targets_out, {"records": non_targets})
    write_json(out_dir / TARGET_PLAN_REPORT, {"records": target_records})
    write_json(out_dir / NON_TARGETS_REPORT, {"records": non_targets})
    return target_records, non_targets


def _records_by_family(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    by_family: dict[str, dict[str, Any]] = {}
    for record in records:
        family = str(record.get("transform_family", ""))
        if family and family not in by_family:
            by_family[family] = record
    return by_family


def _target_record(
    readiness: dict[str, Any],
    parity_by_family: dict[str, dict[str, Any]],
    unified_by_parity: dict[str, str],
) -> dict[str, Any]:
    family = str(readiness.get("transform_family") or readiness.get("transform_id") or "unknown")
    target_status = _target_status(str(readiness.get("parity_gate_status")), str(readiness.get("adapter_status")))
    parity_family = FAMILY_ALIASES.get(family, family)
    parity = parity_by_family.get(parity_family, {})
    parity_id = str(parity.get("candidate_id", ""))
    blockers = list(readiness.get("blockers", []))
    if target_status == "ready_for_planning" and not parity_id:
        target_status = "blocked_needs_parity_fixture"
        blockers = [*blockers, "missing_stage4o_parity_expectation_reference"]
    record: dict[str, Any] = {
        "record_type": "cuda_target_plan",
        "stage_id": "stage-5a",
        "target_id": f"stage5a-{family}-cuda-target",
        "source_readiness_id": readiness.get("readiness_id"),
        "transform_id": readiness.get("transform_id"),
        "canonical_transform_id": readiness.get("canonical_transform_id"),
        "transform_family": family,
        "target_status": target_status,
        "blockers": blockers,
        "cpu_reference_path": "python/libreprimus/cpu_batch/",
        "score_summary_contract": "stage4i",
        "stage4q_readiness_status": readiness.get("parity_gate_status"),
        "stage4o_parity_expectation_id": parity_id,
        "stage4p_unified_result_reference": unified_by_parity.get(parity_id, ""),
        "output_text_hash": parity.get("output_text_hash", ""),
        "output_token_hash": parity.get("output_token_hash", ""),
        "score_summary_shape_hash": parity.get("score_summary_shape_hash", ""),
        "parity_contract_version": parity.get("parity_contract_version", "stage4o-cpu-cuda-parity-v0"),
        "no_raw_data_required": True,
        "broad_campaign_required": False,
        "notes": [
            "Stage 5A target planning only; future implementation requires an explicit later stage.",
        ],
        **CUDA_PLANNING_POLICY,
    }
    return record


def _target_status(parity_gate_status: str, adapter_status: str) -> str:
    if parity_gate_status == "ready_for_future_cuda_planning":
        return "ready_for_planning"
    if parity_gate_status == "skipped_not_cuda_target" or adapter_status == "unsupported_by_design":
        return "non_cuda_target"
    if "score" in parity_gate_status:
        return "blocked_needs_score_summary_contract"
    if "parity" in parity_gate_status or "fixture" in parity_gate_status:
        return "blocked_needs_parity_fixture"
    return "blocked_needs_cpu_adapter"
