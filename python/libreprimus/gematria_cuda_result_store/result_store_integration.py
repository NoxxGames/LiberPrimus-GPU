"""Build Stage 5P compact result-store integration records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import resolve_repo_path
from libreprimus.gematria_cuda_result_store.export import write_record_set, write_report, write_warnings
from libreprimus.gematria_cuda_result_store.loaders import load_stage5o_repeat_parity
from libreprimus.gematria_cuda_result_store.models import (
    COMMON_POLICY_FLAGS,
    HASH_ALGORITHM,
    OUTPUT_DIR,
    RESULT_STORE_INTEGRATION_PATH,
    RESULT_STORE_INTEGRATION_REPORT,
    RESULT_STORE_CONTRACT,
    SCORE_SUMMARY_CONTRACT,
    STAGE4P_SUMMARY,
    STAGE5O_REPEAT_PARITY,
)


def build_result_store_integration(
    *,
    repeat_parity: Path = STAGE5O_REPEAT_PARITY,
    result_store_integration_out: Path = RESULT_STORE_INTEGRATION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Build compact Stage 4P-compatible records from Stage 5O repeat parity."""

    parity_records = load_stage5o_repeat_parity(repeat_parity)
    source_path = _repo_relative_path(repeat_parity)
    records: list[dict[str, Any]] = []
    for index, parity in enumerate(sorted(parity_records, key=lambda item: str(item["repeat_parity_record_id"]))):
        integration_id = f"stage5p-result-store-integration-{index:02d}"
        stage5o_hash = parity.get("stage5o_repeat_cuda_output_token_hash")
        records.append(
            {
                "record_type": "gematria_cuda_result_store_integration_record",
                "result_store_integration_id": integration_id,
                "source_repeat_parity_record_id": parity["repeat_parity_record_id"],
                "source_repeat_run_record_id": parity["repeat_run_record_id"],
                "stage5m_run_record_id": parity.get("stage5m_run_record_id"),
                "stage5m_parity_record_id": parity.get("stage5m_parity_record_id"),
                "mapping_id": parity["mapping_id"],
                "native_fixture_id": parity.get("native_fixture_id"),
                "fixture_id": parity["fixture_id"],
                "candidate_id": parity["candidate_id"],
                "source_input_stream_id": parity["source_input_stream_id"],
                "result_source_kind": "gematria_cuda_repeat_parity_summary",
                "source_path": source_path,
                "result_store_contract": RESULT_STORE_CONTRACT,
                "score_summary_contract": SCORE_SUMMARY_CONTRACT,
                "source_transform_family": parity["source_transform_family"],
                "original_transform_family": parity["source_transform_family"],
                "executed_kernel": parity["executed_kernel"],
                "executed_semantics": parity["executed_semantics"],
                "original_transform_family_semantics_exercised": False,
                "output_hash_algorithm": HASH_ALGORITHM,
                "stage5l_native_output_token_hash": parity["expected_native_output_token_hash"],
                "stage5m_cuda_output_token_hash": parity["stage5m_cuda_output_token_hash"],
                "stage5o_repeat_cuda_output_token_hash": stage5o_hash,
                "output_token_hash": stage5o_hash,
                "output_text_hash": None,
                "output_text_hash_status": "blocked_pending_transliteration_policy",
                "repeat_parity_status": parity["repeat_parity_status"],
                "repeat_cuda_status": parity["repeat_cuda_status"],
                "hashes_match": parity["repeat_parity_status"] == "passed",
                "stage5p_integration_status": "integrated_compact_summary"
                if parity["repeat_parity_status"] == "passed"
                else "blocked_repeat_parity_not_passed",
                "score_summary_link": f"stage5p-score-summary-integration-{index:02d}",
                "method_status_impact": "parity_verified_infrastructure_only",
                "stage4p_surface_reference": str(STAGE4P_SUMMARY),
                "generated_body_reference": "ignored_stage5o_generated_outputs_not_republished",
                "publication_scope": "compact_metadata_only",
                "source_cuda_execution_performed": parity.get("cuda_execution_performed") is True,
                "source_solved_fixture_cuda_used": parity.get("solved_fixture_cuda_used") is True,
                **COMMON_POLICY_FLAGS,
            }
        )
    write_record_set(result_store_integration_out, records)
    write_report(out_dir, RESULT_STORE_INTEGRATION_REPORT, {"records": records})
    write_warnings(out_dir, [])
    return records


def _repo_relative_path(path: Path) -> str:
    resolved = resolve_repo_path(path)
    try:
        return resolved.relative_to(resolve_repo_path(Path("."))).as_posix()
    except ValueError:
        return path.as_posix()
