from libreprimus.token_block.stage5cm import (
    BOUNDARY_SOURCE_RECORD_CLASSES,
    validate_stage5cm_fixture_real_boundary,
)

from test_stage5cm_common import load_yaml


def test_stage5cm_fixture_real_boundary_keeps_fixtures_non_satisfying() -> None:
    payload = load_yaml("data/token-block/stage5cm-fixture-vs-real-record-boundary.yaml")
    assert set(payload["source_record_classes_blocked_from_gate_satisfaction"]) == set(
        BOUNDARY_SOURCE_RECORD_CLASSES
    )
    assert payload["fixture_records_can_satisfy_gate"] is False
    assert payload["templates_can_satisfy_gate"] is False
    assert payload["scaffolds_can_satisfy_gate"] is False
    assert payload["review_packages_can_satisfy_gate"] is False

    counts, errors = validate_stage5cm_fixture_real_boundary()
    assert errors == []
    assert counts["blocked_source_record_class_count"] == len(BOUNDARY_SOURCE_RECORD_CLASSES)
