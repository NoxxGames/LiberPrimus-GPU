from libreprimus.token_block.stage5cm import validate_stage5cm_approval_readiness_boundary

from test_stage5cm_common import load_yaml


def test_stage5cm_approval_readiness_boundary_blocks_non_real_classes() -> None:
    payload = load_yaml("data/token-block/stage5cm-approval-readiness-boundary-contract.yaml")
    assert payload["approval_record_readiness_boundary_created"] is True
    assert payload["fixture_presented_as_real_record_must_fail_closed"] is True
    assert payload["template_presented_as_real_record_must_fail_closed"] is True
    assert payload["scaffold_presented_as_real_record_must_fail_closed"] is True
    assert payload["review_package_presented_as_real_record_must_fail_closed"] is True
    assert payload["future_real_records_created_now"] is False

    counts, errors = validate_stage5cm_approval_readiness_boundary()
    assert errors == []
    assert counts["future_real_record_class_count"] == 4
