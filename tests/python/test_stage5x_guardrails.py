from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_parity.guardrails import build_guardrails


def test_stage5x_guardrails_block_cuda_benchmark_raw_and_publication(tmp_path: Path) -> None:
    records = build_guardrails(guardrail_out=tmp_path / "guardrail.yaml", out_dir=tmp_path)
    assert len(records) == 7
    assert all(record["enforced"] is True for record in records)
    assert all(record["cuda_execution_performed"] is False for record in records)
    assert all(record["cuda_source_modified"] is False for record in records)
    assert all(record["new_cuda_kernels_added"] == 0 for record in records)
    assert all(record["gpu_benchmark_performed"] is False for record in records)
    assert all(record["raw_data_processed"] is False for record in records)
    assert all(record["generated_outputs_committed"] is False for record in records)
    assert all(record["solve_claim"] is False for record in records)
    assert all(record["cxx_launches_python_workers"] is False for record in records)
