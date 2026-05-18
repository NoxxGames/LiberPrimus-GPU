from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]


def test_stage3r_committed_records_have_no_raw_discord_private_content() -> None:
    paths = [
        REPO / "data/observations/discord/stage3r-promoted-source-records.yaml",
        REPO / "data/observations/discord/stage3r-promoted-observation-records.yaml",
        REPO / "data/observations/discord/stage3r-negative-control-records.yaml",
        REPO / "data/observations/discord/stage3r-promotion-audit-summary.yaml",
    ]
    forbidden = [
        "cdn.discordapp.com/attachments/",
        "media.discordapp.net/attachments/",
        "message_body:",
        "username:",
        "user_id:",
        "message_id:",
    ]
    for path in paths:
        text = path.read_text(encoding="utf-8").lower()
        assert all(marker not in text for marker in forbidden)
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        if "records" in payload:
            for record in payload["records"]:
                if "raw_message_committed" in record:
                    assert record["raw_message_committed"] is False
                if "username_committed" in record:
                    assert record["username_committed"] is False
                if "private_url_committed" in record:
                    assert record["private_url_committed"] is False
