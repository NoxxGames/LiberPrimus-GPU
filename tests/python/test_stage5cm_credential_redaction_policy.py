from libreprimus.token_block.stage5cm import (
    _secret_findings,
    validate_stage5cm_credential_redaction_policy,
)

from test_stage5cm_common import load_yaml


def test_stage5cm_credential_redaction_policy_records_no_secret_values() -> None:
    payload = load_yaml("data/source-harvester/stage5cm-credential-redaction-policy.yaml")
    assert payload["credential_redaction_policy_created"] is True
    assert payload["credential_like_remote_must_be_redacted"] is True
    assert payload["credential_like_text_must_not_be_committed"] is True
    assert payload["committed_stage5cm_metadata_secret_scan_required"] is True
    assert payload["secret_values_printed_or_committed"] is False
    assert payload["remote_url_redacted_in_metadata"] is True

    counts, errors = validate_stage5cm_credential_redaction_policy()
    assert errors == []
    assert counts["stage5cm_credential_redaction_policy_valid"] is True


def test_stage5cm_secret_finder_detects_common_credential_shapes() -> None:
    findings = _secret_findings("remote https://ghp_aaaaaaaaaaaaaaaaaaaa@github.com/x/y.git")
    assert "github_personal_access_token_prefix" in findings
    assert "credentialed_github_https_remote" in findings
