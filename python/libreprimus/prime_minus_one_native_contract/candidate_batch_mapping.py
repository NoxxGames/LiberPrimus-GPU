"""Candidate Batch ABI v0 mappings for prime-minus-one Stage 5W records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_contract.export import write_json_report, write_records
from libreprimus.prime_minus_one_native_contract.models import ABI_ID, COMMON_FLAGS, CONTRACT_ID, OUTPUT_DIR, P56_CANDIDATE_ID, P56_FIXTURE_ID, REPORT_FILES, CANDIDATE_BATCH_MAPPING_PATH


def build_candidate_batch_mapping(
    *, candidate_batch_mapping_out: Path = CANDIDATE_BATCH_MAPPING_PATH, out_dir: Path = OUTPUT_DIR
) -> list[dict[str, Any]]:
    records = [
        _record(
            mapping_id="stage5w-mapping-synthetic-prime-control-v0",
            fixture_id="stage5w-synthetic-prime-minus-one-control",
            stream_schedule_ref="stage5w-synthetic-control-prime-minus-one-schedule-v0",
            token_buffer_source="stage5w_declared_synthetic_control_tokens",
            token_count=4,
            transformable_token_count=3,
            separator_count=1,
            candidate_count=1,
            mapping_status="synthetic_control_ready",
        ),
        _record(
            mapping_id="stage5w-mapping-p56-stage4o-bounded-v0",
            fixture_id=P56_FIXTURE_ID,
            candidate_id=P56_CANDIDATE_ID,
            stream_schedule_ref="stage5w-p56-stage4o-bounded-prime-minus-one-schedule-v0",
            token_buffer_source="data/cuda/stage5l-gematria-solved-fixture-token-mapping.yaml:stage5l-token-mapping-04",
            token_count=2,
            transformable_token_count=2,
            separator_count=0,
            candidate_count=1,
            mapping_status="p56_solved_fixture_ready",
        ),
        _record(
            mapping_id="stage5w-mapping-p56-full-fixture-blocked-v0",
            fixture_id=P56_FIXTURE_ID,
            stream_schedule_ref="stage5w-p56-full-reference-prime-minus-one-schedule-v0",
            token_buffer_source="not_committed",
            token_count=0,
            transformable_token_count=0,
            separator_count=0,
            candidate_count=0,
            mapping_status="p56_blocked_missing_token_values",
            blockers=["needs_full_committed_p56_cipher_token_buffer_before_full_fixture_native_execution"],
        ),
    ]
    write_records(candidate_batch_mapping_out, records)
    write_json_report(out_dir, REPORT_FILES["candidate_batch_mapping"], {"records": records})
    return records


def _record(
    *,
    mapping_id: str,
    fixture_id: str,
    stream_schedule_ref: str,
    token_buffer_source: str,
    token_count: int,
    transformable_token_count: int,
    separator_count: int,
    candidate_count: int,
    mapping_status: str,
    candidate_id: str | None = None,
    blockers: list[str] | None = None,
) -> dict[str, Any]:
    return {
        **COMMON_FLAGS,
        "record_type": "prime_minus_one_candidate_batch_mapping_record",
        "schema": "schemas/cuda/prime-minus-one-candidate-batch-mapping-record-v0.schema.json",
        "mapping_id": mapping_id,
        "contract_id": CONTRACT_ID,
        "candidate_batch_abi_id": ABI_ID,
        "fixture_id": fixture_id,
        "candidate_id": candidate_id,
        "stream_schedule_ref": stream_schedule_ref,
        "stream_start_index": 0,
        "stream_advance_policy": "advance_on_enciphered_transformable_rune_tokens_only",
        "transform_parameter_layout": ["stream_schedule_ref:uint32", "stream_start_index:uint32", "stream_advance_policy:uint8"],
        "token_buffer_source": token_buffer_source,
        "token_count": token_count,
        "transformable_token_count": transformable_token_count,
        "separator_count": separator_count,
        "candidate_count": candidate_count,
        "mapping_status": mapping_status,
        "requires_stage5x_execution": mapping_status.endswith("ready"),
        "cuda_execution_allowed": False,
        "generated_body_publication_allowed": False,
        "blockers": blockers or [],
    }
