import subprocess


def test_stage5bf_generated_outputs_and_local_archives_are_ignored() -> None:
    paths = [
        "experiments/results/historical-route/stage5bf/full_archive_file_inventory.jsonl",
        "experiments/results/historical-route/stage5bf/high_priority_artifact_index.json",
        "experiments/results/historical-route/stage5bf/summary.json",
        "deep-research-content-packs/stage5bf/historical-route-source-lock-pack.zip",
        "deep-research-repo-zips/stage5bf/stage5bf-repo.zip",
        "third_party/CicadaSolversIddqd/2012/example.jpg",
        "codex-output/stage5bf-codex-completion.md",
    ]

    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path
