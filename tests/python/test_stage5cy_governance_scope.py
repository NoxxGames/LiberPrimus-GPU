from test_stage5cy_common import ensure_stage5cy_built, load_yaml


def test_stage5cy_governance_scope_requires_stage5cz_review_then_choice_or_pause() -> None:
    ensure_stage5cy_built()
    governance = load_yaml("data/project-state/stage5cy-governance-scope-control.yaml")
    next_stage = load_yaml("data/project-state/stage5cy-next-stage-decision.yaml")

    assert governance["governance_overbuild_risk_acknowledged"] is True
    assert governance["stage5cz_review_required_before_operator_choice"] is True
    assert governance["after_stage5cz_requires_operator_choice_or_pause"] is True
    assert governance["additional_generic_preflight_layers_allowed_without_concrete_defect"] is False
    assert governance["stage5cy_skips_stage5cz_review"] is False
    assert governance["stage5cy_selects_operator_choice"] is False
    assert next_stage["selected_next_stage_id"] == "stage-5cz"
    assert next_stage["selected_next_prompt_type"] == "deep_research_review"
    assert next_stage["selected_next_stage_authorizes_execution"] is False


def test_stage5cy_worker_cap_keeps_eight_and_not_sixteen() -> None:
    ensure_stage5cy_built()
    validation = load_yaml("data/project-state/stage5cy-reviewable-validation-evidence.yaml")

    assert validation["parallel_worker_cap"] == 8
    assert validation["parallel_worker_cap_for_stage5cm_and_later"] == 8
    assert validation["old_16_worker_default_reintroduced"] is False
