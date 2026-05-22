from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_parity.native_execution import build_native_run_records
from libreprimus.prime_minus_one_native_parity.next_stage_decision import build_next_stage_decision
from libreprimus.prime_minus_one_native_parity.parity_records import build_parity_records


def test_stage5x_next_stage_selects_stage5y_when_ready_mappings_pass(tmp_path: Path) -> None:
    run = tmp_path / "run.yaml"
    parity = tmp_path / "parity.yaml"
    decision = tmp_path / "decision.yaml"
    build_native_run_records(native_run_out=run, out_dir=tmp_path)
    build_parity_records(native_run=run, native_parity_out=parity, out_dir=tmp_path)
    records = build_next_stage_decision(native_parity=parity, next_stage_decision_out=decision, out_dir=tmp_path)
    selected = [record for record in records if record["selected"] is True]
    assert len(selected) == 1
    assert selected[0]["option_id"] == "stage5y_prime_minus_one_native_parity_reporting_integration"
    assert selected[0]["recommended_prompt_type"] == "Codex"
    assert selected[0]["cuda_execution_allowed"] is False
