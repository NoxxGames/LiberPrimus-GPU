from libreprimus.token_block.stage5co import (
    validate_stage5co_actual_record_rejection,
    validate_stage5co_credential_redaction_policy,
)

from test_stage5co_common import load_yaml


def test_stage5co_credential_redaction_policy_has_no_secret_values() -> None:
    payload = load_yaml(
        "data/source-harvester/stage5co-credential-redaction-policy-preservation.yaml"
    )
    assert payload["credential_redaction_policy_created"] is True
    assert payload["secret_values_printed_or_committed"] is False
    assert payload["remote_url_redacted_in_metadata"] is True
    assert payload["remote_hygiene"]["secret_value_recorded"] is False

    counts, errors = validate_stage5co_credential_redaction_policy()
    assert errors == []
    assert counts["stage5co_credential_redaction_policy_valid"] is True


def test_stage5co_review_packaging_warning_blocks_secret_bodies() -> None:
    payload = load_yaml("data/source-harvester/stage5co-review-packaging-warning.yaml")
    assert payload["review_packaging_warning_created"] is True
    assert payload["secret_values_printed_or_committed"] is False
    assert payload["raw_review_bodies_committed"] is False
    assert payload["generated_review_bodies_committed"] is False
    assert payload["generated_outputs_committed"] is False


def test_stage5co_rejects_synthetic_credential_like_text() -> None:
    errors = validate_stage5co_actual_record_rejection({"text": "ghp_exampletokenvalue"})
    assert errors
