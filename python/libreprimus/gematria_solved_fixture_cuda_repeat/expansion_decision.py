"""Build the Stage 5O expansion decision record."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_solved_fixture_cuda_repeat.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_solved_fixture_cuda_repeat.models import (
    COMMON_POLICY_FLAGS,
    EXPANSION_DECISION_PATH,
    EXPANSION_DECISION_REPORT,
    NEXT_STAGE_MISMATCH,
    NEXT_STAGE_PREFLIGHT,
    NEXT_STAGE_READY,
    NEXT_STAGE_TOOLCHAIN,
    OUTPUT_DIR,
    REPEAT_PARITY_PATH,
    RESULT_STORE_PREFLIGHT_PATH,
    SCORE_SUMMARY_PREFLIGHT_PATH,
)


def build_expansion_decision(
    *,
    repeat_parity: Path = REPEAT_PARITY_PATH,
    result_store_preflight: Path = RESULT_STORE_PREFLIGHT_PATH,
    score_summary_preflight: Path = SCORE_SUMMARY_PREFLIGHT_PATH,
    expansion_decision_out: Path = EXPANSION_DECISION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    parity = read_record_set(repeat_parity)
    result_store = read_record_set(result_store_preflight)
    score = read_record_set(score_summary_preflight)
    pass_count = sum(1 for record in parity if record["repeat_parity_status"] == "passed")
    fail_count = sum(1 for record in parity if str(record["repeat_parity_status"]).startswith("failed"))
    skip_count = len(parity) - pass_count - fail_count
    result_store_ready = any(record.get("stage5p_ready") is True for record in result_store)
    score_ready = any(record.get("stage5p_ready") is True for record in score)
    decision_status, next_stage, reason, blockers = _decision(
        pass_count=pass_count,
        fail_count=fail_count,
        skip_count=skip_count,
        result_store_ready=result_store_ready,
        score_ready=score_ready,
    )
    record = {
        "record_type": "gematria_cuda_expansion_decision_record",
        "expansion_decision_id": "stage5o-expansion-decision-00",
        "decision_status": decision_status,
        "repeat_parity_pass_count": pass_count,
        "repeat_parity_fail_count": fail_count,
        "repeat_parity_skip_count": skip_count,
        "result_store_preflight_ready": result_store_ready,
        "score_summary_preflight_ready": score_ready,
        "stage5p_ready": decision_status == "stage5p_ready",
        "selected_next_stage": next_stage,
        "selected_next_stage_reason": reason,
        "remaining_blockers": blockers,
        "approved_expansion_scope": "compact_result_store_preflight_only" if decision_status == "stage5p_ready" else "none",
        "broad_solved_fixture_cuda_allowed": False,
        "unsolved_page_cuda_allowed": False,
        "gpu_benchmark_allowed": False,
        "cuda_execution_performed": False,
        "solved_fixture_cuda_used": False,
        "additional_cuda_execution_performed": False,
    }
    record.update(COMMON_POLICY_FLAGS)
    records = [record]
    write_record_set(expansion_decision_out, records)
    write_report(out_dir, EXPANSION_DECISION_REPORT, {"records": records})
    return records


def _decision(
    *,
    pass_count: int,
    fail_count: int,
    skip_count: int,
    result_store_ready: bool,
    score_ready: bool,
) -> tuple[str, str, str, list[str]]:
    if fail_count:
        return (
            "repeat_hash_mismatch_investigation_required",
            NEXT_STAGE_MISMATCH,
            "At least one Stage 5O repeat parity record failed.",
            ["stage5o_repeat_hash_mismatch_or_cuda_run_failure"],
        )
    if skip_count:
        return (
            "repeat_verification_followup_required",
            NEXT_STAGE_TOOLCHAIN,
            "CUDA repeat verification did not run for every exact Stage 5M fixture.",
            ["stage5o_repeat_cuda_not_fully_executed"],
        )
    if pass_count == 5 and result_store_ready and score_ready:
        return (
            "stage5p_ready",
            NEXT_STAGE_READY,
            "All five exact repeat hashes match Stage 5L native and Stage 5M CUDA hashes, and compact preflight is ready.",
            [],
        )
    return (
        "preflight_followup_required",
        NEXT_STAGE_PREFLIGHT,
        "Repeat parity is clean but result-store or score-summary preflight is not ready.",
        ["stage5o_result_store_or_score_summary_preflight_not_ready"],
    )
