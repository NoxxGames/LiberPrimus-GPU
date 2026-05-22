"""Deterministic prime-minus-one schedule records."""

from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_contract.export import write_json_report, write_records
from libreprimus.prime_minus_one_native_contract.models import COMMON_FLAGS, CONTRACT_ID, OUTPUT_DIR, PRIME_SCHEDULE_PATH, REPORT_FILES
from libreprimus.solved_fixtures.prime_stream import first_n_primes


def stream_values(count: int, *, prime_start_index: int = 0) -> tuple[list[int], list[int]]:
    primes = first_n_primes(count + prime_start_index)[prime_start_index:]
    return primes, [(prime - 1) % 29 for prime in primes]


def build_prime_schedule(*, prime_schedule_out: Path = PRIME_SCHEDULE_PATH, out_dir: Path = OUTPUT_DIR) -> list[dict[str, object]]:
    records = [
        _schedule_record(
            schedule_id="stage5w-synthetic-control-prime-minus-one-schedule-v0",
            fixture_id="stage5w-synthetic-prime-minus-one-control",
            value_count=8,
            schedule_status="synthetic_control_ready",
            token_length_source="stage5w_declared_synthetic_control",
        ),
        _schedule_record(
            schedule_id="stage5w-p56-stage4o-bounded-prime-minus-one-schedule-v0",
            fixture_id="p56-an-end-prime-minus-one",
            value_count=2,
            schedule_status="p56_stage4o_bounded_mapping_ready",
            token_length_source="data/cuda/stage5l-gematria-solved-fixture-token-mapping.yaml",
        ),
        _schedule_record(
            schedule_id="stage5w-p56-full-reference-prime-minus-one-schedule-v0",
            fixture_id="p56-an-end-prime-minus-one",
            value_count=84,
            schedule_status="p56_full_fixture_reference_schedule_full_token_buffer_blocked",
            token_length_source="data/fixtures/solved-pages/prime-stream-v0/p56-an-end-prime-minus-one.fixture.json",
            blockers=["needs_full_committed_p56_cipher_token_buffer_before_native_execution"],
        ),
    ]
    write_records(prime_schedule_out, records)
    write_json_report(out_dir, REPORT_FILES["prime_schedule"], {"records": records})
    return records


def _schedule_record(
    *,
    schedule_id: str,
    fixture_id: str,
    value_count: int,
    schedule_status: str,
    token_length_source: str,
    blockers: list[str] | None = None,
) -> dict[str, object]:
    primes, values = stream_values(value_count)
    return {
        **COMMON_FLAGS,
        "record_type": "prime_minus_one_schedule_record",
        "schema": "schemas/cuda/prime-minus-one-schedule-record-v0.schema.json",
        "schedule_id": schedule_id,
        "contract_id": CONTRACT_ID,
        "fixture_id": fixture_id,
        "prime_index_base": 0,
        "prime_start_index": 0,
        "first_n_primes": primes,
        "stream_values_mod29": values,
        "formula": "(prime_i - 1) mod 29",
        "value_count": value_count,
        "generation_algorithm": "trial_division_first_n_primes_from_stage1d_reference",
        "algorithm_status": "source_backed_deterministic",
        "deterministic": True,
        "raw_data_required": False,
        "native_execution_allowed": False,
        "cuda_execution_allowed": False,
        "generated_body_publication_allowed": False,
        "schedule_status": schedule_status,
        "token_length_source": token_length_source,
        "blockers": blockers or [],
    }
