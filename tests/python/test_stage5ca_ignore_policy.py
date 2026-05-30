from test_stage5ca_common import ROOT, git_check_ignore


def test_stage5ca_generated_outputs_and_codex_handoff_are_ignored() -> None:
    assert git_check_ignore("experiments/results/token-block/stage5ca/summary.json")
    assert git_check_ignore("experiments/results/token-block/stage5ca/citation_contract.json")
    assert git_check_ignore("codex-output/stage5ca-codex-completion.md")


def test_stage5ca_codex_output_directory_unused() -> None:
    assert not (ROOT / "codex_output").exists()
