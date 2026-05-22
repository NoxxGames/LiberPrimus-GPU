from __future__ import annotations

from pathlib import Path

from libreprimus.native_candidate_batch_conformance.next_stage_decision import build_next_stage_decision


def test_stage5v_next_stage_decision_is_deterministic_and_not_cuda(tmp_path: Path) -> None:
    records = build_next_stage_decision(next_stage_decision_out=tmp_path / "decision.yaml", out_dir=tmp_path / "out")
    selected = [record for record in records if record["selected"] is True]
    assert len(selected) == 1
    assert selected[0]["recommended_stage_title"] == "Stage 5W - prime-minus-one stream native parity contract preparation"
    assert selected[0]["deep_research_recommended_next"] is False
    assert all(record["cuda_execution_allowed"] is False for record in records)
    assert all(record["benchmark_execution_allowed"] is False for record in records)
