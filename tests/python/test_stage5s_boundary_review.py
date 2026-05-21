from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5s_boundary_review_preserves_no_unsolved_no_benchmark_scope() -> None:
    record = yaml.safe_load(
        Path("data/cuda/stage5s-gematria-expanded-cuda-boundary-review.yaml").read_text(encoding="utf-8")
    )["records"][0]
    assert record["stage5r_exact_scope_confirmed"] is True
    assert record["exact_approved_scope"] == "exact_three_stage5q_mapped_direct_translation_candidates_only"
    assert record["consumed_controls_excluded"] is True
    assert record["blocked_original_family_fixtures_excluded"] is True
    assert record["original_transform_family_semantics_exercised"] is False
    assert record["stage5r_validated_original_direct_translation_semantics"] is False
    assert record["stage5r_authorized_additional_fixture_classes"] is False
    assert record["stage5r_authorized_unsolved_page_cuda"] is False
    assert record["stage5r_authorized_generated_body_publication"] is False
    assert record["stage5r_authorized_benchmarks"] is False
    assert record["unsolved_page_cuda_used"] is False
    assert record["real_liber_primus_cuda_data_used"] is False
    assert record["canonical_corpus_active"] is False
    assert record["page_boundaries_final"] is False
    assert record["gpu_benchmark_performed"] is False
    assert record["speedup_claim"] is False
    assert record["new_cuda_kernels_added"] == 0
