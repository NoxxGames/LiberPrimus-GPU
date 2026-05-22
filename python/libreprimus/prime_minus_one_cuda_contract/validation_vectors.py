"""Build Stage 5Z validation-vector records."""

from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_cuda_contract.export import write_json_report, write_records
from libreprimus.prime_minus_one_cuda_contract.models import (
    FULL_P56_MAPPING_ID,
    OUTPUT_DIR,
    P56_BOUNDED_FORMULA_HASH,
    P56_BOUNDED_MAPPING_ID,
    P56_BOUNDED_OUTPUT_HASH,
    SYNTHETIC_MAPPING_ID,
    SYNTHETIC_OUTPUT_HASH,
    VALIDATION_VECTORS_PATH,
    base_record,
)


def build_validation_vectors(
    validation_vectors_out: Path = VALIDATION_VECTORS_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict]:
    specs = [
        (
            "stage5z-validation-synthetic-prime-control-v0",
            "synthetic_positive",
            SYNTHETIC_MAPPING_ID,
            "ready_for_future_synthetic_cuda_parity",
            SYNTHETIC_OUTPUT_HASH,
            None,
            [],
        ),
        (
            "stage5z-validation-p56-bounded-v0",
            "bounded_p56_fixture_safe",
            P56_BOUNDED_MAPPING_ID,
            "ready_for_future_synthetic_contract_reference_only",
            P56_BOUNDED_OUTPUT_HASH,
            P56_BOUNDED_FORMULA_HASH,
            ["not_authorized_for_stage5aa_cuda_execution"],
        ),
        (
            "stage5z-validation-full-p56-blocked-v0",
            "full_p56_blocker",
            FULL_P56_MAPPING_ID,
            "blocked_full_p56_token_buffer_missing",
            None,
            None,
            ["needs_full_committed_p56_cipher_token_buffer_before_full_fixture_cuda_execution"],
        ),
        (
            "stage5z-validation-invalid-token-v0",
            "invalid_token_value_control",
            "synthetic_invalid_token_control",
            "synthetic_control_expected_status_error",
            None,
            None,
            ["must_reject_token_values_outside_0_28"],
        ),
        (
            "stage5z-validation-invalid-stream-start-v0",
            "invalid_stream_start_control",
            "synthetic_invalid_stream_start_control",
            "synthetic_control_expected_status_error",
            None,
            None,
            ["must_reject_stream_start_beyond_schedule_length"],
        ),
        (
            "stage5z-validation-separator-preservation-v0",
            "separator_preservation_control",
            "synthetic_separator_preservation_control",
            "ready_for_future_synthetic_cuda_parity",
            None,
            None,
            ["separator_tokens_must_not_advance_prime_stream"],
        ),
        (
            "stage5z-validation-zero-transformable-v0",
            "zero_transformable_control",
            "synthetic_zero_transformable_control",
            "synthetic_control_expected_noop",
            None,
            None,
            ["zero_transformable_tokens_must_keep_output_stable"],
        ),
    ]
    records = [
        base_record(
            "prime_minus_one_cuda_validation_vector_record",
            "schemas/cuda/prime-minus-one-cuda-validation-vector-record-v0.schema.json",
            validation_vector_record_id=record_id,
            validation_vector_kind=kind,
            mapping_id=mapping_id,
            validation_status=status,
            expected_output_token_hash=output_hash,
            expected_formula_hash=formula_hash,
            blocker_ids=blockers,
            executable_in_stage5z=False,
            executable_in_stage5aa=kind.startswith("synthetic"),
            full_p56_allowed=False,
            p56_fixture_allowed=False,
            requires_raw_data=False,
        )
        for record_id, kind, mapping_id, status, output_hash, formula_hash, blockers in specs
    ]
    write_records(validation_vectors_out, records)
    write_json_report(out_dir, "validation_vector_report.json", {"records": records})
    return records


__all__ = ["build_validation_vectors"]
