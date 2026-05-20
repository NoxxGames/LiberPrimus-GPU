"""Select the first future CUDA kernel contract candidate."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import resolve_repo_path
from libreprimus.cuda_kernel_contract.export import write_records_yaml, write_report, write_warnings
from libreprimus.cuda_kernel_contract.loaders import load_mapping, load_records, optional_file_present
from libreprimus.cuda_kernel_contract.models import (
    ADAPTER_SELECTION_ID,
    ADAPTER_SELECTION_PATH,
    ADAPTER_SELECTION_REPORT,
    COMMON_GUARDRAILS,
    CONTRACT_ID,
    CONTRACT_PATH,
    CONTRACT_REPORT,
    OUTPUT_DIR,
    SELECTED_ADAPTER_FAMILY,
    SELECTED_KERNEL_ID,
    SELECTED_TARGET_ID,
    SELECTED_TRANSFORM_FAMILY,
    STAGE4O_SUMMARY_PATH,
    STAGE4P_SUMMARY_PATH,
    STAGE5A_IMPLEMENTATION_GATES_PATH,
    STAGE5A_TARGET_PLAN_PATH,
    STAGE5B_FIXTURES_PATH,
    STAGE5B_HARNESS_PATH,
    STAGE5B_MATRIX_PATH,
    STAGE_ID,
)


def select_first_kernel_contract(
    *,
    target_plan_path: Path = STAGE5A_TARGET_PLAN_PATH,
    implementation_gates_path: Path = STAGE5A_IMPLEMENTATION_GATES_PATH,
    harness_path: Path = STAGE5B_HARNESS_PATH,
    fixtures_path: Path = STAGE5B_FIXTURES_PATH,
    matrix_path: Path = STAGE5B_MATRIX_PATH,
    stage4o_summary_path: Path = STAGE4O_SUMMARY_PATH,
    stage4p_summary_path: Path = STAGE4P_SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
    contract_out: Path = CONTRACT_PATH,
    adapter_selection_out: Path = ADAPTER_SELECTION_PATH,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    targets = load_records(target_plan_path)
    gates = load_records(implementation_gates_path)
    harness = load_records(harness_path)
    fixtures = load_records(fixtures_path)
    matrix = load_records(matrix_path)
    stage4o = load_mapping(stage4o_summary_path)
    stage4p = load_mapping(stage4p_summary_path)

    selected_target = _find(targets, "target_id", SELECTED_TARGET_ID)
    selected_matrix = _find(matrix, "kernel_id", SELECTED_KERNEL_ID)
    selected_harness = _find(harness, "stage5a_target_id", SELECTED_TARGET_ID)
    selected_fixture = _find(fixtures, "stage5a_target_id", SELECTED_TARGET_ID)
    if not selected_target or not selected_matrix or not selected_harness or not selected_fixture:
        raise ValueError("Stage 5E selected shift-score candidate is missing required committed records")

    satisfied_gates = sorted(str(record.get("gate_id")) for record in gates if record.get("implementation_gate_status") == "satisfied")
    alternate_candidates, blocked_or_rejected = _classify_candidates(targets, matrix, harness)
    contract = {
        "record_type": "cuda_first_kernel_contract_record",
        "stage_id": STAGE_ID,
        "contract_id": CONTRACT_ID,
        "selected_kernel_id": SELECTED_KERNEL_ID,
        "selected_target_id": SELECTED_TARGET_ID,
        "selected_transform_family": SELECTED_TRANSFORM_FAMILY,
        "selected_adapter_family": SELECTED_ADAPTER_FAMILY,
        "selection_status": "selected_for_stage5f_synthetic_only_contract",
        "selection_reason": (
            "Selected caesar_mod29 shift-score because it is the simplest regular planned target "
            "with Stage 5A gates satisfied, Stage 5B ready harness/fixture rows, Stage 4O parity "
            "hashes, Stage 4P unified result references, and Stage 5D native synthetic shift parity."
        ),
        "stage5a_target_status": selected_target.get("target_status"),
        "stage5b_future_kernel_status": selected_matrix.get("future_kernel_status"),
        "stage5b_harness_status": selected_harness.get("harness_status"),
        "stage5b_fixture_status": selected_fixture.get("fixture_status"),
        "stage5a_satisfied_gates": satisfied_gates,
        "stage4o_parity_expectation_reference": selected_harness.get("stage4o_parity_expectation_reference"),
        "stage4p_unified_result_reference": selected_harness.get("stage4p_unified_result_reference"),
        "stage4o_summary_present": optional_file_present(stage4o_summary_path),
        "stage4p_summary_present": optional_file_present(stage4p_summary_path),
        "stage4o_parity_expectations_written": int(stage4o.get("parity_expectations_written", 0)),
        "stage4p_records_with_parity_expectations": int(stage4p.get("records_with_parity_expectations", 0)),
        "output_text_hash": selected_fixture.get("output_text_hash", ""),
        "output_token_hash": selected_fixture.get("output_token_hash", ""),
        "score_summary_shape_hash": selected_fixture.get("score_summary_shape_hash", ""),
        "vram_profile": selected_fixture.get("vram_profile", "compatibility_8gb"),
        "local_16gb_profile_optional": True,
        "compatibility_8gb_profile_required": True,
        "no_gpu_ci_profile_preserved": True,
        "alternate_candidates": alternate_candidates,
        "blocked_or_rejected_candidates": blocked_or_rejected,
        **COMMON_GUARDRAILS,
    }
    adapter_selection = {
        "record_type": "cuda_adapter_selection_record",
        "stage_id": STAGE_ID,
        "selection_id": ADAPTER_SELECTION_ID,
        "contract_id": CONTRACT_ID,
        "selected_kernel_id": SELECTED_KERNEL_ID,
        "selected_adapter_family": SELECTED_ADAPTER_FAMILY,
        "selected_transform_family": SELECTED_TRANSFORM_FAMILY,
        "cpu_reference_family": str(selected_matrix.get("cpu_reference_family", SELECTED_TRANSFORM_FAMILY)),
        "native_reference_family": "stage5d_native_synthetic_shift",
        "adapter_selection_status": "selected",
        "adapter_scope": "synthetic-only shift/score parity contract for a later explicit Stage 5F implementation",
        "stage5d_reference_required": True,
        "stage5d_reference_semantics": "deterministic native CPU synthetic Caesar-style shift fixture",
        "selection_reason": "Matches the Stage 5D native synthetic shift fixture without requiring raw data, broad search, or GPU execution.",
        **COMMON_GUARDRAILS,
    }
    resolved_out = resolve_repo_path(out_dir)
    resolved_out.mkdir(parents=True, exist_ok=True)
    write_records_yaml(contract_out, [contract])
    write_records_yaml(adapter_selection_out, [adapter_selection])
    write_report(out_dir / CONTRACT_REPORT, {"records": [contract]})
    write_report(out_dir / ADAPTER_SELECTION_REPORT, {"records": [adapter_selection]})
    write_warnings(out_dir, [])
    return [contract], [adapter_selection]


def _find(records: list[dict[str, Any]], key: str, value: str) -> dict[str, Any] | None:
    for record in records:
        if record.get(key) == value:
            return record
    return None


def _classify_candidates(
    targets: list[dict[str, Any]],
    matrix: list[dict[str, Any]],
    harness: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    matrix_by_family = {record.get("cpu_reference_family"): record for record in matrix}
    harness_by_target = {record.get("stage5a_target_id"): record for record in harness}
    alternates: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []
    for target in sorted(targets, key=lambda item: str(item.get("target_id"))):
        target_id = str(target.get("target_id"))
        family = str(target.get("transform_family"))
        if target_id == SELECTED_TARGET_ID:
            continue
        matrix_record = matrix_by_family.get(family)
        harness_record = harness_by_target.get(target_id)
        status = str(target.get("target_status"))
        if status == "ready_for_planning" and matrix_record and matrix_record.get("future_kernel_status") == "planned":
            alternates.append(
                {
                    "target_id": target_id,
                    "transform_family": family,
                    "kernel_id": matrix_record.get("kernel_id"),
                    "reason_not_selected": "Ready alternate, but less minimal than caesar_mod29 shift-score for the first synthetic-only kernel contract.",
                }
            )
        else:
            reasons = list(target.get("blockers") or [])
            if matrix_record and matrix_record.get("future_kernel_status") == "blocked":
                reasons.append("future_kernel_matrix_blocked")
            if harness_record and harness_record.get("harness_status") != "ready_for_future_kernel":
                reasons.extend(harness_record.get("blocked_conditions") or [])
            if not reasons:
                reasons.append("not_selected_for_first_kernel_contract")
            blocked.append(
                {
                    "target_id": target_id,
                    "transform_family": family,
                    "target_status": status,
                    "reasons": sorted({str(reason) for reason in reasons}),
                }
            )
    return alternates, blocked
