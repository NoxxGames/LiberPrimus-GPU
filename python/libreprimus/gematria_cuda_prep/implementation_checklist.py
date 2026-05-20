"""Stage 5J implementation checklist records prepared by Stage 5I."""

from __future__ import annotations

from pathlib import Path

from libreprimus.gematria_cuda_prep.export import write_record_set, write_report, write_warnings
from libreprimus.gematria_cuda_prep.models import (
    CHECKLIST_ID,
    CHECKLIST_PATH,
    COMMON_POLICY_FLAGS,
    IMPLEMENTATION_CHECKLIST_JSON,
    NATIVE_FIXTURE_HASH,
    OUTPUT_DIR,
)

CHECKLIST_ITEMS = [
    "add_gematria_shift_score_kernel_cuh_with_c_compatible_abi_only",
    "add_gematria_shift_score_kernel_cu_with_conservative_cuda_c_subset",
    "no_stl_in_cu_or_cuh",
    "no_exception_or_throw_in_cu_or_cuh",
    "no_dynamic_allocation_in_device_code",
    "no_real_liber_primus_data",
    "no_solved_fixture_cuda_execution",
    "no_unsolved_page_cuda_execution",
    "no_gpu_benchmark",
    "hash_output_host_side_after_copying_output_tokens",
    "compare_cuda_output_hash_to_stage5h_fixture_hash",
    "preserve_stage5f_az_synthetic_kernel",
    "update_cmake_only_behind_lpgpu_enable_cuda",
    "no_gpu_ci_path_must_pass",
    "optional_local_cuda_path_may_run_synthetic_numeric_fixture_only",
]


def build_implementation_checklist_records(
    *,
    checklist_out: Path = CHECKLIST_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, object]]:
    """Build Stage 5J implementation checklist records."""

    record: dict[str, object] = {
        "record_type": "gematria_cuda_implementation_checklist_record",
        "checklist_id": CHECKLIST_ID,
        "checklist_items": [{"item_id": item, "required": True, "status": "planned"} for item in CHECKLIST_ITEMS],
        "implementation_blockers": [],
        "stage5j_ready_for_synthetic_implementation": True,
        "stage5j_success_criteria": f"cuda_synthetic_gematria_hash_equals_{NATIVE_FIXTURE_HASH}",
        "real_liber_primus_cuda_data_blocked": True,
        "solved_fixture_cuda_execution_blocked": True,
        "unsolved_page_cuda_execution_blocked": True,
        "gpu_benchmark_blocked": True,
        **COMMON_POLICY_FLAGS,
    }
    records = [record]
    write_record_set(checklist_out, records)
    write_report(out_dir, IMPLEMENTATION_CHECKLIST_JSON, {"records": records})
    write_warnings(out_dir, [])
    return records
