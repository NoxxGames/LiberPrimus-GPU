from libreprimus.token_block.stage5cq import (
    validate_stage5cq_actual_record_rejection,
    validate_stage5cq_credential_redaction_policy,
)

from test_stage5cq_common import ensure_stage5cq_built, load_yaml


def test_stage5cq_credential_redaction_policy_has_no_secret_values() -> None:
    ensure_stage5cq_built()
    payload = load_yaml("data/source-harvester/stage5cq-credential-redaction-policy-preservation.yaml")
    assert payload["credential_redaction_policy_preserved"] is True
    assert payload["secret_values_printed_or_committed"] is False
    assert payload["remote_hygiene"]["credential_like_remote_detected"] is False
    counts, errors = validate_stage5cq_credential_redaction_policy()
    assert not errors
    assert counts["stage5cq_credential_redaction_policy_valid"] is True


def test_stage5cq_rejects_synthetic_credential_like_text() -> None:
    errors = validate_stage5cq_actual_record_rejection({"text": "ghp_exampletokenvalue"})
    assert errors
