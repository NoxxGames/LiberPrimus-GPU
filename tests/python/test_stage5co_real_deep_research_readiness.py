from libreprimus.token_block.stage5co import (
    REAL_DEEP_RESEARCH_REQUIREMENTS,
    validate_stage5co_actual_record_rejection,
    validate_stage5co_real_deep_research_readiness,
)

from test_stage5co_common import load_yaml


def test_stage5co_real_deep_research_acceptance_is_absent_now() -> None:
    payload = load_yaml(
        "data/token-block/stage5co-real-deep-research-acceptance-readiness-preflight.yaml"
    )
    assert payload["real_deep_research_acceptance_readiness_preflight_created"] is True
    assert payload["deep_research_activation_accept_record_present_now"] is False
    assert set(REAL_DEEP_RESEARCH_REQUIREMENTS).issubset(payload["required_future_fields"])

    counts, errors = validate_stage5co_real_deep_research_readiness()
    assert errors == []
    assert counts["stage5co_real_deep_research_readiness_valid"] is True


def test_stage5co_rejects_synthetic_deep_research_acceptance_present_now() -> None:
    errors = validate_stage5co_actual_record_rejection(
        {"deep_research_activation_accept_record_present_now": True}
    )
    assert errors
