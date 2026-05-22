"""Build the Stage 5T CUDA parity/readiness matrix."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cuda_solved_family_readiness.export import read_mapping, read_record_set, write_record_set, write_report
from libreprimus.cuda_solved_family_readiness.models import (
    COMMON_FLAGS,
    INVENTORY_PATH,
    OUTPUT_DIR,
    PARITY_MATRIX_PATH,
    PARITY_MATRIX_REPORT_JSON,
    STAGE5M_SUMMARY,
    STAGE5R_SUMMARY,
)


def build_parity_matrix(
    *,
    inventory: Path = INVENTORY_PATH,
    stage5m_summary: Path = STAGE5M_SUMMARY,
    stage5r_summary: Path = STAGE5R_SUMMARY,
    parity_matrix_out: Path = PARITY_MATRIX_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    """Classify each solved family against existing CUDA parity coverage."""

    inventory_records = read_record_set(inventory)
    stage5m = read_mapping(stage5m_summary)
    stage5r = read_mapping(stage5r_summary)
    records: list[dict[str, Any]] = []
    for index, item in enumerate(inventory_records):
        family = item["solved_family_id"]
        status, blockers, original_verified = _classify_family(family)
        verified_count = _verified_count(family, stage5m, stage5r)
        records.append(
            {
                "record_type": "solved_family_cuda_parity_matrix_record",
                "parity_matrix_id": f"stage5t-parity-matrix-{index:02d}",
                "solved_family_id": family,
                "fixture_class": item["fixture_class"],
                "readiness_status": status,
                "verified_current_kernel_parity_count": verified_count,
                "original_transform_semantics_cuda_verified": original_verified,
                "gematria_shift_score_only_parity": family in {"direct_translation", "gematria_shift_score_only"},
                "stage5m_reference_count": stage5m.get("parity_pass_count", 0),
                "stage5r_reference_count": stage5r.get("parity_pass_count", 0),
                "blockers": blockers,
                "rationale": _rationale(family, status),
                **COMMON_FLAGS,
            }
        )
    write_record_set(parity_matrix_out, records)
    write_report(out_dir, PARITY_MATRIX_REPORT_JSON, {"records": records})
    return records


def _classify_family(family: str) -> tuple[str, list[str], bool]:
    if family in {"synthetic_shift_score", "synthetic_gematria_mod29", "gematria_shift_score_only"}:
        return "cuda_parity_verified_existing_kernel", [], family == "gematria_shift_score_only"
    if family == "direct_translation":
        return "cuda_parity_ready_existing_kernel", ["original_transform_semantics_not_cuda_verified"], False
    if family in {"vigenere_explicit_key", "prime_minus_one_stream"}:
        return "needs_batch_abi", ["needs_cuda_kernel_contract", "needs_batch_abi"], False
    return "blocked_original_transform_contract", ["needs_cuda_kernel_contract", "blocked_original_transform_contract"], False


def _verified_count(family: str, stage5m: dict[str, Any], stage5r: dict[str, Any]) -> int:
    if family == "gematria_shift_score_only":
        return int(stage5m.get("parity_pass_count", 0)) + int(stage5r.get("parity_pass_count", 0))
    if family in {"synthetic_shift_score", "synthetic_gematria_mod29"}:
        return 1
    return 0


def _rationale(family: str, status: str) -> str:
    if family == "direct_translation":
        return "Direct fixture buffers were used for shift-score parity, but direct translation has no CUDA transform semantics yet."
    if status == "cuda_parity_verified_existing_kernel":
        return "Existing scoped CUDA parity is verified for this kernel surface."
    if status == "needs_batch_abi":
        return "The solved family needs shared batch ABI surfaces before a CUDA contract can be responsible."
    return "The solved family needs an original transform-family contract before CUDA readiness can advance."
