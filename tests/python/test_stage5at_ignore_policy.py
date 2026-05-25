import subprocess


def test_stage5at_review_pack_and_generated_outputs_are_ignored() -> None:
    paths = [
        "human-review-packs/stage5at/token-case-review/index.html",
        "human-review-packs/stage5at/token-case-review/crops",
        "human-review-packs/stage5at/token-case-review/token-case-review-pack.zip",
        "experiments/results/token-block/stage5at/case_review_challenge_set.json",
        "codex-output/stage5at-codex-completion.md",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path
