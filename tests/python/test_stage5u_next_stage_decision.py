from __future__ import annotations

from pathlib import Path

from libreprimus.cuda_candidate_batch_abi.gap_closure import build_gap_closure
from libreprimus.cuda_candidate_batch_abi.next_stage_decision import build_next_stage_decision


def test_stage5u_next_stage_decision_selects_stage5v_native_adapter(tmp_path: Path) -> None:
    gaps = tmp_path / "gaps.yaml"
    build_gap_closure(
        stage5t_gaps=Path("data/cuda/stage5t-cuda-candidate-batch-abi-gaps.yaml"),
        gap_closure_out=gaps,
        out_dir=tmp_path / "gap_reports",
    )
    records = build_next_stage_decision(
        gap_closure=gaps,
        next_stage_decision_out=tmp_path / "decisions.yaml",
        out_dir=tmp_path / "reports",
    )
    selected = [record for record in records if record["selected"]]
    assert len(selected) == 1
    assert selected[0]["recommended_stage_title"] == "Stage 5V - native candidate batch ABI reference adapter and conformance fixtures"
    assert selected[0]["recommended_prompt_type"] == "Codex"
    assert selected[0]["deep_research_recommended_next"] is False
    assert selected[0]["cuda_execution_allowed"] is False


def test_stage5u_next_stage_keeps_deep_research_unselected(tmp_path: Path) -> None:
    gaps = tmp_path / "gaps.yaml"
    build_gap_closure(
        stage5t_gaps=Path("data/cuda/stage5t-cuda-candidate-batch-abi-gaps.yaml"),
        gap_closure_out=gaps,
        out_dir=tmp_path / "gap_reports2",
    )
    records = build_next_stage_decision(
        gap_closure=gaps,
        next_stage_decision_out=tmp_path / "decisions2.yaml",
        out_dir=tmp_path / "reports2",
    )
    deep_research = [record for record in records if record["recommended_prompt_type"] == "Deep Research"]
    assert deep_research
    assert all(record["selected"] is False for record in deep_research)
