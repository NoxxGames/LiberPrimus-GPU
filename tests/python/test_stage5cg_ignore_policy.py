from test_stage5cg_common import git_check_ignore


def test_stage5cg_generated_outputs_and_codex_completion_are_ignored() -> None:
    assert git_check_ignore("experiments/results/token-block/stage5cg/summary.json")
    assert git_check_ignore("experiments/results/token-block/stage5cg/wording_review.json")
    assert git_check_ignore("codex-output/stage5cg-codex-completion.md")
    assert git_check_ignore("codex_output/stage5cg-codex-completion.md")
