from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_reporting.cuda_contract_readiness import build_cuda_contract_readiness_gate
from libreprimus.prime_minus_one_native_reporting.next_stage_decision import build_next_stage_decision
from libreprimus.prime_minus_one_native_reporting.parity_report import build_parity_report
from libreprimus.prime_minus_one_native_reporting.result_store_integration import build_result_store_integration
from libreprimus.prime_minus_one_native_reporting.score_summary_integration import build_score_summary_integration


def test_stage5y_next_stage_decision_selects_stage5z_contract_prep(tmp_path: Path) -> None:
    parity = tmp_path / "parity.yaml"
    result = tmp_path / "result.yaml"
    score = tmp_path / "score.yaml"
    gate = tmp_path / "gate.yaml"
    build_parity_report(parity_report_out=parity, out_dir=tmp_path)
    build_result_store_integration(parity_report=parity, result_store_integration_out=result, out_dir=tmp_path)
    build_score_summary_integration(parity_report=parity, score_summary_integration_out=score, out_dir=tmp_path)
    build_cuda_contract_readiness_gate(
        parity_report=parity,
        result_store_integration=result,
        score_summary_integration=score,
        cuda_contract_readiness_gate_out=gate,
        out_dir=tmp_path,
    )
    records = build_next_stage_decision(
        cuda_contract_readiness_gate=gate,
        next_stage_decision_out=tmp_path / "decision.yaml",
        out_dir=tmp_path,
    )
    selected = [record for record in records if record["selected"] is True]
    assert len(selected) == 1
    assert selected[0]["option_id"] == "stage5z_prime_minus_one_cuda_contract_preparation"
    assert selected[0]["recommended_prompt_type"] == "Codex"
    assert all(record["cuda_execution_allowed"] is False for record in records)
    assert all(record["benchmark_execution_allowed"] is False for record in records)
