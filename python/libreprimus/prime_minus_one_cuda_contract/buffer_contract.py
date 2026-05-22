"""Build Stage 5Z CUDA buffer contract records."""

from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_cuda_contract.export import write_json_report, write_records
from libreprimus.prime_minus_one_cuda_contract.models import BUFFER_CONTRACT_PATH, OUTPUT_DIR, base_record


def build_buffer_contract(buffer_contract_out: Path = BUFFER_CONTRACT_PATH, out_dir: Path = OUTPUT_DIR) -> list[dict]:
    specs = [
        ("token_values", "input", "uint8", "Gematria token values 0..28; separators use preserved token kind metadata."),
        ("token_kinds", "input", "uint8", "Rune/separator/cleartext token kind preservation."),
        ("transformable_mask", "input", "uint8", "1 for enciphered transformable rune tokens, 0 otherwise."),
        ("fixture_offsets_lengths", "input", "uint32", "Fixture token offsets and lengths in manifest order."),
        ("stream_schedule_values", "input", "uint8", "Prime-minus-one stream values computed as (prime_i - 1) mod 29."),
        ("stream_offsets_lengths", "input", "uint32", "Per-schedule offsets and lengths for candidate stream access."),
        ("candidate_fixture_stream_refs", "input", "uint32", "Candidate fixture indices and candidate stream start indices."),
        ("output_tokens", "output", "uint8", "Candidate-major output token values."),
        ("output_token_kinds", "output", "uint8", "Output token-kind preservation."),
        ("status_codes", "output", "int32", "Per-candidate success or validation failure status codes."),
        ("output_hash_policy", "host", "sha256", "Host-side canonical JSON token hash policy."),
    ]
    records = [
        base_record(
            "prime_minus_one_cuda_buffer_contract_record",
            "schemas/cuda/prime-minus-one-cuda-buffer-contract-record-v0.schema.json",
            buffer_contract_record_id=f"stage5z-buffer-{name}",
            buffer_name=name,
            buffer_direction=direction,
            element_type=element_type,
            description=description,
            memory_layout="structure_of_arrays",
            ordering="candidate_major_then_token_position",
            required_for_future_kernel=True,
            cuda_c_style_subset=True,
            implementation_allowed=False,
            cuda_execution_allowed=False,
        )
        for name, direction, element_type, description in specs
    ]
    write_records(buffer_contract_out, records)
    write_json_report(out_dir, "buffer_contract_report.json", {"records": records})
    return records
