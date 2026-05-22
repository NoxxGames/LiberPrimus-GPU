"""Build Stage 5Z prime-minus-one CUDA contract records."""

from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_cuda_contract.export import write_json_report, write_records, write_warnings
from libreprimus.prime_minus_one_cuda_contract.models import CUDA_CONTRACT_ID, CUDA_CONTRACT_PATH, KERNEL_ID, OUTPUT_DIR, base_record


def build_contract_records(cuda_contract_out: Path = CUDA_CONTRACT_PATH, out_dir: Path = OUTPUT_DIR) -> list[dict]:
    records = [
        base_record(
            "prime_minus_one_cuda_contract_record",
            "schemas/cuda/prime-minus-one-cuda-contract-record-v0.schema.json",
            contract_record_id="stage5z-prime-minus-one-cuda-contract-v0",
            contract_status="complete_contract_preparation_only",
            family_id="prime_minus_one_stream",
            supported_family="prime_minus_one_stream",
            future_kernel_id=KERNEL_ID,
            token_domain="0..28",
            modulus=29,
            stream_source="ordered_prime_sequence",
            stream_formula="(prime_i - 1) mod 29",
            decryption_formula="plaintext_token = (ciphertext_token - ((prime_i - 1) mod 29)) mod 29",
            encryption_formula="ciphertext_token = (plaintext_token + ((prime_i - 1) mod 29)) mod 29",
            advance_policy="advance_on_enciphered_transformable_rune_tokens_only",
            reset_policy="reset_per_fixture_or_manifest_declared",
            separator_policy="separators_do_not_advance_stream",
            skip_policy="cleartext_pass_through_tokens_do_not_advance_stream",
            output_ordering="candidate_major_then_token_position",
            output_hash_algorithm="sha256_canonical_json_v1",
            supported_mapping_ids=[
                "stage5w-mapping-synthetic-prime-control-v0",
                "stage5w-mapping-p56-stage4o-bounded-v0",
            ],
            blocked_mapping_ids=["stage5w-mapping-p56-full-fixture-blocked-v0"],
            contract_preparation_complete=True,
            cuda_contract_readiness_status="ready_for_synthetic_kernel_contract_implementation_stage",
            implementation_allowed=False,
            cuda_execution_allowed=False,
            benchmark_allowed=False,
            blockers=[],
        ),
        base_record(
            "prime_minus_one_cuda_contract_record",
            "schemas/cuda/prime-minus-one-cuda-contract-record-v0.schema.json",
            contract_record_id="stage5z-prime-minus-one-full-p56-contract-blocker-v0",
            contract_status="blocked_full_p56_token_buffer_missing",
            family_id="prime_minus_one_stream",
            future_kernel_id=KERNEL_ID,
            token_domain="0..28",
            modulus=29,
            stream_source="ordered_prime_sequence",
            stream_formula="(prime_i - 1) mod 29",
            output_ordering="candidate_major_then_token_position",
            output_hash_algorithm="sha256_canonical_json_v1",
            supported_mapping_ids=[],
            blocked_mapping_ids=["stage5w-mapping-p56-full-fixture-blocked-v0"],
            contract_preparation_complete=True,
            full_p56_status="blocked_full_p56_token_buffer_missing",
            implementation_allowed=False,
            cuda_execution_allowed=False,
            benchmark_allowed=False,
            blockers=["needs_full_committed_p56_cipher_token_buffer_before_full_fixture_cuda_execution"],
        ),
    ]
    write_records(cuda_contract_out, records)
    write_json_report(out_dir, "cuda_contract_report.json", {"records": records})
    write_warnings(out_dir, [])
    return records


__all__ = ["build_contract_records", "CUDA_CONTRACT_ID"]
