"""Build Stage 5Z CUDA-C style kernel ABI records."""

from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_cuda_contract.export import write_json_report, write_records
from libreprimus.prime_minus_one_cuda_contract.models import KERNEL_ABI_PATH, KERNEL_ID, OUTPUT_DIR, base_record


def build_kernel_abi(kernel_abi_out: Path = KERNEL_ABI_PATH, out_dir: Path = OUTPUT_DIR) -> list[dict]:
    record = base_record(
        "prime_minus_one_cuda_kernel_abi_record",
        "schemas/cuda/prime-minus-one-cuda-kernel-abi-record-v0.schema.json",
        kernel_abi_record_id="stage5z-prime-minus-one-kernel-abi-v0",
        kernel_id=KERNEL_ID,
        abi_status="contract_only_not_implemented",
        cuda_c_style_subset=True,
        forbidden_cuda_features=[
            "std::array",
            "std::vector",
            "std::string",
            "std::span",
            "std::optional",
            "std::variant",
            "exceptions",
            "rtti",
            "dynamic_allocation",
            "iostreams",
            "lambdas",
        ],
        allowed_cuda_features=[
            "pod_structs",
            "fixed_size_c_arrays",
            "raw_pointers",
            "primitive_integer_types",
            "explicit_lengths",
            "status_codes",
        ],
        entrypoint_name="prime_minus_one_stream_candidate_kernel",
        input_buffers=[
            "token_values",
            "token_kinds",
            "transformable_mask",
            "fixture_offsets",
            "fixture_lengths",
            "stream_schedule_values",
            "stream_offsets",
            "stream_lengths",
            "candidate_fixture_indices",
            "candidate_stream_start_indices",
        ],
        output_buffers=["output_tokens", "output_token_kinds", "status_codes"],
        output_hash_location="host_side_after_kernel_completion",
        output_ordering="candidate_major_then_token_position",
        host_runner_implemented=False,
        cuda_kernel_implemented=False,
        cuda_source_modified=False,
        implementation_allowed=False,
        cuda_execution_allowed=False,
    )
    records = [record]
    write_records(kernel_abi_out, records)
    write_json_report(out_dir, "kernel_abi_report.json", {"records": records})
    return records
