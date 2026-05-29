from test_stage5bs_common import ROOT, run_git_check_ignore


def test_stage5bs_generated_outputs_are_ignored() -> None:
    assert run_git_check_ignore("experiments/results/token-block/stage5bs/summary.json")
    assert run_git_check_ignore("experiments/results/token-block/stage5bs/source_file_digests.json")
    assert run_git_check_ignore("experiments/results/token-block/stage5bs/warnings.jsonl")


def test_stage5bs_codex_completion_uses_ignored_canonical_output_root() -> None:
    assert run_git_check_ignore("codex-output/stage5bs-codex-completion.md")
    assert not (ROOT / "codex_output").exists()


def test_stage5bs_forbidden_raw_roots_have_no_stage5bs_tracked_files() -> None:
    forbidden_roots = [
        "third_party",
        "human-review-packs",
        "data/raw",
        "data/normalized",
        "codex-output",
        "codex_output",
        "experiments/results",
    ]
    tracked_files = subprocess_paths(forbidden_roots)

    assert not [path for path in tracked_files if "stage5bs" in path.lower()]


def subprocess_paths(paths: list[str]) -> list[str]:
    import subprocess

    result = subprocess.run(["git", "ls-files", *paths], cwd=ROOT, check=True, capture_output=True, text=True)
    return [line for line in result.stdout.splitlines() if line]
