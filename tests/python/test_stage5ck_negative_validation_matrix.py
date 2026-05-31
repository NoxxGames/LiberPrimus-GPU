from libreprimus.token_block.stage5ck import NEGATIVE_MATRIX_CLASSES

from test_stage5ck_common import load_yaml


def test_negative_validation_matrix_covers_fixture_rejections() -> None:
    payload = load_yaml("data/token-block/stage5ck-approval-fixture-negative-validation-matrix.yaml")
    assert payload["negative_validation_matrix_status"] == "active"
    assert set(NEGATIVE_MATRIX_CLASSES) <= set(payload["negative_validation_classes"])
    assert payload["fixture_records_rejected_as_actual_records"] is True
    assert payload["fixtures_may_satisfy_real_gate"] is False
