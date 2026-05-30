from test_stage5ce_common import ROOT, git_check_ignore


def test_stage5ce_generated_outputs_and_codex_handoff_are_ignored() -> None:
    assert git_check_ignore("experiments/results/token-block/stage5ce/summary.json")
    assert git_check_ignore("experiments/results/token-block/stage5ce/proposal_package.json")
    assert git_check_ignore("experiments/results/token-block/stage5ce/combined_gate_contract.json")
    assert git_check_ignore("codex-output/stage5ce-codex-completion.md")


def test_stage5ce_codex_output_directory_unused() -> None:
    assert not (ROOT / "codex_output").exists()
