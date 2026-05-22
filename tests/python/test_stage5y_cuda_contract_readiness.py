from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_reporting.cuda_contract_readiness import build_cuda_contract_readiness_gate
from libreprimus.prime_minus_one_native_reporting.parity_report import build_parity_report
from libreprimus.prime_minus_one_native_reporting.result_store_integration import build_result_store_integration
from libreprimus.prime_minus_one_native_reporting.score_summary_integration import build_score_summary_integration


def test_stage5y_cuda_contract_readiness_gate_allows_only_contract_prep(tmp_path: Path) -> None:
    parity = tmp_path / "parity.yaml"
    result = tmp_path / "result.yaml"
    score = tmp_path / "score.yaml"
    build_parity_report(parity_report_out=parity, out_dir=tmp_path)
    build_result_store_integration(parity_report=parity, result_store_integration_out=result, out_dir=tmp_path)
    build_score_summary_integration(parity_report=parity, score_summary_integration_out=score, out_dir=tmp_path)
    records = build_cuda_contract_readiness_gate(
        parity_report=parity,
        result_store_integration=result,
        score_summary_integration=score,
        cuda_contract_readiness_gate_out=tmp_path / "gate.yaml",
        out_dir=tmp_path,
    )
    assert len(records) == 1
    record = records[0]
    assert record["prime_minus_one_cuda_contract_preparation_ready"] is True
    assert record["cuda_execution_allowed"] is False
    assert record["cuda_source_changes_allowed"] is False
    assert record["new_kernel_allowed"] is False
    assert record["benchmark_execution_allowed"] is False
