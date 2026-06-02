from test_stage5cw_common import ensure_stage5cw_built, git_check_ignore


def test_stage5cw_generated_outputs_and_handoff_are_ignored() -> None:
    ensure_stage5cw_built()

    assert git_check_ignore("experiments/results/token-block/stage5cw/summary.json")
    assert git_check_ignore(
        "experiments/results/token-block/stage5cw/real_decision_package_preflight_report.json"
    )
    assert git_check_ignore("experiments/results/token-block/stage5cw/preflight_misuse_report.json")
    assert git_check_ignore("codex-output/stage5cw-codex-completion.md")
    assert git_check_ignore("data/raw/example.txt")
