from __future__ import annotations

import subprocess


def test_stage5ax_generated_outputs_and_local_handoffs_are_ignored() -> None:
    ignored_paths = [
        "experiments/results/ci/parallel-validation/stage5ax/run-summary.json",
        "experiments/results/ci/parallel-validation/stage5ax/commands.jsonl",
        "experiments/results/ci/parallel-validation/stage5ax/logs",
        "codex-output/stage5ax-codex-completion.md",
    ]
    for path in ignored_paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path


def test_raw_and_human_review_paths_are_not_tracked_new() -> None:
    for path in ["data/raw", "human-review-packs", "third_party"]:
        result = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard", path],
            text=True,
            capture_output=True,
            check=False,
        )
        assert result.returncode == 0
        assert result.stdout.strip() == ""
