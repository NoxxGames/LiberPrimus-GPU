from __future__ import annotations

import subprocess


def test_stage3u_generated_outputs_are_ignored() -> None:
    for path in [
        "experiments/results/post-discord/stage3u/hash_candidate_records.jsonl",
        "experiments/results/post-discord/stage3u/exact_matches.jsonl",
        "experiments/results/post-discord/stage3u/summary.json",
    ]:
        result = subprocess.run(["git", "check-ignore", "-q", "--", path], check=False)
        assert result.returncode == 0


def test_stage3u_raw_inputs_remain_ignored() -> None:
    for path in [
        "third_party/LiberPrimusDiscordChats/example.html",
        "third_party/LiberPrimusPages/example.jpg",
    ]:
        result = subprocess.run(["git", "check-ignore", "-q", "--", path], check=False)
        assert result.returncode == 0
