from pathlib import Path

import yaml

from libreprimus.token_block.stage5ce import validate_stage5ce_sidecar_gates
from test_stage5ce_common import load_yaml


def test_stage5ce_findings_integrate_stage5cd_warnings() -> None:
    findings = load_yaml("data/project-state/stage5ce-stage5cd-findings-integration.yaml")
    assert findings["stage5cd_findings_integrated"] is True
    assert findings["stage5cd_verdict"] == "accept_with_warnings"
    assert findings["warnings_are_gate_openers"] is False
    assert findings["active_string4_ingestion_recommended"] is False


def test_stage5ce_reviewability_records_include_pytest_count() -> None:
    evidence = load_yaml("data/project-state/stage5ce-reviewable-validation-evidence.yaml")
    digest = load_yaml("data/project-state/stage5ce-reviewable-source-digest-index.yaml")
    gaps = load_yaml("data/project-state/stage5ce-reviewability-gap-register.yaml")
    assert evidence["codex_completion_summary_path"] == "codex-output/stage5ce-codex-completion.md"
    assert evidence["final_commit_self_embedded"] is False
    assert evidence["ci_external_evidence_required"] is True
    assert isinstance(evidence["pytest_count_observed_locally"], int)
    assert evidence["pytest_count_observed_locally"] > 0
    assert digest["source_digest_unique_path_count"] == digest["source_digest_record_count"]
    assert gaps["gap_count"] == 4


def test_stage5ce_missing_pytest_count_capture_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/project-state/stage5ce-reviewable-validation-evidence.yaml")
    payload.pop("pytest_count_observed_locally")
    candidate = tmp_path / "validation.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5ce_sidecar_gates(validation_evidence=candidate)
    assert counts["stage5ce_sidecar_gates_valid"] is False
    assert "pytest_count_observed_locally must be an integer" in errors


def test_stage5ce_codex_output_usage_fails(tmp_path: Path) -> None:
    payload = load_yaml("data/source-harvester/stage5ce-codex-handoff-policy.yaml")
    payload["codex_output_used"] = True
    candidate = tmp_path / "handoff.yaml"
    candidate.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    counts, errors = validate_stage5ce_sidecar_gates(handoff=candidate)
    assert counts["stage5ce_sidecar_gates_valid"] is False
    assert "codex_output_used must be false" in errors
