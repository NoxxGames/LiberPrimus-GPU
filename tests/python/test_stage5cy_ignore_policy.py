from pathlib import Path

from test_stage5cy_common import ensure_stage5cy_built, git_check_ignore, load_yaml


def test_stage5cy_generated_outputs_and_codex_completion_are_ignored() -> None:
    ensure_stage5cy_built()
    assert git_check_ignore("experiments/results/token-block/stage5cy/summary.json")
    assert git_check_ignore("experiments/results/token-block/stage5cy/option_selection_preflight_report.json")
    assert git_check_ignore("experiments/results/token-block/stage5cy/validation_count_reconciliation_report.json")
    assert git_check_ignore("experiments/results/token-block/stage5cy/warnings.jsonl")
    assert git_check_ignore("codex-output/stage5cy-codex-completion.md")


def test_stage5cy_uses_hyphenated_codex_output_and_never_underscore_root() -> None:
    ensure_stage5cy_built()
    handoff = load_yaml("data/source-harvester/stage5cy-codex-handoff-policy.yaml")

    assert handoff["canonical_codex_handoff_root"] == "codex-output"
    assert handoff["deprecated_handoff_root"] == "codex_output"
    assert handoff["codex_output_used"] is False
    assert handoff["codex_completion_summary_committed"] is False
    assert handoff["codex_output_exists_locally"] is False
    assert not Path("codex_output").exists()
