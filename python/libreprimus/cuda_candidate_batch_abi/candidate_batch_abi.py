"""Build Candidate Batch ABI v0 records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cuda_candidate_batch_abi.export import write_record_set, write_report
from libreprimus.cuda_candidate_batch_abi.models import (
    ABI_ID,
    CANDIDATE_BATCH_ABI_PATH,
    CANDIDATE_BATCH_ABI_REPORT_JSON,
    COMMON_FLAGS,
    OUTPUT_DIR,
)


def build_candidate_batch_abi(
    *,
    candidate_batch_abi_out: Path = CANDIDATE_BATCH_ABI_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Define the top-level Candidate Batch ABI v0 contract."""

    record = {
        "record_type": "candidate_batch_abi_record",
        "candidate_batch_abi_record_id": "stage5u-candidate-batch-abi-v0",
        "abi_id": ABI_ID,
        "abi_version": 0,
        "abi_scope": "contract_only_no_execution",
        "token_domain": "gematria_index29_tokens_and_separator_metadata",
        "candidate_ordering": "candidate_major",
        "fixture_ordering": "manifest_order",
        "output_ordering": "candidate_major_then_token_position",
        "memory_layout": "structure_of_arrays_preferred",
        "host_orchestration": "python",
        "native_reference_backend": "cpp_cpu_future",
        "cuda_backend": "future_cuda_c_style_kernel_abi",
        "generated_body_publication_allowed": False,
        "compact_summary_only": True,
        "result_store_contract": "stage4p",
        "score_summary_contract": "stage4i",
        "benchmark_execution_allowed": False,
        "cuda_execution_allowed": False,
        "unsolved_page_cuda_allowed": False,
        "supported_surfaces": [
            "variable_length_token_buffers",
            "token_kind_metadata",
            "transformable_mask",
            "separator_positions",
            "candidate_shifts",
            "affine_parameters",
            "reverse_mode_flags",
            "rotated_reverse_parameters",
            "vigenere_key_schedule_buffers",
            "prime_minus_one_stream_schedule_buffers",
            "score_vector_outputs",
            "topk_candidate_outputs",
            "output_token_hashes",
            "compact_result_store_summaries",
        ],
        "rejected_surfaces": [
            "raw_page_text_input",
            "unsolved_page_input",
            "canonical_corpus_input",
            "generated_body_publication",
            "performance_claims",
            "method_status_upgrade_by_parity",
        ],
        "version_status": "defined_for_stage5v_conformance",
        **COMMON_FLAGS,
    }
    records = [record]
    write_record_set(candidate_batch_abi_out, records)
    write_report(out_dir, CANDIDATE_BATCH_ABI_REPORT_JSON, {"records": records})
    return records
