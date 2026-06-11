from __future__ import annotations

from libreprimus.validation.stage_id import normalize_stage_token, stage_display_label, validation_command_name
from test_stage5ea_common import ensure_stage5ea_built, load_yaml


def test_stage_id_normalization_accepts_hyphenated_stage_ids() -> None:
    ensure_stage5ea_built()

    record = load_yaml("data/project-state/stage5ea-validation-wrapper-repair.yaml")

    assert record["stage_id_normalization_accepts_hyphenated_stage_ids"] is True
    assert normalize_stage_token("stage-5ea") == "stage5ea"
    assert normalize_stage_token("5ea") == "stage5ea"
    assert validation_command_name("stage-5ea") == "validate-stage5ea"
    assert stage_display_label("stage5eb") == "Stage 5EB"
