from __future__ import annotations

from pathlib import Path

import yaml


def _matrix() -> dict[str, dict[str, object]]:
    records = yaml.safe_load(Path("data/cuda/stage5t-solved-family-cuda-parity-matrix.yaml").read_text(encoding="utf-8"))[
        "records"
    ]
    return {record["solved_family_id"]: record for record in records}


def test_stage5t_shift_score_cuda_parity_is_current_kernel_only() -> None:
    matrix = _matrix()
    assert matrix["gematria_shift_score_only"]["readiness_status"] == "cuda_parity_verified_existing_kernel"
    assert matrix["gematria_shift_score_only"]["verified_current_kernel_parity_count"] == 8
    assert matrix["direct_translation"]["readiness_status"] == "cuda_parity_ready_existing_kernel"
    assert matrix["direct_translation"]["original_transform_semantics_cuda_verified"] is False


def test_stage5t_original_transform_families_are_not_marked_cuda_verified() -> None:
    matrix = _matrix()
    for family in (
        "reverse_gematria",
        "rotated_reverse_gematria",
        "vigenere_explicit_key",
        "prime_minus_one_stream",
    ):
        assert matrix[family]["original_transform_semantics_cuda_verified"] is False
        assert matrix[family]["verified_current_kernel_parity_count"] == 0


def test_stage5t_matrix_keeps_blockers_explicit() -> None:
    matrix = _matrix()
    assert "needs_batch_abi" in matrix["vigenere_explicit_key"]["blockers"]
    assert "needs_batch_abi" in matrix["prime_minus_one_stream"]["blockers"]
    assert "blocked_original_transform_contract" in matrix["reverse_gematria"]["blockers"]
