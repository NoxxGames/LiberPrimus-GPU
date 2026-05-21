from __future__ import annotations

from pathlib import Path

import yaml


def _records(path: str) -> list[dict[str, object]]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"]


def test_stage5n_parity_report_contains_all_five_stage5m_records() -> None:
    records = _records("data/cuda/stage5n-gematria-solved-fixture-cuda-report.yaml")
    assert len(records) == 5
    assert {record["parity_status"] for record in records} == {"passed"}
    assert {record["mapping_id"] for record in records} == {
        "stage5h-solved-fixture-safe-mapping-00",
        "stage5h-solved-fixture-safe-mapping-01",
        "stage5h-solved-fixture-safe-mapping-02",
        "stage5h-solved-fixture-safe-mapping-03",
        "stage5h-solved-fixture-safe-mapping-04",
    }


def test_stage5n_parity_report_rejects_performance_claims() -> None:
    records = _records("data/cuda/stage5n-gematria-solved-fixture-cuda-report.yaml")
    assert all(record["gpu_benchmark_performed"] is False for record in records)
    assert all(record["performance_claim"] is False for record in records)
    assert all(record["speedup_claim"] is False for record in records)
    assert all(record["not_production_broad_cuda_readiness"] is True for record in records)
