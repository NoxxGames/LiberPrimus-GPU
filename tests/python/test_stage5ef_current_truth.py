from __future__ import annotations

from libreprimus.token_block import stage5ef
from test_stage5ef_common import ensure_stage5ef_built, load_yaml


def test_stage5ef_current_truth_authority_is_single_registry() -> None:
    ensure_stage5ef_built()

    result = stage5ef.validate_stage5ef_current_truth()
    policy = load_yaml("data/project-state/stage5ef-current-truth-authority-policy.yaml")
    current = load_yaml("data/project-state/current-stage-state.yaml")

    assert result.validation_error_count == 0
    assert policy["authoritative_current_truth"] == ["data/project-state/current-stage-state.yaml"]
    assert policy["human_readable_docs_are_mirrors_only"] is True
    assert policy["historical_sections_can_contain_old_next_stage_claims"] is True
    if load_yaml("data/project-state/stage5eh-summary.yaml"):
        assert current["latest_completed_stage_id"] == "stage-5eh"
        assert current["recommended_next_stage_id"] == "stage-5ei"
    elif load_yaml("data/project-state/stage5eg-summary.yaml"):
        assert current["latest_completed_stage_id"] == "stage-5eg"
        assert current["recommended_next_stage_id"] == "stage-5eh"
    else:
        assert current["latest_completed_stage_id"] == "stage-5ef"
        assert current["recommended_next_stage_id"] == "stage-5eg"
