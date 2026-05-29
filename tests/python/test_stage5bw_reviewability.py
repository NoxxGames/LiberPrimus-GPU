from test_stage5bw_common import STAGE5BW_RECORDS, load_yaml


def test_stage5bw_reviewability_records_exist_and_include_validation() -> None:
    validation = load_yaml("data/project-state/stage5bw-reviewable-validation-evidence.yaml")
    digest = load_yaml("data/project-state/stage5bw-reviewable-source-digest-index.yaml")

    assert validation["local_validation_evidence_committed"] is True
    assert any(command["command_id"] == "stage5bw_validate" for command in validation["validation_commands"])
    assert validation["stage5ax_parallel_validation_used"] is True
    assert validation["codex_completion_summary_path"] == "codex-output/stage5bw-codex-completion.md"
    assert digest["source_digest_record_count"] >= 15
    assert len(STAGE5BW_RECORDS) == 27


def test_stage5bw_gap_register_has_no_blocking_stage5bw_gap() -> None:
    gaps = load_yaml("data/project-state/stage5bw-reviewability-gap-register.yaml")
    assert gaps["blocking_gap_count"] == 0
