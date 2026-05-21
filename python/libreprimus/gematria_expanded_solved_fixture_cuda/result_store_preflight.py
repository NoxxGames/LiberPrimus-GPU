"""Build Stage 5R result-store preflight records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import resolve_repo_path
from libreprimus.gematria_expanded_solved_fixture_cuda.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_expanded_solved_fixture_cuda.models import (
    COMMON_POLICY_FLAGS,
    HASH_ALGORITHM,
    OUTPUT_DIR,
    PARITY_RECORDS_PATH,
    RESULT_STORE_CONTRACT,
    RESULT_STORE_PREFLIGHT_PATH,
    RESULT_STORE_PREFLIGHT_REPORT,
    SCORE_SUMMARY_CONTRACT,
    STAGE4P_SUMMARY,
)
from libreprimus.paths import repo_root


def build_result_store_preflight(
    *,
    parity_records: Path = PARITY_RECORDS_PATH,
    stage4p_summary: Path = STAGE4P_SUMMARY,
    result_store_preflight_out: Path = RESULT_STORE_PREFLIGHT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    parity = read_record_set(parity_records)
    stage4p_present = resolve_repo_path(stage4p_summary).is_file()
    records = [
        _record(index=index, parity=record, stage4p_summary=stage4p_summary, stage4p_present=stage4p_present)
        for index, record in enumerate(sorted(parity, key=lambda item: str(item["parity_record_id"])))
    ]
    write_record_set(result_store_preflight_out, records)
    write_report(out_dir, RESULT_STORE_PREFLIGHT_REPORT, {"records": records})
    return records


def _record(*, index: int, parity: dict[str, Any], stage4p_summary: Path, stage4p_present: bool) -> dict[str, Any]:
    ready = parity["parity_status"] == "passed" and stage4p_present
    record = {
        "record_type": "gematria_expanded_solved_fixture_result_store_preflight_record",
        "result_store_preflight_id": f"stage5r-result-store-preflight-{index:02d}",
        "parity_record_id": parity["parity_record_id"],
        "fixture_id": parity["fixture_id"],
        "candidate_id": parity["candidate_id"],
        "source_input_stream_id": parity["source_input_stream_id"],
        "result_source": "expanded_solved_fixture_safe_cuda_parity",
        "result_source_kind": "expanded_solved_fixture_safe_cuda_parity",
        "result_store_contract": RESULT_STORE_CONTRACT,
        "score_summary_contract": SCORE_SUMMARY_CONTRACT,
        "stage4p_summary_path": _repo_relative(stage4p_summary),
        "stage4p_summary_present": stage4p_present,
        "stage4p_compatibility": stage4p_present,
        "stage4i_compatibility": True,
        "output_token_hash_required": True,
        "output_token_hash": parity.get("stage5r_cuda_output_token_hash"),
        "output_hash_algorithm": HASH_ALGORITHM,
        "output_text_hash_optional_until_transliteration_policy": True,
        "generated_output_bodies_ignored": True,
        "generated_result_bodies_committed": False,
        "generated_body_publication_allowed": False,
        "compact_summary_only": True,
        "method_status_upgrade_allowed": False,
        "preflight_status": "ready_for_stage5s_result_store_integration" if ready else "blocked_parity_or_stage4p_missing",
        "stage5s_ready": ready,
        "blockers": [] if ready else ["stage5r_parity_not_passed_or_stage4p_missing"],
        "blocker_count": 0 if ready else 1,
        "cuda_execution_performed": parity["cuda_execution_performed"],
        "solved_fixture_cuda_used": parity["solved_fixture_cuda_used"],
    }
    record.update(COMMON_POLICY_FLAGS)
    record["cuda_execution_performed"] = parity["cuda_execution_performed"]
    record["solved_fixture_cuda_used"] = parity["solved_fixture_cuda_used"]
    return record


def _repo_relative(path: Path) -> str:
    resolved = resolve_repo_path(path)
    try:
        return resolved.relative_to(repo_root()).as_posix()
    except ValueError:
        return path.as_posix()
