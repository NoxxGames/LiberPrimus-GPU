from test_stage5cc_common import load_yaml


def test_stage5cc_findings_integrate_stage5cb_warnings() -> None:
    findings = load_yaml("data/project-state/stage5cc-stage5cb-findings-integration.yaml")
    assert findings["stage5cb_findings_integrated"] is True
    assert findings["stage5cb_verdict"] == "accept_with_warnings"
    assert findings["warnings_are_gate_openers"] is False
    assert findings["active_string4_ingestion_recommended"] is False


def test_stage5cc_reviewability_records_exist() -> None:
    evidence = load_yaml("data/project-state/stage5cc-reviewable-validation-evidence.yaml")
    digest = load_yaml("data/project-state/stage5cc-reviewable-source-digest-index.yaml")
    gaps = load_yaml("data/project-state/stage5cc-reviewability-gap-register.yaml")
    assert evidence["codex_completion_summary_path"] == "codex-output/stage5cc-codex-completion.md"
    assert evidence["final_commit_self_embedded"] is False
    assert evidence["ci_external_evidence_required"] is True
    assert digest["source_digest_unique_path_count"] == digest["source_digest_record_count"]
    assert gaps["gap_count"] == 3


def test_stage5cc_extension_policies_are_non_gate_opening() -> None:
    trigger_policy = load_yaml("data/token-block/stage5cc-fail-closed-trigger-extension-policy.yaml")
    activation_policy = load_yaml(
        "data/token-block/stage5cc-activation-precondition-extension-policy.yaml"
    )
    for policy in [trigger_policy, activation_policy]:
        assert policy["extension_policy_status"] == "explicit_extensions_only"
        assert policy["unclassified_extension_allowed"] is False
        assert policy["extension_can_open_gate"] is False
        assert policy["extension_can_authorize_execution"] is False
        assert policy["extension_can_authorize_active_input"] is False
        assert policy["extension_can_authorize_byte_stream_generation"] is False
