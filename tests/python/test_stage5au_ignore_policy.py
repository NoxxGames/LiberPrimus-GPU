import subprocess


def test_stage5au_review_pack_and_generated_outputs_are_ignored() -> None:
    paths = [
        "human-review-packs/stage5au/token-case-review-v2/index.html",
        "human-review-packs/stage5au/token-case-review-v2/crops",
        "human-review-packs/stage5au/token-case-review-v2/context-crops",
        "human-review-packs/stage5au/token-case-review-v2/overlays",
        "human-review-packs/stage5au/token-case-review-v2/token-case-review-pack-v2.zip",
        "experiments/results/token-block/stage5au/summary.json",
        "third_party/LiberPrimusPages/49.jpg",
        "codex-output/stage5au-codex-completion.md",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path
