from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5n_boundary_review_confirms_exact_stage5m_scope_only() -> None:
    record = yaml.safe_load(Path("data/cuda/stage5n-gematria-cuda-boundary-review.yaml").read_text(encoding="utf-8"))["records"][0]
    assert record["stage5m_scope_exact_stage5l_mapped_token_buffers_only"] is True
    assert record["stage5m_executed_semantics"] == "gematria_shift_score_only"
    assert record["additional_fixture_classes_authorized"] is False
    assert record["unsolved_page_cuda_authorized"] is False


def test_stage5n_boundary_review_does_not_validate_non_shift_family_semantics() -> None:
    record = yaml.safe_load(Path("data/cuda/stage5n-gematria-cuda-boundary-review.yaml").read_text(encoding="utf-8"))["records"][0]
    assert record["non_shift_original_transform_family_semantics_validated"] is False
    assert record["new_cuda_kernel_added"] is False
    assert record["new_cuda_kernels_added"] == 0
    assert record["cuda_source_modified"] is False
    assert record["device_kernel_arithmetic_modified"] is False
