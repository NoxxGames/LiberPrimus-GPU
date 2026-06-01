from libreprimus.token_block.stage5cq import validate_stage5cq_stage5co_preservation

from test_stage5cq_common import ensure_stage5cq_built, load_yaml


def test_stage5cq_preserves_stage5co_readiness_and_missing_requirements() -> None:
    ensure_stage5cq_built()
    readiness = load_yaml("data/token-block/stage5cq-stage5co-readiness-package-preservation.yaml")
    missing = load_yaml("data/token-block/stage5cq-stage5co-missing-requirements-preservation.yaml")
    transition = load_yaml("data/token-block/stage5cq-stage5co-transition-plan-preservation.yaml")
    assert readiness["stage5co_readiness_package_preserved"] is True
    assert readiness["stage5co_real_record_creation_blocker_preserved"] is True
    assert missing["missing_requirement_count"] == 13
    assert missing["stage5co_missing_requirements_falsely_closed"] is False
    assert transition["stage5co_activation_transition_plan_preserved"] is True
    counts, errors = validate_stage5cq_stage5co_preservation()
    assert not errors
    assert counts["stage5cq_stage5co_preservation_valid"] is True
