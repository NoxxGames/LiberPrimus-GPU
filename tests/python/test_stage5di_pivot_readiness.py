from __future__ import annotations

from libreprimus.token_block.stage5di import PIVOT_CANDIDATES, validate_stage5di_pivot_readiness

from test_stage5di_common import ensure_stage5di_built, load_yaml, write_temp_yaml


def test_stage5di_pivot_readiness_exists_and_selects_no_target() -> None:
    ensure_stage5di_built()
    counts, errors = validate_stage5di_pivot_readiness()

    assert errors == []
    assert counts["pivot_option_count"] == len(PIVOT_CANDIDATES)
    assert counts["pivot_target_selected_now"] is False
    assert counts["operator_target_priority_decision_created_now"] is False

    payload = load_yaml("data/project-state/stage5di-pivot-readiness-package.yaml")
    assert payload["selected_next_solve_target_id"] is None
    assert all(candidate["candidate_not_selected"] is True for candidate in payload["pivot_candidates"])
    assert all(candidate["immediate_execution_allowed"] is False for candidate in payload["pivot_candidates"])


def test_stage5di_pivot_validator_rejects_selected_target(tmp_path) -> None:
    ensure_stage5di_built()
    payload = load_yaml("data/project-state/stage5di-pivot-readiness-package.yaml")
    payload["pivot_target_selected_now"] = True
    payload["selected_next_solve_target_id"] = "page32_tree_polar_route_first"
    temp = write_temp_yaml(tmp_path / "pivot.yaml", payload)

    _, errors = validate_stage5di_pivot_readiness(package=temp)

    assert errors
    assert "pivot_target_selected_now_must_be_false" in errors
    assert "selected_next_solve_target_id_must_be_null" in errors
