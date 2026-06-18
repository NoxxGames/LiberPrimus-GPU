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
    if load_yaml("data/project-state/stage6h-summary.yaml"):
        assert current["latest_completed_stage_id"] == "stage-6h"
        assert current["recommended_next_stage_id"] == "stage-6i"
    elif load_yaml("data/project-state/stage6g-summary.yaml"):
        assert current["latest_completed_stage_id"] == "stage-6g"
        assert current["recommended_next_stage_id"] == "stage-6h"
    elif load_yaml("data/project-state/stage6f-summary.yaml"):
        assert current["latest_completed_stage_id"] == "stage-6f"
        assert current["recommended_next_stage_id"] == "stage-6g"
    elif load_yaml("data/project-state/stage6e-summary.yaml"):
        assert current["latest_completed_stage_id"] == "stage-6e"
        assert current["recommended_next_stage_id"] == "stage-6f"
    elif load_yaml("data/project-state/stage6d-summary.yaml"):
        assert current["latest_completed_stage_id"] == "stage-6d"
        assert current["recommended_next_stage_id"] == "stage-6e"
    elif load_yaml("data/project-state/stage6c-summary.yaml"):
        assert current["latest_completed_stage_id"] == "stage-6c"
        assert current["recommended_next_stage_id"] == "stage-6d"
    elif load_yaml("data/project-state/stage6b-summary.yaml"):
        assert current["latest_completed_stage_id"] == "stage-6b"
        assert current["recommended_next_stage_id"] == "stage-6c"
    elif load_yaml("data/project-state/stage6-summary.yaml"):
        assert current["latest_completed_stage_id"] == "stage-6"
        assert current["recommended_next_stage_id"] == "stage-6b"
    elif load_yaml("data/project-state/stage5ei-summary.yaml"):
        assert current["latest_completed_stage_id"] == "stage-5ei"
        assert current["recommended_next_stage_id"] == "stage-6"
    elif load_yaml("data/project-state/stage5eh-summary.yaml"):
        assert current["latest_completed_stage_id"] == "stage-5eh"
        assert current["recommended_next_stage_id"] == "stage-5ei"
    elif load_yaml("data/project-state/stage5eg-summary.yaml"):
        assert current["latest_completed_stage_id"] == "stage-5eg"
        assert current["recommended_next_stage_id"] == "stage-5eh"
    else:
        assert current["latest_completed_stage_id"] == "stage-5ef"
        assert current["recommended_next_stage_id"] == "stage-5eg"
