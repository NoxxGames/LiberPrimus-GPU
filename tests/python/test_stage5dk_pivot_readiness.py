from __future__ import annotations

from libreprimus.token_block import stage5dk
from test_stage5dk_common import ensure_stage5dk_built, load_yaml, write_temp_yaml


def test_stage5dk_pivot_readiness_has_seven_unselected_options() -> None:
    ensure_stage5dk_built()
    record = load_yaml("data/project-state/stage5dk-pivot-readiness-update.yaml")

    assert record["pivot_option_count"] == 7
    assert record["pivot_target_selected_now"] is False
    assert record["target_priority_decision_created_now"] is False
    assert [option["option_id"] for option in record["pivot_options"]] == stage5dk.PIVOT_OPTIONS
    assert all(option["selected_now"] is False for option in record["pivot_options"])
    assert all(option["final_ranking_assigned_now"] is False for option in record["pivot_options"])


def test_stage5dk_pivot_validator_rejects_selected_option(monkeypatch: object, tmp_path) -> None:
    ensure_stage5dk_built()
    record = load_yaml("data/project-state/stage5dk-pivot-readiness-update.yaml")
    record["pivot_target_selected_now"] = True
    record["pivot_options"][0]["selected_now"] = True
    path = write_temp_yaml(tmp_path / "pivot.yaml", record)
    monkeypatch.setitem(stage5dk.DATA_PATHS, "pivot_readiness_update", path)

    result = stage5dk.validate_stage5dk_pivot_readiness()
    assert result.validation_error_count > 0
    assert any("pivot_target_selected_now_must_be_false" in error for error in result.errors)
    assert any("pivot_option_selected" in error for error in result.errors)
