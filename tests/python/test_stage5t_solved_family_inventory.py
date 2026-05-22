from __future__ import annotations

from pathlib import Path

import yaml


def _inventory() -> list[dict[str, object]]:
    return yaml.safe_load(Path("data/cuda/stage5t-solved-family-cuda-inventory.yaml").read_text(encoding="utf-8"))[
        "records"
    ]


def test_stage5t_inventory_includes_expected_solved_families() -> None:
    family_ids = {record["solved_family_id"] for record in _inventory()}
    assert {
        "direct_translation",
        "reverse_gematria",
        "rotated_reverse_gematria",
        "vigenere_explicit_key",
        "prime_minus_one_stream",
        "gematria_shift_score_only",
        "synthetic_shift_score",
        "synthetic_gematria_mod29",
    } <= family_ids


def test_stage5t_inventory_distinguishes_shift_score_from_original_transforms() -> None:
    records = {record["solved_family_id"]: record for record in _inventory()}
    assert records["gematria_shift_score_only"]["verified_current_kernel_parity"] is True
    assert records["direct_translation"]["verified_current_kernel_parity"] is False
    assert records["direct_translation"]["original_transform_semantics_cuda_verified"] is False
    assert records["vigenere_explicit_key"]["readiness_status"] == "needs_batch_abi"
    assert records["prime_minus_one_stream"]["readiness_status"] == "needs_batch_abi"


def test_stage5t_inventory_has_no_execution_or_solve_flags() -> None:
    for record in _inventory():
        assert record["cuda_execution_performed"] is False
        assert record["cuda_source_modified"] is False
        assert record["new_cuda_kernel_added"] is False
        assert record["gpu_benchmark_performed"] is False
        assert record["solve_claim"] is False
        assert record["no_solve_claim"] is True
