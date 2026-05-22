from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.cuda_solved_family_readiness.next_stage_decision import build_next_stage_decision


def _decisions() -> list[dict[str, object]]:
    return yaml.safe_load(Path("data/cuda/stage5t-cuda-next-stage-decision.yaml").read_text(encoding="utf-8"))[
        "records"
    ]


def test_stage5t_next_stage_decision_selects_stage5u() -> None:
    selected = [record for record in _decisions() if record["selected"]]
    assert len(selected) == 1
    decision = selected[0]
    assert decision["recommended_prompt_type"] == "Codex"
    assert decision["recommended_stage_title"] == "Stage 5U - unified candidate batch ABI and backend contract consolidation"
    assert decision["deep_research_recommended_next"] is False
    assert decision["cuda_execution_allowed"] is False


def test_stage5t_next_stage_decision_is_deterministic(tmp_path: Path) -> None:
    output = tmp_path / "decision.yaml"
    out_dir = tmp_path / "reports"
    records = build_next_stage_decision(
        batch_abi_gaps=Path("data/cuda/stage5t-cuda-candidate-batch-abi-gaps.yaml"),
        next_stage_decision_out=output,
        out_dir=out_dir,
    )
    selected = [record for record in records if record["selected"]]
    assert len(selected) == 1
    assert selected[0]["decision_id"] == "stage5u_unified_candidate_batch_abi"
