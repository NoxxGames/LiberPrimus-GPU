from libreprimus.token_block.stage5co import (
    MISSING_REQUIREMENTS,
    validate_stage5co_current_missing_requirements,
)

from test_stage5co_common import load_yaml


def test_stage5co_missing_requirements_register_blocks_activation() -> None:
    payload = load_yaml(
        "data/token-block/stage5co-current-missing-requirements-register.yaml"
    )
    assert payload["activation_valid_now"] is False
    assert payload["missing_requirements"]
    assert set(payload["missing_requirements"]) == set(MISSING_REQUIREMENTS)
    assert payload["missing_requirement_count"] == len(MISSING_REQUIREMENTS)

    counts, errors = validate_stage5co_current_missing_requirements()
    assert errors == []
    assert counts["stage5co_current_missing_requirements_valid"] is True
