from test_stage5bs_common import load_yaml


def test_stage5bs_reviewable_source_digest_records_ignored_stage5br_report() -> None:
    payload = load_yaml("data/project-state/stage5bs-reviewable-source-digest-index.yaml")
    ignored_records = [
        row
        for row in payload["consumed_source_records"]
        if row["role"] == "ignored_deep_research_report"
    ]

    assert len(ignored_records) == 1
    assert ignored_records[0]["present"] is True
    assert ignored_records[0]["committed"] is False
    assert ignored_records[0]["sha256"]


def test_stage5bs_reviewability_gap_register_records_external_evidence_gaps() -> None:
    payload = load_yaml("data/project-state/stage5bs-reviewability-gap-register.yaml")
    gap_ids = {row["gap_id"] for row in payload["gaps"]}

    assert "final_commit_hash_not_self_embedded" in gap_ids
    assert "ci_run_id_not_committed_at_stage_commit_time" in gap_ids
    assert "raw_codex_completion_summary_uncommitted" in gap_ids


def test_stage5bs_validation_evidence_is_compact_and_no_raw_output_staged() -> None:
    payload = load_yaml("data/project-state/stage5bs-reviewable-validation-evidence.yaml")
    command_ids = {row["command_id"] for row in payload["commands"]}

    assert payload["reviewability_evidence_status"] == "committed_compact_evidence"
    assert payload["local_validation_evidence_committed"] is True
    assert payload["raw_or_generated_files_staged"] is False
    assert payload["codex_output_staged"] is False
    assert "stage5bs_validator" in command_ids
    assert "bash_consistency_wrapper" in command_ids
