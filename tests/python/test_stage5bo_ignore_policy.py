import subprocess

from test_stage5bo_common import ROOT, run_git_check_ignore


def test_stage5bo_generated_templates_and_codex_handoff_are_ignored() -> None:
    assert run_git_check_ignore("experiments/results/token-block/stage5bo/summary.json")
    assert run_git_check_ignore("experiments/results/historical-route/stage5bo/summary.json")
    assert run_git_check_ignore("human-review-packs/stage5au/token-case-review-v2/decision-template.yaml")
    assert run_git_check_ignore("human-review-packs/stage5au/token-case-review-v2/decision-template-corrected.yaml")
    assert run_git_check_ignore("codex-output/stage5bo-codex-completion.md")
    assert run_git_check_ignore("codex_output/stage5bo-codex-completion.md")


def test_stage5bo_raw_and_generated_paths_are_not_staged() -> None:
    status = subprocess.run(["git", "status", "--short"], cwd=ROOT, check=True, capture_output=True, text=True).stdout
    forbidden_prefixes = (
        "A  human-review-packs/",
        "A  experiments/results/token-block/stage5bo/",
        "A  experiments/results/historical-route/stage5bo/",
        "A  codex-output/",
        "A  codex_output/",
    )
    assert not any(line.startswith(forbidden_prefixes) for line in status.splitlines())
