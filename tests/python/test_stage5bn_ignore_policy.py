from test_stage5bn_common import run_git_check_ignore


def test_stage5bn_generated_and_raw_paths_are_ignored() -> None:
    assert run_git_check_ignore("experiments/results/token-block/stage5bn/summary.json")
    assert run_git_check_ignore("experiments/results/historical-route/stage5bn/summary.json")
    assert run_git_check_ignore("human-review-packs/stage5bn/string4-unsupported-position/review-template.yaml")
    assert run_git_check_ignore("codex-output/stage5bn-codex-completion.md")
    assert run_git_check_ignore("codex_output/stage5bn-codex-completion.md")
    assert run_git_check_ignore("third_party/3N_3p_Bases_49-51.jpg.xlsx")
