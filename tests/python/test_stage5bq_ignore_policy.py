import subprocess

from test_stage5bq_common import ROOT, run_git_check_ignore


def test_stage5bq_generated_and_codex_handoff_are_ignored() -> None:
    assert run_git_check_ignore("experiments/results/token-block/stage5bq/summary.json")
    assert run_git_check_ignore("experiments/results/token-block/stage5bq/source_file_digests.json")
    assert run_git_check_ignore("codex-output/stage5bq-codex-completion.md")
    assert run_git_check_ignore("codex_output/stage5bq-codex-completion.md")


def test_stage5bq_raw_and_generated_paths_are_not_staged() -> None:
    status = subprocess.run(["git", "status", "--short"], cwd=ROOT, check=True, capture_output=True, text=True)
    forbidden_prefixes = (
        "A  experiments/results/token-block/stage5bq/",
        "A  codex-output/",
        "A  codex_output/",
        "A  human-review-packs/",
    )

    assert not any(line.startswith(forbidden_prefixes) for line in status.stdout.splitlines())
