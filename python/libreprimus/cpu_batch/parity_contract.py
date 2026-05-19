"""CPU/CUDA parity contract records for future GPU work."""

from __future__ import annotations


def parity_contract_record() -> dict:
    """Return the Stage 4H parity contract record."""

    return {
        "record_type": "cpu_cuda_parity_contract",
        "parity_contract_version": "cpu-cuda-parity-contract-v0",
        "cpu_reference_package": "libreprimus.cpu_batch",
        "cuda_implementation_status": "deferred",
        "required_semantics": [
            "Token order is preserved exactly from normalized input stream records.",
            "Only token_kind=rune participates in modulo-29 transforms.",
            "Separators and unknown symbols are preserved or skipped exactly as the CPU adapter records.",
            "Modulo arithmetic is over Z_29 and must match the CPU transform registry definitions.",
            "Vigenere key advancement and skip rules must match solved_fixtures.vigenere.",
            "Prime stream values, reset behavior, and payload skips must match solved_fixtures.prime_stream.",
            "Scoring compatibility requires byte-for-byte matching output text before score comparison.",
            "Output text hashes and output token hashes are the parity comparison anchors.",
        ],
        "required_result_fields": [
            "candidate_id",
            "input_stream_id",
            "transform_id",
            "canonical_transform_id",
            "transform_parameters",
            "output_text_hash",
            "output_token_hash",
            "score_summary",
            "cuda_used",
            "no_solve_claim",
        ],
        "cpu_only": True,
        "cuda_used": False,
        "cuda_required": False,
        "no_solve_claim": True,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "notes": [
            "Stage 4H defines the parity contract only; no CUDA implementation is added.",
            "Future CUDA transforms must match these CPU records before any acceleration result is trusted.",
        ],
    }
