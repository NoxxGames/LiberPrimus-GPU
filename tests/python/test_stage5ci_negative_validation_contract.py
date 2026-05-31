from libreprimus.token_block.stage5ci import (
    NEGATIVE_FAILURE_CLASSES,
    validate_stage5ci_negative_validation_contract,
)
from test_stage5ci_common import load_yaml, write_yaml


def test_stage5ci_negative_validation_contract_enumerates_failure_classes(tmp_path) -> None:
    counts, errors = validate_stage5ci_negative_validation_contract()
    assert not errors
    assert counts["failure_class_count"] == len(NEGATIVE_FAILURE_CLASSES)

    payload = load_yaml("data/token-block/stage5ci-approval-record-negative-validation-contract.yaml")
    payload["failure_classes"] = []
    bad = tmp_path / "negative.yaml"
    write_yaml(bad, payload)

    _, bad_errors = validate_stage5ci_negative_validation_contract(negative_contract=bad)
    assert bad_errors
