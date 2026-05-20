"""Stage 5I Gematria CUDA kernel-preparation record generation."""

from __future__ import annotations

from pathlib import Path

from libreprimus.gematria_cuda_prep.export import write_record_set, write_report, write_warnings
from libreprimus.gematria_cuda_prep.models import (
    ARITHMETIC_FORMULA,
    COMMON_POLICY_FLAGS,
    KERNEL_PREPARATION_JSON,
    OUTPUT_DIR,
    PREPARATION_ID,
    PREPARATION_PATH,
    STAGE5F_HASH,
)


def build_kernel_preparation_records(
    *,
    preparation_out: Path = PREPARATION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    """Build no-GPU-safe implementation-preparation records."""

    record: dict[str, object] = {
        "record_type": "gematria_cuda_kernel_preparation_record",
        "preparation_id": PREPARATION_ID,
        "preparation_status": "ready_for_stage5j_synthetic_implementation",
        "arithmetic_formula": ARITHMETIC_FORMULA,
        "implementation_boundary": "preparation_only_no_cuda_kernel_added",
        "stage5h_contract_source": "data/cuda/stage5h-gematria-shift-score-contract.yaml",
        "stage5h_fixture_source": "data/cuda/stage5h-gematria-native-parity-fixtures.yaml",
        "stage5g_device_subset_source": "data/cuda/stage5g-cuda-device-code-subset-audit.yaml",
        "preserved_stage5f_hash": STAGE5F_HASH,
        "preparation_requirements": [
            "define_c_compatible_kernel_abi",
            "define_numeric_token_buffers",
            "define_transformable_mask",
            "define_candidate_major_output_order",
            "define_validation_vectors_from_stage5h_fixture",
            "preserve_stage5f_uppercase_latin_kernel_scope",
            "keep_solved_fixture_cuda_execution_blocked",
        ],
        "stage5j_ready_for_synthetic_implementation": True,
        **COMMON_POLICY_FLAGS,
    }
    records = [record]
    write_record_set(preparation_out, records)
    write_report(out_dir, KERNEL_PREPARATION_JSON, {"records": records})
    write_warnings(out_dir, [])
    return records
