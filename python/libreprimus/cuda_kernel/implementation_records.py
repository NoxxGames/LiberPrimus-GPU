"""Implementation records for the Stage 5F synthetic CUDA kernel."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cuda_kernel.export import write_record_set, write_report, write_warnings
from libreprimus.cuda_kernel.models import (
    COMMON_POLICY_FLAGS,
    IMPLEMENTATION_PATH,
    IMPLEMENTATION_REPORT,
    NATIVE_REFERENCE_HASH,
    OUTPUT_DIR,
    STAGE_ID,
)


def build_implementation_records(
    *,
    implementation_out: Path = IMPLEMENTATION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    record: dict[str, Any] = {
        "record_type": "cuda_synthetic_kernel_implementation_record",
        "stage_id": STAGE_ID,
        "implementation_id": "stage5f-shift-score-synthetic-kernel-implementation",
        "implementation_status": "implemented_synthetic_only",
        "kernel_header": "cuda/include/libreprimus/shift_score_kernel.cuh",
        "kernel_source": "cuda/kernels/shift_score_kernel.cu",
        "cuda_kernel_added": True,
        "cuda_source_modified": True,
        "cuda_transform_executed": False,
        "native_reference_hash": NATIVE_REFERENCE_HASH,
        "synthetic_fixture_text": "LIBER PRIMUS STAGE FIVE D",
        "synthetic_shifts": [0, 1, 3, 7, 13, 28],
        "semantic_scope": "uppercase_latin_a_to_z_synthetic_shift_only",
        "notes": [
            "This kernel matches the Stage 5D synthetic uppercase shift fixture only.",
            "It is not a production Gematria Primus mod-29 kernel.",
            "It must not be used on real solved or unsolved Liber Primus page material.",
        ],
        **COMMON_POLICY_FLAGS,
    }
    records = [record]
    write_record_set(implementation_out, records)
    write_report(out_dir, IMPLEMENTATION_REPORT, {"records": records})
    write_warnings(out_dir, [])
    return records
