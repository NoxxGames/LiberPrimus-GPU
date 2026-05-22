"""Result-store preflight records for Stage 5X."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_parity.export import read_records, write_json_report, write_records
from libreprimus.prime_minus_one_native_parity.models import COMMON_RECORD_FLAGS, NATIVE_PARITY_PATH, OUTPUT_DIR, REPORT_FILES, RESULT_SOURCE_KIND, RESULT_STORE_PREFLIGHT_PATH


def build_result_store_preflight(
    *,
    native_parity: Path = NATIVE_PARITY_PATH,
    result_store_preflight_out: Path = RESULT_STORE_PREFLIGHT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    records = [_preflight(record) for record in read_records(native_parity)]
    write_records(result_store_preflight_out, records)
    write_json_report(out_dir, REPORT_FILES["result_store_preflight"], {"records": records})
    return records


def _preflight(parity: dict[str, Any]) -> dict[str, Any]:
    status = {
        "passed": "ready_for_stage5y_compact_summary_integration",
        "blocked_not_executed": "blocked_full_p56_token_buffer_missing",
    }.get(str(parity["parity_status"]), "blocked_hash_mismatch")
    return {
        **COMMON_RECORD_FLAGS,
        "record_type": "prime_minus_one_native_result_store_preflight_record",
        "schema": "schemas/cuda/prime-minus-one-native-result-store-preflight-record-v0.schema.json",
        "preflight_id": f"stage5x-result-store-{parity['mapping_id']}",
        "mapping_id": parity["mapping_id"],
        "fixture_id": parity["fixture_id"],
        "candidate_id": parity.get("candidate_id"),
        "result_source_kind": RESULT_SOURCE_KIND,
        "result_store_contract": "stage4p",
        "score_summary_contract": "stage4i",
        "compact_summary_only": True,
        "stage4p_compatible": status != "blocked_hash_mismatch",
        "output_token_hash_required": True,
        "output_token_hash": parity.get("computed_output_token_hash"),
        "output_text_hash_policy": "blocked_pending_transliteration_policy",
        "score_summary_label_policy": "finite_triage_only",
        "confidence_interpretation": "triage_only",
        "method_status_upgrade_allowed": False,
        "generated_body_publication_allowed": False,
        "performance_claim_allowed": False,
        "speedup_claim_allowed": False,
        "solve_claim": False,
        "preflight_status": status,
        "blockers": list(parity.get("blockers", [])),
    }
