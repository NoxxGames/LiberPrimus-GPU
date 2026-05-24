from __future__ import annotations

import subprocess


def test_stage5ak_raw_generated_and_handoff_paths_are_ignored() -> None:
    paths = [
        "third_party/UsefulFilesAndIdeas/community-facts/community-facts-collection.txt",
        "third_party/UsefulFilesAndIdeas/community-facts/1.webp",
        "experiments/results/source-harvester-community-facts/stage5ak/community_claim_records.jsonl",
        "research-inputs/stage5ak/community_claim_records.jsonl",
        "codex-output/stage5ak-codex-completion.md",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path
