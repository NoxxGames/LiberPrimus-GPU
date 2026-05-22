from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_contract.next_stage_decision import build_next_stage_decision


def test_stage5w_next_stage_decision_is_deterministic_and_not_cuda(tmp_path: Path) -> None:
    first = build_next_stage_decision(next_stage_decision_out=tmp_path / "decision1.yaml", out_dir=tmp_path)
    second = build_next_stage_decision(next_stage_decision_out=tmp_path / "decision2.yaml", out_dir=tmp_path)
    assert first == second
    selected = [record for record in first if record["selected"]]
    assert len(selected) == 1
    assert "no-GPU native parity execution" in selected[0]["recommended_stage_title"]
    assert selected[0]["recommended_prompt_type"] == "Codex"
    assert all(record["cuda_execution_allowed"] is False for record in first)
    assert all(record["unsolved_page_cuda_allowed"] is False for record in first)

