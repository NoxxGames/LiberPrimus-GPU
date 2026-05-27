import subprocess


def test_stage5bd_generated_outputs_and_archive_markers_are_ignored() -> None:
    paths = [
        "experiments/results/token-block/stage5bd/summary.json",
        "experiments/results/token-block/stage5bd/dry_run_plan_manifest.json",
        "experiments/results/token-block/stage5bd/fixtures/fixture_dry_run_records.json",
        "deep-research-repo-zips/stage5bd/ARCHIVE_MANIFEST.json",
        "deep-research-repo-zips/stage5bd/stage5bd-repo.zip",
        "codex-output/stage5bd-codex-completion.md",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path
