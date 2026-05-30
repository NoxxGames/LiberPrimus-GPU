from test_stage5cc_common import ROOT, git_check_ignore


def test_stage5cc_generated_outputs_and_codex_handoff_are_ignored() -> None:
    assert git_check_ignore("experiments/results/token-block/stage5cc/summary.json")
    assert git_check_ignore("experiments/results/token-block/stage5cc/fail_closed_trigger_contract.json")
    assert git_check_ignore("codex-output/stage5cc-codex-completion.md")


def test_stage5cc_codex_output_directory_unused() -> None:
    assert not (ROOT / "codex_output").exists()
