"""Implementation records for the Stage 5J Gematria CUDA kernel."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_cuda_kernel.export import write_record_set, write_report, write_warnings
from libreprimus.gematria_cuda_kernel.models import (
    COMMON_POLICY_FLAGS,
    EXPECTED_OUTPUTS,
    IMPLEMENTATION_PATH,
    IMPLEMENTATION_REPORT,
    INPUT_TOKEN_VALUES,
    KERNEL_HEADER,
    KERNEL_SOURCE,
    KERNEL_TEST,
    OUTPUT_DIR,
    SHIFTS,
    TOKEN_KINDS,
    TRANSFORMABLE_MASK,
)


def build_implementation_records(
    *,
    implementation_out: Path = IMPLEMENTATION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Build committed implementation metadata for the single Stage 5J kernel."""

    record: dict[str, Any] = {
        "record_type": "gematria_cuda_kernel_implementation_record",
        "implementation_id": "stage5j-gematria-mod29-shift-score-kernel-implementation",
        "implementation_status": "implemented_synthetic_numeric_only",
        "kernel_header": KERNEL_HEADER,
        "kernel_source": KERNEL_SOURCE,
        "kernel_test": KERNEL_TEST,
        "cuda_c_abi_shape": {
            "input_token_values": "const unsigned char*",
            "transformable_mask": "const unsigned char*",
            "shifts": "const unsigned char*",
            "output_token_values": "unsigned char*",
            "status_codes": "int*",
            "token_count": "int",
            "candidate_count": "int",
        },
        "input_token_values": list(INPUT_TOKEN_VALUES),
        "transformable_mask": list(TRANSFORMABLE_MASK),
        "token_kinds": list(TOKEN_KINDS),
        "shifts": list(SHIFTS),
        "expected_outputs": [list(row) for row in EXPECTED_OUTPUTS],
        "semantic_scope": "synthetic_numeric_gematria_mod29_shift_only",
        "cuda_execution_performed": False,
        "notes": [
            "Exactly one new CUDA kernel target is introduced for Stage 5J.",
            "The Stage 5F uppercase Latin synthetic kernel remains separate.",
            "Solved fixtures, unsolved pages, and real Liber Primus data remain blocked from CUDA execution.",
        ],
        **COMMON_POLICY_FLAGS,
    }
    records = [record]
    write_record_set(implementation_out, records)
    write_report(out_dir, IMPLEMENTATION_REPORT, {"records": records})
    write_warnings(out_dir, [])
    return records
