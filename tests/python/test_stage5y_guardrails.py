from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_reporting.guardrails import build_guardrails


def test_stage5y_guardrails_all_pass_without_cuda_or_execution(tmp_path: Path) -> None:
    records = build_guardrails(guardrail_out=tmp_path / "guardrail.yaml", out_dir=tmp_path)
    assert len(records) == 9
    assert all(record["guardrail_status"] == "passed" for record in records)
    assert all(record["native_execution_performed"] is False for record in records)
    assert all(record["cuda_execution_performed"] is False for record in records)
    assert all(record["new_cuda_kernels_added"] == 0 for record in records)
    assert all(record["solve_claim"] is False for record in records)
