"""Build Stage 5O result-store preflight records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import resolve_repo_path
from libreprimus.gematria_solved_fixture_cuda_repeat.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_solved_fixture_cuda_repeat.models import (
    COMMON_POLICY_FLAGS,
    OUTPUT_DIR,
    REPEAT_PARITY_PATH,
    RESULT_STORE_CONTRACT,
    RESULT_STORE_PREFLIGHT_PATH,
    RESULT_STORE_PREFLIGHT_REPORT,
    SCORE_SUMMARY_CONTRACT,
    STAGE4P_SUMMARY,
)


def build_result_store_preflight(
    *,
    repeat_parity: Path = REPEAT_PARITY_PATH,
    stage4p_summary: Path = STAGE4P_SUMMARY,
    result_store_preflight_out: Path = RESULT_STORE_PREFLIGHT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    parity = read_record_set(repeat_parity)
    pass_count = sum(1 for record in parity if record["repeat_parity_status"] == "passed")
    stage4p_present = resolve_repo_path(stage4p_summary).is_file()
    ready = pass_count == 5 and stage4p_present
    records = [
        _record(
            record_id="stage5o-result-store-compact-summary-00",
            preflight_kind="compact_summary_integration",
            preflight_status="ready_for_stage5p_compact_summary_integration" if ready else "blocked_repeat_parity_or_stage4p_missing",
            stage4p_summary=stage4p_summary,
            stage4p_present=stage4p_present,
            repeat_parity_pass_count=pass_count,
            stage5p_ready=ready,
        ),
        _record(
            record_id="stage5o-result-store-generated-body-policy-00",
            preflight_kind="generated_body_publication_policy",
            preflight_status="blocked_generated_body_publication",
            stage4p_summary=stage4p_summary,
            stage4p_present=stage4p_present,
            repeat_parity_pass_count=pass_count,
            stage5p_ready=False,
        ),
        _record(
            record_id="stage5o-result-store-unsolved-scope-00",
            preflight_kind="unsolved_cuda_scope_policy",
            preflight_status="blocked_unsolved_scope",
            stage4p_summary=stage4p_summary,
            stage4p_present=stage4p_present,
            repeat_parity_pass_count=pass_count,
            stage5p_ready=False,
        ),
    ]
    write_record_set(result_store_preflight_out, records)
    write_report(out_dir, RESULT_STORE_PREFLIGHT_REPORT, {"records": records})
    return records


def _record(
    *,
    record_id: str,
    preflight_kind: str,
    preflight_status: str,
    stage4p_summary: Path,
    stage4p_present: bool,
    repeat_parity_pass_count: int,
    stage5p_ready: bool,
) -> dict[str, Any]:
    record = {
        "record_type": "stage5o_gematria_cuda_result_store_preflight_record",
        "preflight_record_id": record_id,
        "preflight_kind": preflight_kind,
        "preflight_status": preflight_status,
        "result_source_kind": "stage5o_solved_fixture_cuda_repeat_parity",
        "result_store_contract": RESULT_STORE_CONTRACT,
        "score_summary_contract": SCORE_SUMMARY_CONTRACT,
        "stage4p_summary_path": str(stage4p_summary),
        "stage4p_summary_present": stage4p_present,
        "repeat_parity_pass_count": repeat_parity_pass_count,
        "expected_repeat_parity_pass_count": 5,
        "output_token_hash_required": True,
        "generated_result_bodies_committed": False,
        "generated_result_body_publication_allowed": False,
        "compact_summary_only": True,
        "method_status_upgrade_allowed": False,
        "stage5p_ready": stage5p_ready,
        "cuda_execution_performed": False,
        "solved_fixture_cuda_used": False,
        "additional_cuda_execution_performed": False,
    }
    record.update(COMMON_POLICY_FLAGS)
    return record
