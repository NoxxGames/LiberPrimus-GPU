from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

REPO = Path(__file__).resolve().parents[2]
SCHEMAS = [
    "schemas/history/discord-archive-record-v0.schema.json",
    "schemas/history/discord-html-file-lock-v0.schema.json",
    "schemas/history/discord-extracted-link-v0.schema.json",
    "schemas/history/discord-attachment-candidate-v0.schema.json",
    "schemas/history/discord-method-claim-candidate-v0.schema.json",
    "schemas/history/discord-numeric-observation-candidate-v0.schema.json",
    "schemas/history/discord-ingestion-summary-v0.schema.json",
]


def test_discord_schemas_validate() -> None:
    for relative in SCHEMAS:
        payload = json.loads((REPO / relative).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(payload)


def test_discord_privacy_flags_are_false_by_schema() -> None:
    for relative in SCHEMAS:
        payload = json.loads((REPO / relative).read_text(encoding="utf-8"))
        properties = payload.get("properties", {})
        constrained = False
        for flag in [
            "raw_logs_committed",
            "message_bodies_committed",
            "usernames_committed",
            "ai_upload_allowed",
            "ai_upload_used",
            "live_api_used",
            "scrape_used",
            "raw_content_committed",
            "message_body_committed",
            "raw_message_committed",
        ]:
            if flag not in properties:
                continue
            constrained = True
            assert properties[flag]["const"] is False
        for flag in ["surrounding_text_redacted", "private_url_redacted"]:
            if flag not in properties:
                continue
            constrained = True
            assert properties[flag]["const"] is True
        assert constrained
