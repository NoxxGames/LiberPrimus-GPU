from libreprimus.token_block.stage5cu import validate_stage5cu_credential_redaction_policy

from test_stage5cu_common import ensure_stage5cu_built, load_yaml


def test_stage5cu_preserves_credential_redaction_policy() -> None:
    ensure_stage5cu_built()
    payload = load_yaml("data/source-harvester/stage5cu-credential-redaction-policy-preservation.yaml")
    assert payload["credential_redaction_policy_preserved"] is True
    assert payload["credential_like_remote_must_be_redacted"] is True
    assert payload["secret_values_printed_or_committed"] is False
    counts, errors = validate_stage5cu_credential_redaction_policy()
    assert not errors
    assert counts["stage5cu_credential_redaction_policy_valid"] is True
