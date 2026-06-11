from __future__ import annotations

from libreprimus.validation.stage_id import validation_command_name
from test_stage5ea_common import ensure_stage5ea_built, load_yaml


def test_historical_tests_do_not_require_stage5dz_to_remain_latest() -> None:
    ensure_stage5ea_built()

    record = load_yaml("data/project-state/stage5ea-historical-test-isolation-repair.yaml")

    assert record["historical_stage_tests_use_explicit_fixture_or_registry"] is True
    assert record["stage5dz_tests_do_not_require_stage5dz_to_remain_latest"] is True
    assert validation_command_name("stage-5dz") == "validate-stage5dz"
    assert validation_command_name("stage-5ea") == "validate-stage5ea"
