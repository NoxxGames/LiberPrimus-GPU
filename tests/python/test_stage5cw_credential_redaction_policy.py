from test_stage5cw_common import ensure_stage5cw_built, load_yaml


def test_stage5cw_credential_policy_records_no_secret_values() -> None:
    ensure_stage5cw_built()
    payload = load_yaml(
        "data/source-harvester/stage5cw-credential-redaction-policy-preservation.yaml"
    )

    assert payload["credential_redaction_policy_preserved"] is True
    assert payload["credential_like_remote_must_be_redacted"] is True
    assert payload["credential_like_text_must_not_be_committed"] is True
    assert payload["secret_values_printed_or_committed"] is False
    assert payload["remote_hygiene"]["secret_value_recorded"] is False
