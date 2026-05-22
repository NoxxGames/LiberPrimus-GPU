"""Stage 5AA kernel implementation metadata."""

from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_cuda_synthetic.export import resolve, write_json_report, write_records
from libreprimus.prime_minus_one_cuda_synthetic.models import (
    CUDA_HEADER,
    CUDA_SOURCE,
    CUDA_TEST,
    KERNEL_ENTRYPOINT,
    KERNEL_IMPLEMENTATION_PATH,
    OUTPUT_DIR,
    REPORT_FILES,
    VALIDATION_VECTOR_ID,
    base_record,
)


def build_kernel_implementation_records(
    *,
    kernel_implementation_out: Path = KERNEL_IMPLEMENTATION_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    record = base_record(
        "prime_minus_one_cuda_synthetic_kernel_implementation_record",
        "schemas/cuda/prime-minus-one-cuda-synthetic-kernel-implementation-record-v0.schema.json",
        implementation_record_id="stage5aa-prime-minus-one-cuda-synthetic-kernel-implementation-v0",
        kernel_entrypoint=KERNEL_ENTRYPOINT,
        validation_vector_id=VALIDATION_VECTOR_ID,
        cuda_source_files=[
            str(CUDA_HEADER),
            str(CUDA_SOURCE),
            str(CUDA_TEST),
            "cuda/CMakeLists.txt",
            "cuda/tests/CMakeLists.txt",
        ],
        cuda_header_present=resolve(CUDA_HEADER).exists(),
        cuda_source_present=resolve(CUDA_SOURCE).exists(),
        cuda_test_present=resolve(CUDA_TEST).exists(),
        implementation_scope="stage5z_validation_synthetic_prime_control_only",
        p56_cuda_allowed=False,
        full_p56_cuda_allowed=False,
        unsolved_page_cuda_allowed=False,
        scored_experiment_allowed=False,
        benchmark_allowed=False,
        host_computed_output_hash_required=True,
        expected_hash_source="data/cuda/stage5z-prime-minus-one-cuda-validation-vectors.yaml",
        cuda_c_style_subset_required=True,
        implementation_status="implemented_synthetic_only",
        blockers=[],
    )
    records = [record]
    write_records(kernel_implementation_out, records)
    write_json_report(out_dir, REPORT_FILES["kernel_build"], {"records": records})
    return records
