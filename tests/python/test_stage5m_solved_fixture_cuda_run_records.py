from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.gematria_solved_fixture_cuda.run_records import build_run_records


def _records(path: str) -> list[dict[str, object]]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"]


def test_stage5m_run_records_represent_exact_stage5l_mappings() -> None:
    records = _records("data/cuda/stage5m-gematria-solved-fixture-cuda-run.yaml")
    assert len(records) == 5
    assert [record["mapping_id"] for record in records] == [
        "stage5h-solved-fixture-safe-mapping-00",
        "stage5h-solved-fixture-safe-mapping-01",
        "stage5h-solved-fixture-safe-mapping-02",
        "stage5h-solved-fixture-safe-mapping-03",
        "stage5h-solved-fixture-safe-mapping-04",
    ]
    assert {record["solved_fixture_cuda_execution_scope"] for record in records} == {
        "exact_stage5l_mapped_token_buffers_only"
    }


def test_stage5m_run_records_preserve_safety_flags() -> None:
    records = _records("data/cuda/stage5m-gematria-solved-fixture-cuda-run.yaml")
    for record in records:
        assert record["executed_kernel"] == "gematria_mod29_shift_score_kernel"
        assert record["executed_semantics"] == "gematria_shift_score_only"
        assert record["original_transform_family_semantics_exercised"] is False
        assert record["unsolved_page_cuda_used"] is False
        assert record["real_liber_primus_cuda_data_used"] is False
        assert record["gpu_benchmark_performed"] is False
        assert record["performance_claim"] is False
        assert record["speedup_claim"] is False
        assert record["canonical_corpus_active"] is False
        assert record["page_boundaries_final"] is False
        assert record["no_solve_claim"] is True
        assert record["solve_claim"] is False


def test_stage5m_run_record_builder_is_no_gpu_safe_before_run(tmp_path: Path) -> None:
    output = tmp_path / "run.yaml"
    out_dir = tmp_path / "reports"
    records = build_run_records(run_records_out=output, out_dir=out_dir)
    assert len(records) == 5
    assert output.is_file()
    assert (out_dir / "cuda_run_report.json").is_file()
    assert all(record["cuda_run_status"] == "pending" for record in records)
    assert all(record["cuda_run_attempted"] is False for record in records)
