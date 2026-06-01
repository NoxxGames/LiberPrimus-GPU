from libreprimus.token_block.stage5cs import validate_stage5cs_stage5co_preservation

from test_stage5cs_common import ensure_stage5cs_built, load_yaml


def test_stage5cs_preserves_stage5co_readiness_and_missing_requirements() -> None:
    ensure_stage5cs_built()
    payload = load_yaml("data/token-block/stage5cs-stage5co-missing-requirements-preservation.yaml")
    assert payload["stage5co_missing_requirements_register_preserved"] is True
    assert payload["missing_requirement_count"] == 13
    counts, errors = validate_stage5cs_stage5co_preservation()
    assert not errors
    assert counts["stage5cs_stage5co_preservation_valid"] is True
