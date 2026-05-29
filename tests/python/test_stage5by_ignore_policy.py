from test_stage5by_common import ROOT, git_check_ignore


def test_stage5by_generated_outputs_and_codex_handoff_are_ignored() -> None:
    assert git_check_ignore("experiments/results/token-block/stage5by/summary.json")
    assert git_check_ignore(
        "experiments/results/token-block/stage5by/sidecar-planning-manifest-scaffold.json"
    )
    assert git_check_ignore("codex-output/stage5by-codex-completion.md")


def test_stage5by_codex_output_directory_unused() -> None:
    assert not (ROOT / "codex_output").exists()
