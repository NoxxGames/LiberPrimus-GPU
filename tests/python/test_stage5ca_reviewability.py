from test_stage5ca_common import load_yaml


def test_stage5ca_summary_is_complete_and_metadata_only() -> None:
    summary = load_yaml("data/project-state/stage5ca-summary.yaml")
    assert summary["status"] == "complete"
    assert summary["metadata_only"] is True
    assert summary["execution_allowed"] is False
    assert summary["solve_claim"] is False
    assert summary["recommended_next_stage_id"] == "stage-5cb"


def test_stage5ca_findings_integration_encodes_stage5bz_verdict() -> None:
    findings = load_yaml("data/project-state/stage5ca-stage5bz-findings-integration.yaml")
    assert findings["stage5bz_findings_integrated"] is True
    assert findings["stage5bz_verdict"] == "accept_with_warnings"
    assert findings["warnings_are_gate_openers"] is False


def test_stage5ca_reviewability_records_exist() -> None:
    evidence = load_yaml("data/project-state/stage5ca-reviewable-validation-evidence.yaml")
    digest = load_yaml("data/project-state/stage5ca-reviewable-source-digest-index.yaml")
    assert evidence["codex_completion_summary_path"] == "codex-output/stage5ca-codex-completion.md"
    assert digest["source_paths_unique"] is True
    assert digest["source_digest_record_count"] == digest["source_digest_unique_path_count"]
