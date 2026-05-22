"""Summary builder for Stage 5W prime-minus-one contract prep."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_contract.export import read_records, read_yaml, write_json_report, write_summary
from libreprimus.prime_minus_one_native_contract.models import (
    ABI_ID,
    COMMON_FLAGS,
    CANDIDATE_BATCH_MAPPING_PATH,
    GUARDRAIL_PATH,
    NATIVE_PARITY_PREPARATION_PATH,
    NEXT_STAGE_DECISION_PATH,
    NEXT_STAGE_REASON_READY,
    OUTPUT_DIR,
    PRIME_SCHEDULE_PATH,
    REPORT_FILES,
    RESULT_STORE_PREFLIGHT_PATH,
    SOURCE_INVENTORY_PATH,
    SOURCE_STAGE_ID,
    STREAM_CONTRACT_PATH,
    SUMMARY_PATH,
)


def build_summary(
    *,
    source_inventory: Path = SOURCE_INVENTORY_PATH,
    stream_contract: Path = STREAM_CONTRACT_PATH,
    prime_schedule: Path = PRIME_SCHEDULE_PATH,
    candidate_batch_mapping: Path = CANDIDATE_BATCH_MAPPING_PATH,
    native_parity_preparation: Path = NATIVE_PARITY_PREPARATION_PATH,
    result_store_preflight: Path = RESULT_STORE_PREFLIGHT_PATH,
    guardrail: Path = GUARDRAIL_PATH,
    next_stage_decision: Path = NEXT_STAGE_DECISION_PATH,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    source_records = read_records(source_inventory)
    contract_records = read_records(stream_contract)
    schedule_records = read_records(prime_schedule)
    mapping_records = read_records(candidate_batch_mapping)
    prep_records = read_records(native_parity_preparation)
    result_records = read_records(result_store_preflight)
    guardrail_records = read_records(guardrail)
    decision_records = read_records(next_stage_decision)
    selected = next(record for record in decision_records if record.get("selected") is True)
    blocked_count = _blocked_count(source_records, contract_records, schedule_records, mapping_records, prep_records, result_records, decision_records)
    payload = {
        **COMMON_FLAGS,
        "record_type": "stage5w_prime_minus_one_native_contract_summary",
        "schema": "schemas/cuda/stage5w-prime-minus-one-native-contract-summary-v0.schema.json",
        "stage_id": "stage-5w",
        "status": "complete",
        "source_stage_id": SOURCE_STAGE_ID,
        "candidate_batch_abi_id": ABI_ID,
        "source_inventory_records": len(source_records),
        "stream_contract_records": len(contract_records),
        "prime_schedule_records": len(schedule_records),
        "candidate_batch_mapping_records": len(mapping_records),
        "native_parity_preparation_records": len(prep_records),
        "result_store_preflight_records": len(result_records),
        "guardrail_records": len(guardrail_records),
        "next_stage_decision_records": len(decision_records),
        "p56_source_inventory_status": "source_backed_bounded_stage4o_mapping_ready_full_fixture_token_buffer_blocked",
        "p56_token_values_available": True,
        "p56_formula_direction_available": True,
        "p56_skip_policy_available": True,
        "p56_candidate_batch_mapping_status": "p56_solved_fixture_ready_for_bounded_stage4o_mapping",
        "p56_native_parity_preparation_status": "p56_stage4o_bounded_reference_hash_linked_full_fixture_blocked",
        "synthetic_control_schedule_records": sum(1 for record in schedule_records if str(record.get("schedule_status")).startswith("synthetic")),
        "synthetic_control_ready_count": sum(1 for record in mapping_records if record.get("mapping_status") == "synthetic_control_ready"),
        "blocked_record_count": blocked_count,
        "recommended_next_prompt_type": selected["recommended_prompt_type"],
        "recommended_next_stage_title": selected["recommended_stage_title"],
        "recommended_next_stage_reason": selected["rationale"] or NEXT_STAGE_REASON_READY,
        "deep_research_recommended_next": False,
    }
    write_summary(summary_out, payload)
    write_json_report(out_dir, REPORT_FILES["summary"], payload)
    return payload


def load_summary(path: Path = SUMMARY_PATH) -> dict[str, Any]:
    payload = read_yaml(path)
    if not isinstance(payload, dict):
        raise ValueError(f"summary is not a mapping: {path}")
    return dict(payload)


def _blocked_count(*groups: list[dict[str, Any]]) -> int:
    return sum(
        1
        for records in groups
        for record in records
        if str(record.get("status", "")).startswith("blocked")
        or str(record.get("contract_status", "")).startswith("blocked")
        or str(record.get("schedule_status", "")).startswith("p56_full_fixture")
        or str(record.get("mapping_status", "")).startswith("p56_blocked")
        or str(record.get("preparation_status", "")).startswith("blocked")
        or str(record.get("preflight_status", "")).startswith("blocked")
        or bool(record.get("blockers"))
    )
