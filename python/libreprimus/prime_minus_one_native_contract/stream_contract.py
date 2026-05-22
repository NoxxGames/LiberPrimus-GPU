"""Prime-minus-one stream contract records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.prime_minus_one_native_contract.export import write_json_report, write_records
from libreprimus.prime_minus_one_native_contract.models import ABI_ID, COMMON_FLAGS, CONTRACT_ID, FAMILY_ID, OUTPUT_DIR, REPORT_FILES, STREAM_CONTRACT_PATH


def build_stream_contract(*, stream_contract_out: Path = STREAM_CONTRACT_PATH, out_dir: Path = OUTPUT_DIR) -> list[dict[str, Any]]:
    records = [
        {
            **COMMON_FLAGS,
            "record_type": "prime_minus_one_stream_contract_record",
            "schema": "schemas/cuda/prime-minus-one-stream-contract-record-v0.schema.json",
            "contract_id": CONTRACT_ID,
            "family_id": FAMILY_ID,
            "contract_status": "ready_for_stage5x_bounded_native_parity_execution",
            "candidate_batch_abi_id": ABI_ID,
            "token_domain": "0..28",
            "modulus": 29,
            "stream_source": "ordered_prime_sequence",
            "stream_formula": "(prime_i - 1) mod 29",
            "prime_index_base": 0,
            "stream_start_index_policy": "per_candidate_stream_start_index_required",
            "advance_policy": "advance_on_enciphered_transformable_rune_tokens_only",
            "reset_policy": "reset_per_fixture_or_manifest_declared",
            "separator_policy": "separators_do_not_advance_stream",
            "skip_policy": "cleartext_pass_through_tokens_do_not_advance_stream",
            "direction_policy": "forward_decrypt_subtract_prime_minus_one_stream",
            "ciphertext_to_plaintext_formula": "plaintext_token = (ciphertext_token - ((prime_i - 1) mod 29)) mod 29",
            "plaintext_to_ciphertext_formula": "ciphertext_token = (plaintext_token + ((prime_i - 1) mod 29)) mod 29",
            "source_backing_status": "source_backed_by_stage1d_fixture_registry_and_reference_code",
            "requires_native_execution_stage": True,
            "requires_cuda_kernel_contract": True,
            "blockers": [],
        },
        {
            **COMMON_FLAGS,
            "record_type": "prime_minus_one_stream_contract_record",
            "schema": "schemas/cuda/prime-minus-one-stream-contract-record-v0.schema.json",
            "contract_id": "prime_minus_one_stream_full_p56_token_buffer_blocker_v0",
            "family_id": FAMILY_ID,
            "contract_status": "blocked_full_p56_token_buffer_not_committed",
            "candidate_batch_abi_id": ABI_ID,
            "token_domain": "0..28",
            "modulus": 29,
            "stream_source": "ordered_prime_sequence",
            "stream_formula": "(prime_i - 1) mod 29",
            "prime_index_base": 0,
            "stream_start_index_policy": "per_candidate_stream_start_index_required",
            "advance_policy": "advance_on_enciphered_transformable_rune_tokens_only",
            "reset_policy": "reset_per_fixture_or_manifest_declared",
            "separator_policy": "separators_do_not_advance_stream",
            "skip_policy": "cleartext_pass_through_tokens_do_not_advance_stream",
            "direction_policy": "forward_decrypt_subtract_prime_minus_one_stream",
            "ciphertext_to_plaintext_formula": "plaintext_token = (ciphertext_token - ((prime_i - 1) mod 29)) mod 29",
            "plaintext_to_ciphertext_formula": "ciphertext_token = (plaintext_token + ((prime_i - 1) mod 29)) mod 29",
            "source_backing_status": "formula_source_backed_but_full_p56_cipher_token_buffer_missing",
            "requires_native_execution_stage": True,
            "requires_cuda_kernel_contract": True,
            "blockers": ["needs_full_committed_p56_cipher_token_buffer_before_full_fixture_native_execution"],
        },
    ]
    write_records(stream_contract_out, records)
    write_json_report(out_dir, REPORT_FILES["stream_contract"], {"records": records})
    return records
