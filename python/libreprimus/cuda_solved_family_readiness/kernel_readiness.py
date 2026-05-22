"""Build Stage 5T future-kernel readiness rankings."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cuda_solved_family_readiness.export import read_record_set, write_record_set, write_report
from libreprimus.cuda_solved_family_readiness.models import COMMON_FLAGS, KERNEL_READINESS_PATH, KERNEL_READINESS_REPORT_JSON, OUTPUT_DIR, PARITY_MATRIX_PATH


def build_kernel_readiness(
    *,
    parity_matrix: Path = PARITY_MATRIX_PATH,
    kernel_readiness_out: Path = KERNEL_READINESS_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Rank future CUDA work without authorizing implementation."""

    matrix = read_record_set(parity_matrix)
    rows = [
        ("gematria_shift_score_only", 1, "verified_existing_kernel", "low", "No new implementation; retain as parity control."),
        ("prime_minus_one_stream", 2, "ready_for_contract_review_after_abi", "medium", "High-value stream family, but stream schedule ABI is missing."),
        ("vigenere_explicit_key", 3, "ready_for_contract_review_after_abi", "medium", "High-value explicit-key family, but key schedule ABI is missing."),
        ("reverse_gematria", 4, "needs_cuda_kernel_contract", "low", "Simple original transform semantics need a separate contract."),
        ("rotated_reverse_gematria", 5, "needs_cuda_kernel_contract", "medium", "Rotation parameter ABI and original semantics need a separate contract."),
        ("direct_translation", 6, "not_cuda_kernel_priority", "low", "Direct translation is useful for fixtures but not a meaningful next CUDA kernel."),
        ("top_k_reducer", 7, "future_reducer_after_score_vector", "medium", "Reducer work belongs after unified batch and score-vector surfaces."),
    ]
    matrix_by_family = {record["solved_family_id"]: record for record in matrix}
    records = [
        {
            "record_type": "cuda_kernel_readiness_record",
            "kernel_readiness_id": f"stage5t-kernel-readiness-{rank:02d}",
            "candidate_family_id": family,
            "priority_rank": rank,
            "readiness_status": status,
            "risk_level": risk,
            "implementation_allowed_now": False,
            "requires_batch_abi": family in {"prime_minus_one_stream", "vigenere_explicit_key", "top_k_reducer"},
            "requires_new_cuda_kernel_contract": family not in {"gematria_shift_score_only", "direct_translation"},
            "source_parity_status": matrix_by_family.get(family, {}).get("readiness_status", "not_applicable"),
            "rationale": rationale,
            **COMMON_FLAGS,
        }
        for family, rank, status, risk, rationale in rows
    ]
    write_record_set(kernel_readiness_out, records)
    write_report(out_dir, KERNEL_READINESS_REPORT_JSON, {"records": records})
    return records
