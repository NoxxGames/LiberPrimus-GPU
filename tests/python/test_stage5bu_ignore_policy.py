from test_stage5bu_common import run_git_check_ignore


def test_stage5bu_generated_outputs_and_codex_handoff_are_ignored() -> None:
    assert run_git_check_ignore("experiments/results/token-block/stage5bu/summary.json")
    assert run_git_check_ignore("experiments/results/token-block/stage5bu/source_file_digests.json")
    assert run_git_check_ignore("experiments/results/token-block/stage5bu/lineage_path_resolution.json")
    assert run_git_check_ignore("experiments/results/token-block/stage5bu/warnings.jsonl")
    assert run_git_check_ignore("codex-output/stage5bu-codex-completion.md")


def test_stage5bu_raw_and_generated_roots_not_staged_by_policy() -> None:
    assert run_git_check_ignore("data/raw/example.txt")
    assert run_git_check_ignore("experiments/results/token-block/stage5bu/example.json")
    assert run_git_check_ignore("codex-output/stage5bu-codex-completion.md")
