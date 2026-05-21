"""Build compact Stage 5S result-store integration records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_expanded_cuda_result_store.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_expanded_cuda_result_store.models import (
    COMMON_FLAGS,
    EXECUTED_KERNEL,
    EXECUTED_SEMANTICS,
    HASH_ALGORITHM,
    OUTPUT_DIR,
    RESULT_STORE_CONTRACT,
    RESULT_STORE_INTEGRATION_PATH,
    RESULT_STORE_REPORT_JSON,
    SCORE_SUMMARY_CONTRACT,
    PARITY_REPORT_PATH,
)


def build_result_store_integration(
    *,
    parity_report: Path = PARITY_REPORT_PATH,
    result_store_integration_out: Path = RESULT_STORE_INTEGRATION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    parity = sorted(read_record_set(parity_report), key=lambda record: str(record["fixture_id"]))
    records = [_record(index=index, parity=record) for index, record in enumerate(parity)]
    write_record_set(result_store_integration_out, records)
    write_report(out_dir, RESULT_STORE_REPORT_JSON, {"records": records})
    return records


def _record(*, index: int, parity: dict[str, Any]) -> dict[str, Any]:
    record = {
        "record_type": "gematria_expanded_cuda_result_store_integration_record",
        "result_store_integration_id": f"stage5s-expanded-result-store-integration-{index:02d}",
        "parity_report_id": parity["parity_report_id"],
        "source_candidate_inventory_id": parity["source_stage5q_candidate_inventory_id"],
        "fixture_id": parity["fixture_id"],
        "source_input_stream_id": parity["source_input_stream_id"],
        "candidate_id": parity["candidate_id"],
        "original_transform_family": parity["source_transform_family"],
        "executed_kernel": EXECUTED_KERNEL,
        "executed_semantics": EXECUTED_SEMANTICS,
        "original_transform_family_semantics_exercised": False,
        "stage5q_native_hash": parity["stage5q_native_hash"],
        "stage5r_cuda_hash": parity["stage5r_cuda_hash"],
        "parity_status": parity["parity_status"],
        "output_hash_algorithm": HASH_ALGORITHM,
        "generated_body_committed": False,
        "output_token_hash_required": True,
        "output_text_hash_required": False,
        "stage4p_compatibility": True,
        "stage4p_surface_reference": "data/research/stage4p-result-store-score-summary-unification-summary.yaml",
        "score_summary_contract": SCORE_SUMMARY_CONTRACT,
        "result_store_contract": RESULT_STORE_CONTRACT,
        "method_status_impact": "expanded_parity_verified_infrastructure_only",
        "score_summary_link": f"stage5s-score-summary-integration-{index:02d}",
        "result_store_integration_status": "ready_compact_metadata_only",
    }
    record.update(COMMON_FLAGS)
    return record
