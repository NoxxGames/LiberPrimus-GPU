from libreprimus.token_block.stage5ca import INCORRECT_STAGE5AW_PATH
from libreprimus.token_block.stage5cm import (
    END_TO_END_NEGATIVE_CASES,
    validate_stage5cm_actual_record_rejection,
    validate_stage5cm_end_to_end_readiness_boundary,
)

from test_stage5cm_common import load_yaml


def test_stage5cm_end_to_end_boundary_lists_required_negative_cases() -> None:
    payload = load_yaml("data/token-block/stage5cm-end-to-end-readiness-boundary-validation.yaml")
    assert payload["all_negative_cases_fail_closed"] is True
    assert set(payload["negative_cases"]) == set(END_TO_END_NEGATIVE_CASES)

    counts, errors = validate_stage5cm_end_to_end_readiness_boundary()
    assert errors == []
    assert counts["negative_case_count"] == len(END_TO_END_NEGATIVE_CASES)


def test_stage5cm_actual_record_rejection_rejects_gate_opening_inputs() -> None:
    bad_records = [
        {"fixture_only": True},
        {"template_only": True},
        {"record_status": "review_package_only"},
        {"activation_authorized_now": True},
        {"active_planning_input_selected_now": True},
        {"byte_stream_generation_authorized_now": True},
        {"execution_authorized_now": True},
        {"solve_claim": True},
        {"path": INCORRECT_STAGE5AW_PATH},
    ]
    for payload in bad_records:
        assert validate_stage5cm_actual_record_rejection(payload)
