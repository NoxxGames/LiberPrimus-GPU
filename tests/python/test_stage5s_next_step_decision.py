from __future__ import annotations

from pathlib import Path

import yaml


def _records(path: str) -> list[dict[str, object]]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"]


def test_stage5s_next_step_decision_selects_deep_research_review() -> None:
    records = _records("data/cuda/stage5s-gematria-expanded-cuda-next-step-decision.yaml")
    selected = [record for record in records if record["selected"]]
    assert len(selected) == 1
    decision = selected[0]
    assert decision["decision_class"] == "deep_research_project_review"
    assert decision["decision_status"] == "recommended"
    assert decision["deep_research_recommended"] is True
    assert decision["selected_next_prompt"] == (
        "Deep Research - Stage 5M-5S CUDA parity arc project review and next-direction assessment"
    )
    assert decision["additional_solved_fixture_candidate_status"] == "strategic_ambiguity_review_first"
    assert decision["original_transform_family_contract_status"] == "blocked_pending_contract_review"
    assert decision["broad_solved_fixture_cuda_status"] == "blocked_broad_scope"
    assert decision["unsolved_page_cuda_status"] == "blocked_unsolved"


def test_stage5s_next_step_decision_keeps_cuda_scope_blocked() -> None:
    records = _records("data/cuda/stage5s-gematria-expanded-cuda-next-step-decision.yaml")
    statuses = {record["decision_class"]: record["decision_status"] for record in records}
    assert statuses["unsolved_page_cuda"] == "blocked_unsolved"
    assert statuses["broad_solved_fixture_cuda_campaign"] == "blocked_broad_scope"
    assert statuses["original_transform_family_cuda_contract_review"] == "blocked_pending_contract_review"
