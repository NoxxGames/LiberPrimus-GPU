from libreprimus.token_block.stage5co import (
    FUTURE_REAL_RECORD_CLASSES,
    validate_stage5co_actual_record_rejection,
    validate_stage5co_approval_readiness_package,
)

from test_stage5co_common import load_yaml


def test_stage5co_approval_readiness_package_creates_no_real_records() -> None:
    payload = load_yaml("data/token-block/stage5co-real-approval-record-readiness-package.yaml")
    assert payload["real_approval_record_readiness_package_created"] is True
    assert payload["future_real_records_created_now"] is False
    assert payload["real_approval_records_created"] is False
    assert set(payload["future_real_record_classes"]) == set(FUTURE_REAL_RECORD_CLASSES)

    counts, errors = validate_stage5co_approval_readiness_package()
    assert errors == []
    assert counts["future_real_record_class_count"] == 4


def test_stage5co_rejects_synthetic_readiness_satisfied_now() -> None:
    errors = validate_stage5co_actual_record_rejection(
        {"real_approval_readiness_satisfied_now": True}
    )
    assert errors
