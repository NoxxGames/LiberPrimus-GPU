from __future__ import annotations

import subprocess
from pathlib import Path

import yaml


def test_stage4a_generated_outputs_and_raw_inputs_ignored() -> None:
    for path in [
        "experiments/results/discord-full-review/stage4a/site/index.html",
        "experiments/results/discord-full-review/stage4a/channel_shards/example.part001.md",
        "experiments/results/discord-full-review/stage4a/lp_pages/lp_page_image_manifest.jsonl",
        "third_party/LiberPrimusDiscordChats/example.html",
        "third_party/LiberPrimusPages/example.jpg",
    ]:
        result = subprocess.run(["git", "check-ignore", "-q", "--", path], check=False)
        assert result.returncode == 0, path


def test_stage4a_aggregates_do_not_contain_raw_private_content() -> None:
    for relative in [
        "data/observations/discord/stage4a-full-review-aggregate.yaml",
        "data/observations/visual/stage4a-lp-page-gallery-aggregate.yaml",
    ]:
        payload = yaml.safe_load(Path(relative).read_text(encoding="utf-8"))
        text = Path(relative).read_text(encoding="utf-8").lower()
        assert payload["solve_claim"] is False
        assert "cdn.discord" not in text
        assert "media.discord" not in text
