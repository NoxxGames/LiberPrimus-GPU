"""Build transform-parameter contract records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cuda_candidate_batch_abi.export import write_record_set, write_report
from libreprimus.cuda_candidate_batch_abi.models import (
    COMMON_FLAGS,
    OUTPUT_DIR,
    TRANSFORM_PARAMETER_CONTRACT_PATH,
    TRANSFORM_PARAMETER_REPORT_JSON,
)


def build_transform_parameter_contract(
    *,
    transform_parameter_contract_out: Path = TRANSFORM_PARAMETER_CONTRACT_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Define transform family parameter layouts without implementing kernels."""

    rows = [
        {
            "family_id": "shift_mod29",
            "contract_status": "defined_for_existing_gematria_shift_score_control",
            "parameter_layout": ["shift_value:uint8"],
            "candidate_parameter_count": 1,
            "parameter_value_domains": {"shift_value": "0..28"},
            "formula_policy": "(token + shift_value) mod 29 for transformable rune tokens only",
            "requires_cuda_kernel_contract": False,
            "requires_native_reference_contract": False,
        },
        {
            "family_id": "reverse_gematria",
            "contract_status": "needs_family_specific_contract",
            "parameter_layout": [],
            "candidate_parameter_count": 0,
            "parameter_value_domains": {},
            "formula_policy": "candidate formula equivalent to 28 - token; separate contract must confirm direction and output hashing",
            "requires_cuda_kernel_contract": True,
            "requires_native_reference_contract": True,
        },
        {
            "family_id": "rotated_reverse_gematria",
            "contract_status": "needs_family_specific_contract",
            "parameter_layout": ["rotation:uint8"],
            "candidate_parameter_count": 1,
            "parameter_value_domains": {"rotation": "0..28"},
            "formula_policy": "reverse plus rotation is expected but exact committed family contract remains pending",
            "requires_cuda_kernel_contract": True,
            "requires_native_reference_contract": True,
        },
        {
            "family_id": "affine_mod29",
            "contract_status": "needs_family_specific_contract",
            "parameter_layout": ["a:uint8", "b:uint8"],
            "candidate_parameter_count": 2,
            "parameter_value_domains": {"a": "1..28 and gcd(a,29)=1", "b": "0..28"},
            "formula_policy": "(a * token + b) mod 29 is the placeholder contract; direction must be confirmed by a later family-specific stage",
            "requires_cuda_kernel_contract": True,
            "requires_native_reference_contract": True,
        },
        {
            "family_id": "vigenere_explicit_key",
            "contract_status": "defined_for_stage5v_planning_implementation_pending",
            "parameter_layout": ["key_schedule_ref:uint32", "key_reset_policy:uint8", "key_advance_policy:uint8"],
            "candidate_parameter_count": 3,
            "parameter_value_domains": {
                "key_schedule_ref": "0..key_schedule_count-1",
                "key_reset_policy": "declared enum",
                "key_advance_policy": "declared enum",
            },
            "formula_policy": "Vigenere key tokens 0..28; skip/advance/reset must be explicit before execution",
            "requires_cuda_kernel_contract": True,
            "requires_native_reference_contract": True,
        },
        {
            "family_id": "prime_minus_one_stream",
            "contract_status": "defined_for_stage5v_planning_implementation_pending",
            "parameter_layout": ["stream_schedule_ref:uint32", "stream_start_index:uint32", "stream_advance_policy:uint8"],
            "candidate_parameter_count": 3,
            "parameter_value_domains": {
                "stream_schedule_ref": "0..stream_schedule_count-1",
                "stream_start_index": "0..stream_length-1",
                "stream_advance_policy": "declared enum",
            },
            "formula_policy": "stream values are (prime_i - 1) mod 29 from a declared deterministic stream record",
            "requires_cuda_kernel_contract": True,
            "requires_native_reference_contract": True,
        },
    ]
    records = []
    for index, row in enumerate(rows):
        family_id = str(row["family_id"])
        records.append(
            {
                "record_type": "transform_parameter_contract_record",
                "transform_parameter_contract_id": f"stage5u-transform-parameter-{index:02d}",
                "family_id": family_id,
                "reset_policy_supported": family_id in {"vigenere_explicit_key", "prime_minus_one_stream"},
                "advance_policy_supported": family_id in {"vigenere_explicit_key", "prime_minus_one_stream"},
                "requires_key_schedule": family_id == "vigenere_explicit_key",
                "requires_stream_schedule": family_id == "prime_minus_one_stream",
                "requires_affine_coefficients": family_id == "affine_mod29",
                "requires_rotation_parameter": family_id == "rotated_reverse_gematria",
                "requires_per_candidate_seed": family_id in {"vigenere_explicit_key", "prime_minus_one_stream"},
                "compatible_with_candidate_batch_abi_v0": True,
                "implementation_allowed_now": False,
                "notes": "Contract record only; no CUDA or native backend implementation is added in Stage 5U.",
                **row,
                **COMMON_FLAGS,
            }
        )
    write_record_set(transform_parameter_contract_out, records)
    write_report(out_dir, TRANSFORM_PARAMETER_REPORT_JSON, {"records": records})
    return records
