"""Source inventory records for Stage 5W prime-minus-one contract prep."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_contract.export import read_yaml, write_json_report, write_records
from libreprimus.prime_minus_one_native_contract.models import (
    COMMON_FLAGS,
    FAMILY_ID,
    OUTPUT_DIR,
    P56_FIXTURE_ID,
    P56_FIXTURE_PATH,
    REPORT_FILES,
    SOURCE_INVENTORY_PATH,
    STAGE4O_MANIFEST_PATH,
    STAGE5L_NATIVE_PARITY_PATH,
    STAGE5L_TOKEN_MAPPING_PATH,
    STAGE5T_INVENTORY_PATH,
    STAGE5T_KERNEL_READINESS_PATH,
    STAGE5U_STREAM_CONTRACT_PATH,
    STAGE5V_SUMMARY_PATH,
    TRANSFORM_REGISTRY_PATH,
)


def build_source_inventory(*, source_inventory_out: Path = SOURCE_INVENTORY_PATH, out_dir: Path = OUTPUT_DIR) -> list[dict[str, Any]]:
    fixture = read_yaml(P56_FIXTURE_PATH)
    stage5l_mapping = _find_record(STAGE5L_TOKEN_MAPPING_PATH, "fixture_id", P56_FIXTURE_ID)
    stage5l_parity = _find_record(STAGE5L_NATIVE_PARITY_PATH, "fixture_id", P56_FIXTURE_ID)
    records = [
        _record(
            source_inventory_id="stage5w-source-p56-fixture-json",
            fixture_id=P56_FIXTURE_ID,
            source_path=str(P56_FIXTURE_PATH),
            source_record_id=str(fixture.get("fixture_id")),
            source_kind="solved_page_fixture",
            source_status="committed_safe_fixture_metadata_present",
            solved_fixture_safe=True,
            token_values_available=False,
            plaintext_or_expected_available=True,
            stream_formula_available=True,
            formula_direction_available=True,
            skip_policy_available=True,
            candidate_batch_abi_compatible=True,
            blockers=["full_cipher_token_buffer_not_committed_for_stage5w_native_execution"],
            notes=[
                "Fixture declares transform_chain with prime_start_index=0, direction=forward, stream_value=prime_minus_one_mod29, and cleartext pass-through skip rule.",
                "The fixture includes expected plaintext and payload checks but not a full committed cipher token buffer for Stage 5W native execution.",
            ],
        ),
        _record(
            source_inventory_id="stage5w-source-stage5l-p56-token-mapping",
            fixture_id=P56_FIXTURE_ID,
            source_path=str(STAGE5L_TOKEN_MAPPING_PATH),
            source_record_id=str(stage5l_mapping.get("mapping_record_id")),
            source_kind="stage5l_solved_fixture_token_mapping",
            source_status="committed_safe_p56_stage4o_token_mapping_present",
            solved_fixture_safe=True,
            token_values_available=True,
            plaintext_or_expected_available=False,
            stream_formula_available=False,
            formula_direction_available=False,
            skip_policy_available=False,
            candidate_batch_abi_compatible=True,
            token_count=int(stage5l_mapping.get("token_count", 0)),
            source_backed_token_value_hash=stage5l_mapping.get("source_backed_token_value_hash"),
            blockers=["full_p56_fixture_token_buffer_not_available_in_stage5l"],
            notes=["Stage 5L provides the tiny Stage 4O p56 solved-fixture-safe token mapping, not the full p56 page token buffer."],
        ),
        _record(
            source_inventory_id="stage5w-source-stage5l-p56-native-parity-hash",
            fixture_id=P56_FIXTURE_ID,
            source_path=str(STAGE5L_NATIVE_PARITY_PATH),
            source_record_id=str(stage5l_parity.get("native_parity_record_id")),
            source_kind="stage5l_solved_fixture_native_parity_hash",
            source_status="committed_safe_reference_hash_present",
            solved_fixture_safe=True,
            token_values_available=False,
            plaintext_or_expected_available=False,
            stream_formula_available=False,
            formula_direction_available=False,
            skip_policy_available=False,
            candidate_batch_abi_compatible=True,
            output_token_hash=stage5l_parity.get("output_token_hash"),
            blockers=[],
            notes=["Stage 5W cites this compact hash for future result-store compatibility; it does not recompute or publish token bodies."],
        ),
        _record(
            source_inventory_id="stage5w-source-stage5u-stream-schedule-contract",
            fixture_id=P56_FIXTURE_ID,
            source_path=str(STAGE5U_STREAM_CONTRACT_PATH),
            source_record_id="stage5u-prime-minus-one-stream-schedule-v0",
            source_kind="stage5u_stream_schedule_contract",
            source_status="committed_stream_schedule_contract_present",
            solved_fixture_safe=True,
            token_values_available=False,
            plaintext_or_expected_available=False,
            stream_formula_available=True,
            formula_direction_available=False,
            skip_policy_available=True,
            candidate_batch_abi_compatible=True,
            blockers=["formula_direction_confirmed_by_stage1d_fixture_not_stage5u_contract_alone"],
        ),
        _record(
            source_inventory_id="stage5w-source-transform-registry",
            fixture_id=P56_FIXTURE_ID,
            source_path=str(TRANSFORM_REGISTRY_PATH),
            source_record_id="prime_minus_one_stream",
            source_kind="cpu_reference_transform_registry",
            source_status="committed_cpu_reference_formula_present",
            solved_fixture_safe=True,
            token_values_available=False,
            plaintext_or_expected_available=False,
            stream_formula_available=True,
            formula_direction_available=True,
            skip_policy_available=True,
            candidate_batch_abi_compatible=True,
        ),
        _record(
            source_inventory_id="stage5w-source-stage4o-p56-input-stream",
            fixture_id=P56_FIXTURE_ID,
            source_path=str(STAGE4O_MANIFEST_PATH),
            source_record_id="stage4o-fixture-prime-an-v0",
            source_kind="stage4o_solved_fixture_safe_cpu_batch_stream",
            source_status="committed_safe_two_token_p56_stream_present",
            solved_fixture_safe=True,
            token_values_available=True,
            plaintext_or_expected_available=False,
            stream_formula_available=True,
            formula_direction_available=True,
            skip_policy_available=True,
            candidate_batch_abi_compatible=True,
            token_count=int(stage5l_mapping.get("token_count", 0)),
            blockers=[],
            notes=["This is the bounded p56 stream Stage 5X may execute no-GPU; it is not full-page p56 execution."],
        ),
        _record(
            source_inventory_id="stage5w-source-stage5t-prime-family-readiness",
            fixture_id=P56_FIXTURE_ID,
            source_path=f"{STAGE5T_INVENTORY_PATH};{STAGE5T_KERNEL_READINESS_PATH};{STAGE5V_SUMMARY_PATH}",
            source_record_id="stage5t-inventory-prime_minus_one_stream",
            source_kind="cuda_solved_family_readiness_and_stage5v_selection",
            source_status="committed_priority_and_stage5v_selection_present",
            solved_fixture_safe=True,
            token_values_available=False,
            plaintext_or_expected_available=False,
            stream_formula_available=False,
            formula_direction_available=False,
            skip_policy_available=False,
            candidate_batch_abi_compatible=True,
            blockers=[],
        ),
    ]
    write_records(source_inventory_out, records)
    write_json_report(out_dir, REPORT_FILES["source_inventory"], {"records": records})
    return records


def _record(
    *,
    source_inventory_id: str,
    fixture_id: str,
    source_path: str,
    source_record_id: str,
    source_kind: str,
    source_status: str,
    solved_fixture_safe: bool,
    token_values_available: bool,
    plaintext_or_expected_available: bool,
    stream_formula_available: bool,
    formula_direction_available: bool,
    skip_policy_available: bool,
    candidate_batch_abi_compatible: bool,
    blockers: list[str] | None = None,
    notes: list[str] | None = None,
    **extra: Any,
) -> dict[str, Any]:
    return {
        **COMMON_FLAGS,
        "record_type": "prime_minus_one_source_inventory_record",
        "schema": "schemas/cuda/prime-minus-one-source-inventory-record-v0.schema.json",
        "source_inventory_id": source_inventory_id,
        "family_id": FAMILY_ID,
        "fixture_id": fixture_id,
        "source_path": source_path,
        "source_record_id": source_record_id,
        "source_kind": source_kind,
        "source_status": source_status,
        "committed_safe_source": True,
        "raw_data_required": False,
        "canonical_corpus_required": False,
        "solved_fixture_safe": solved_fixture_safe,
        "token_values_available": token_values_available,
        "plaintext_or_expected_available": plaintext_or_expected_available,
        "stream_formula_available": stream_formula_available,
        "formula_direction_available": formula_direction_available,
        "skip_policy_available": skip_policy_available,
        "candidate_batch_abi_compatible": candidate_batch_abi_compatible,
        "blockers": blockers or [],
        "notes": notes or [],
        **extra,
    }


def _find_record(path: Path, key: str, value: str) -> dict[str, Any]:
    payload = read_yaml(path)
    for record in payload.get("records", []) if isinstance(payload, dict) else []:
        if isinstance(record, dict) and record.get(key) == value:
            return dict(record)
    return {}
