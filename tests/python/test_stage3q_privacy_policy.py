from __future__ import annotations

from pathlib import Path

import yaml


def test_stage3q_aggregate_contains_no_message_bodies_or_usernames() -> None:
    repo = Path(__file__).resolve().parents[2]
    path = repo / "data/observations/discord/discord-review-bundle-aggregate-stage3q.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    text = path.read_text(encoding="utf-8").lower()

    assert payload["raw_logs_committed"] is False
    assert payload["raw_message_committed"] is False
    assert payload["username_committed"] is False
    assert payload["private_url_committed"] is False
    assert payload["ai_upload_used"] is False
    assert payload["live_api_used"] is False
    assert payload["scrape_used"] is False
    assert payload["solve_claim"] is False
    assert "cdn.discordapp.com/attachments/" not in text
    assert "media.discordapp.net/attachments/" not in text
    assert "message_body:" not in text
    assert "username:" not in text
