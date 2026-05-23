from __future__ import annotations

from libreprimus.source_harvester.summary import build_next_stage_decision


def test_stage5af_next_stage_decision_is_deterministic() -> None:
    records = build_next_stage_decision(tool_validation_clean=True)
    selected = [record for record in records if record["selected"]]
    assert len(selected) == 1
    assert selected[0]["option_id"] == "stage5ag_run_source_harvester_on_user_downloads"
    assert selected[0]["recommended_next_prompt_type"] == "Codex"
    assert selected[0]["deep_research_recommended_next"] is False
    assert all(record["execution_enabled"] is False for record in records)


def test_stage5af_gap_closure_selected_when_validation_fails() -> None:
    records = build_next_stage_decision(tool_validation_clean=False)
    selected = [record for record in records if record["selected"]]
    assert selected[0]["option_id"] == "stage5ag_harvester_gap_closure"
    assert selected[0]["scored_experiment_recommended_next"] is False
    assert selected[0]["unsolved_page_cuda_recommended_next"] is False
