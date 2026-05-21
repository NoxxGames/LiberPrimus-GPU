from __future__ import annotations

import yaml


def test_stage5r_boundary_records_preserve_cuda_scope() -> None:
    records = yaml.safe_load(open("data/cuda/stage5r-gematria-expanded-solved-fixture-cuda-boundary.yaml", encoding="utf-8"))["records"]
    assert len(records) == 1
    record = records[0]
    assert record["approved_stage5r_scope"] == "exact_three_stage5q_mapped_direct_translation_candidates_only"
    assert record["run_records"] == 3
    assert record["consumed_controls_excluded"] is True
    assert record["blocked_original_family_fixtures_excluded"] is True
    assert record["original_transform_family_semantics_exercised"] is False
    assert record["unsolved_page_cuda_used"] is False
    assert record["real_liber_primus_cuda_data_used"] is False
    assert record["new_cuda_kernels_added"] == 0
    assert record["device_kernel_arithmetic_modified"] is False
    assert record["gpu_benchmark_performed"] is False
    assert record["performance_claim"] is False
    assert record["speedup_claim"] is False
    assert record["canonical_corpus_active"] is False
    assert record["page_boundaries_final"] is False
    assert record["solve_claim"] is False
    assert record["cxx_launches_python_workers"] is False
