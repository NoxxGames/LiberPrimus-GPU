"""Result-store and score-summary preflight records for Stage 5W."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_contract.export import write_json_report, write_records
from libreprimus.prime_minus_one_native_contract.models import ABI_ID, COMMON_FLAGS, CONTRACT_ID, OUTPUT_DIR, P56_FIXTURE_ID, REPORT_FILES, RESULT_STORE_PREFLIGHT_PATH


def build_result_store_preflight(
    *, result_store_preflight_out: Path = RESULT_STORE_PREFLIGHT_PATH, out_dir: Path = OUTPUT_DIR
) -> list[dict[str, Any]]:
    records = [
        _record(
            result_store_preflight_id="stage5w-result-store-preflight-synthetic-control-v0",
            fixture_id="stage5w-synthetic-prime-minus-one-control",
            preflight_status="ready_for_stage5x_synthetic_native_parity",
        ),
        _record(
            result_store_preflight_id="stage5w-result-store-preflight-p56-stage4o-bounded-v0",
            fixture_id=P56_FIXTURE_ID,
            preflight_status="ready_for_stage5x_bounded_p56_native_parity",
        ),
        _record(
            result_store_preflight_id="stage5w-result-store-preflight-p56-full-blocked-v0",
            fixture_id=P56_FIXTURE_ID,
            preflight_status="blocked_missing_full_p56_token_values",
            output_token_hash_required=True,
            blockers=["needs_full_committed_p56_cipher_token_buffer_before_full_fixture_result_store_preflight"],
        ),
    ]
    write_records(result_store_preflight_out, records)
    write_json_report(out_dir, REPORT_FILES["result_store_preflight"], {"records": records})
    return records


def _record(
    *,
    result_store_preflight_id: str,
    fixture_id: str,
    preflight_status: str,
    output_token_hash_required: bool = True,
    blockers: list[str] | None = None,
) -> dict[str, Any]:
    return {
        **COMMON_FLAGS,
        "record_type": "prime_minus_one_result_store_preflight_record",
        "schema": "schemas/cuda/prime-minus-one-result-store-preflight-record-v0.schema.json",
        "result_store_preflight_id": result_store_preflight_id,
        "fixture_id": fixture_id,
        "contract_id": CONTRACT_ID,
        "result_store_contract": "stage4p",
        "score_summary_contract": "stage4i",
        "candidate_batch_abi_id": ABI_ID,
        "result_source_kind": "prime_minus_one_native_contract_preparation",
        "compact_summary_only": True,
        "output_token_hash_required": output_token_hash_required,
        "output_text_hash_policy": "blocked_pending_transliteration_policy",
        "score_summary_label_policy": "finite_triage_only",
        "confidence_interpretation": "triage_only",
        "method_status_upgrade_allowed": False,
        "generated_body_publication_allowed": False,
        "performance_claim_allowed": False,
        "speedup_claim_allowed": False,
        "solve_claim": False,
        "preflight_status": preflight_status,
        "blockers": blockers or [],
    }
