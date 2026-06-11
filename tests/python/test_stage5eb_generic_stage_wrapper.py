from __future__ import annotations

from libreprimus.validation.stage_id import normalize_stage_token, stage_display_label, validation_command_name
from test_stage5eb_common import ensure_stage5eb_built, load_yaml


def test_stage5eb_generic_stage_wrapper_accepts_short_identifiers() -> None:
    ensure_stage5eb_built()

    record = load_yaml("data/project-state/stage5eb-generic-stage-wrapper-repair.yaml")

    assert record["stage_command_normalization_generic"] is True
    assert record["hardcoded_stage_allowlist_removed"] is True
    assert normalize_stage_token("stage-5eb") == "stage5eb"
    assert normalize_stage_token("stage5eb") == "stage5eb"
    assert normalize_stage_token("5eb") == "stage5eb"
    assert normalize_stage_token("eb") == "stage5eb"
    assert validation_command_name("eb") == "validate-stage5eb"
    assert validation_command_name("stage-5eb") == "validate-stage5eb"
    assert stage_display_label("eb") == "Stage 5EB"
