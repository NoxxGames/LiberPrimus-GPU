"""Native parity preparation records for Stage 5W."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cpu_batch.input_streams import stable_json_sha256
from libreprimus.prime_minus_one_native_contract.export import read_yaml, write_json_report, write_records
from libreprimus.prime_minus_one_native_contract.models import COMMON_FLAGS, CONTRACT_ID, NATIVE_PARITY_PREPARATION_PATH, OUTPUT_DIR, P56_CANDIDATE_ID, P56_FIXTURE_ID, REPORT_FILES, STAGE5L_NATIVE_PARITY_PATH


def build_native_parity_preparation(
    *, native_parity_preparation_out: Path = NATIVE_PARITY_PREPARATION_PATH, out_dir: Path = OUTPUT_DIR
) -> list[dict[str, Any]]:
    stage5l_hash = _p56_stage5l_hash()
    synthetic_output = [
        {"position": 0, "token_kind": "rune", "transformable": True, "index29": 28},
        {"position": 1, "token_kind": "rune", "transformable": True, "index29": 0},
        {"position": 2, "token_kind": "word_separator", "transformable": False, "index29": -1},
        {"position": 3, "token_kind": "rune", "transformable": True, "index29": 27},
    ]
    records = [
        _record(
            native_parity_preparation_id="stage5w-native-prep-synthetic-control-v0",
            fixture_id="stage5w-synthetic-prime-minus-one-control",
            candidate_batch_mapping_id="stage5w-mapping-synthetic-prime-control-v0",
            preparation_status="synthetic_contract_hash_prepared_without_native_execution",
            input_token_values_available=True,
            stream_schedule_available=True,
            formula_direction_available=True,
            skip_policy_available=True,
            expected_output_token_hash=stable_json_sha256(synthetic_output),
            next_required_stage="Stage 5X may execute synthetic no-GPU native parity controls if explicitly scoped.",
        ),
        _record(
            native_parity_preparation_id="stage5w-native-prep-p56-stage4o-bounded-v0",
            fixture_id=P56_FIXTURE_ID,
            candidate_id=P56_CANDIDATE_ID,
            candidate_batch_mapping_id="stage5w-mapping-p56-stage4o-bounded-v0",
            preparation_status="p56_stage4o_bounded_reference_hash_linked",
            input_token_values_available=True,
            stream_schedule_available=True,
            formula_direction_available=True,
            skip_policy_available=True,
            expected_output_token_hash=stage5l_hash,
            existing_reference_hash_source="data/cuda/stage5l-gematria-solved-fixture-native-parity.yaml:stage5l-native-parity-04",
            next_required_stage="Stage 5X can execute no-GPU native parity against this bounded p56 mapping.",
        ),
        _record(
            native_parity_preparation_id="stage5w-native-prep-p56-full-fixture-blocked-v0",
            fixture_id=P56_FIXTURE_ID,
            candidate_batch_mapping_id="stage5w-mapping-p56-full-fixture-blocked-v0",
            preparation_status="blocked_missing_full_p56_token_values",
            input_token_values_available=False,
            stream_schedule_available=True,
            formula_direction_available=True,
            skip_policy_available=True,
            expected_output_token_hash=None,
            blockers=["needs_full_committed_p56_cipher_token_buffer_before_full_fixture_native_execution"],
            next_required_stage="Full p56 native execution requires a future source-backed token-buffer expansion stage.",
        ),
    ]
    write_records(native_parity_preparation_out, records)
    write_json_report(out_dir, REPORT_FILES["native_parity_preparation"], {"records": records})
    return records


def _record(
    *,
    native_parity_preparation_id: str,
    fixture_id: str,
    candidate_batch_mapping_id: str,
    preparation_status: str,
    input_token_values_available: bool,
    stream_schedule_available: bool,
    formula_direction_available: bool,
    skip_policy_available: bool,
    expected_output_token_hash: str | None,
    next_required_stage: str,
    candidate_id: str | None = None,
    blockers: list[str] | None = None,
    existing_reference_hash_source: str | None = None,
) -> dict[str, Any]:
    return {
        **COMMON_FLAGS,
        "record_type": "prime_minus_one_native_parity_preparation_record",
        "schema": "schemas/cuda/prime-minus-one-native-parity-preparation-record-v0.schema.json",
        "native_parity_preparation_id": native_parity_preparation_id,
        "fixture_id": fixture_id,
        "candidate_id": candidate_id,
        "contract_id": CONTRACT_ID,
        "candidate_batch_mapping_id": candidate_batch_mapping_id,
        "preparation_status": preparation_status,
        "input_token_values_available": input_token_values_available,
        "stream_schedule_available": stream_schedule_available,
        "formula_direction_available": formula_direction_available,
        "skip_policy_available": skip_policy_available,
        "expected_output_token_hash": expected_output_token_hash,
        "existing_reference_hash_source": existing_reference_hash_source,
        "output_hash_algorithm": "sha256_canonical_json_v1",
        "expected_output_body_committed": False,
        "native_execution_performed": False,
        "python_reference_execution_performed": False,
        "cuda_execution_performed": False,
        "blockers": blockers or [],
        "next_required_stage": next_required_stage,
    }


def _p56_stage5l_hash() -> str:
    payload = read_yaml(STAGE5L_NATIVE_PARITY_PATH)
    for record in payload.get("records", []) if isinstance(payload, dict) else []:
        if isinstance(record, dict) and record.get("fixture_id") == P56_FIXTURE_ID:
            return str(record.get("output_token_hash", ""))
    return ""
