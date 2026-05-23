from __future__ import annotations

import subprocess


def test_stage5ai_generated_outputs_are_ignored() -> None:
    paths = [
        "research-inputs/stage5ai/master_manifest.yaml",
        "research-inputs/stage5ai/source_cards.jsonl",
        "research-inputs/stage5ai/website_ingest_index.json",
        "research-inputs/stage5ai/01-signed-messages-and-authenticity/manifest.yaml",
        "experiments/results/research-bundles/stage5ai/summary.json",
        "codex-output/stage5ai-codex-completion.md",
    ]
    for path in paths:
        result = subprocess.run(["git", "check-ignore", "-q", path], check=False)
        assert result.returncode == 0, path


def test_stage5ai_raw_third_party_content_is_ignored() -> None:
    result = subprocess.run(["git", "check-ignore", "-q", "third_party/LiberPrimusDiscordChats/example.txt"], check=False)
    assert result.returncode == 0
