from libreprimus.token_block.stage5cu import (
    OPTION_SELECTION_MISUSE_TRANSITIONS,
    validate_stage5cu_option_selection_misuse,
)

from test_stage5cu_common import ensure_stage5cu_built, load_yaml


def test_stage5cu_option_selection_misuse_matrix_fails_closed() -> None:
    ensure_stage5cu_built()
    payload = load_yaml("data/token-block/stage5cu-option-selection-misuse-validation-matrix.yaml")
    assert payload["option_selection_misuse_case_count"] == 13
    assert {
        (row["source_record_class"], row["target_record_class"]) for row in payload["matrix_rows"]
    } == set(OPTION_SELECTION_MISUSE_TRANSITIONS)
    for row in payload["matrix_rows"]:
        assert row["allowed_now"] is False
        assert row["must_fail_closed"] is True
        assert row["authorizes_execution"] is False
        assert row["solve_claim"] is False
    counts, errors = validate_stage5cu_option_selection_misuse()
    assert not errors
    assert counts["stage5cu_option_selection_misuse_valid"] is True
