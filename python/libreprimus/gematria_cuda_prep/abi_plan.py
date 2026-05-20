"""Stage 5I CUDA-C ABI plan records for future Gematria shift kernel."""

from __future__ import annotations

from pathlib import Path

from libreprimus.gematria_cuda_prep.export import write_record_set, write_report, write_warnings
from libreprimus.gematria_cuda_prep.models import (
    ABI_PLAN_ID,
    ABI_PLAN_JSON,
    ABI_PLAN_PATH,
    ARITHMETIC_FORMULA,
    COMMON_POLICY_FLAGS,
    FUTURE_KERNEL_HEADER,
    FUTURE_KERNEL_SOURCE,
    OUTPUT_DIR,
)


def build_abi_plan_records(*, abi_plan_out: Path = ABI_PLAN_PATH, out_dir: Path = OUTPUT_DIR) -> list[dict[str, object]]:
    """Build C/POD ABI plan records without creating CUDA files."""

    record: dict[str, object] = {
        "record_type": "gematria_cuda_abi_plan_record",
        "abi_plan_id": ABI_PLAN_ID,
        "c_compatible_kernel_boundary": True,
        "device_code_subset_required": True,
        "stl_in_device_path_allowed": False,
        "exceptions_in_device_path_allowed": False,
        "dynamic_allocation_in_device_path_allowed": False,
        "strings_cross_kernel_boundary": False,
        "host_ownership_types_cross_kernel_boundary": False,
        "output_hashing_host_side": True,
        "future_kernel_header_expected": FUTURE_KERNEL_HEADER,
        "future_kernel_source_expected": FUTURE_KERNEL_SOURCE,
        "future_cuda_files_created": False,
        "future_kernel_signature_plan": (
            "gematria_shift_score_kernel(const uint8_t* token_values, "
            "const uint8_t* transformable_mask, const uint8_t* shifts, "
            "uint8_t* output_token_values, int token_count, int candidate_count, int* status_codes)"
        ),
        "buffer_layout": {
            "token_values": {"type": "const uint8_t*", "purpose": "input numeric tokens, including separator placeholders"},
            "transformable_mask": {"type": "const uint8_t*", "purpose": "1 for rune tokens, 0 for separators"},
            "shifts": {"type": "const uint8_t*", "purpose": "candidate shift values"},
            "output_token_values": {"type": "uint8_t*", "purpose": "candidate-major output tokens"},
            "token_count": {"type": "int", "purpose": "input token count"},
            "candidate_count": {"type": "int", "purpose": "shift candidate count"},
            "status_codes": {"type": "int*", "purpose": "optional per-candidate status codes"},
        },
        "output_index_formula": "output[candidate_index * token_count + token_index]",
        "device_formula": f"mask ? {ARITHMETIC_FORMULA} : token",
        "host_wrapper_policy": "C++ host wrappers may own buffers outside the device ABI only",
        **COMMON_POLICY_FLAGS,
    }
    records = [record]
    write_record_set(abi_plan_out, records)
    write_report(out_dir, ABI_PLAN_JSON, {"records": records})
    write_warnings(out_dir, [])
    return records
