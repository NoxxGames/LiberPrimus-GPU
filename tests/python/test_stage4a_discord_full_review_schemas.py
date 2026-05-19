from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMA_FILES = [
    "schemas/history/discord-full-review-channel-record-v0.schema.json",
    "schemas/history/discord-full-review-message-record-v0.schema.json",
    "schemas/history/discord-full-review-shard-record-v0.schema.json",
    "schemas/history/discord-full-review-index-record-v0.schema.json",
    "schemas/history/discord-full-review-summary-v0.schema.json",
    "schemas/visual/lp-page-gallery-record-v0.schema.json",
    "schemas/visual/discord-image-reference-v0.schema.json",
]


def test_stage4a_schemas_parse() -> None:
    for relative in SCHEMA_FILES:
        schema = json.loads(Path(relative).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_stage4a_summary_schema_enforces_privacy_flags() -> None:
    schema = json.loads(Path("schemas/history/discord-full-review-summary-v0.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    payload = {
        "record_type": "discord_full_review_summary",
        "run_id": "stage4a",
        "privacy_mode": "redacted_public",
        "discord_html_file_count": 1,
        "total_bytes_processed": 100,
        "channel_count": 1,
        "redacted_message_count": 1,
        "channel_shard_count": 1,
        "topic_shard_count": 12,
        "public_link_count": 1,
        "image_reference_count": 1,
        "attachment_reference_count": 1,
        "method_claim_count": 1,
        "numeric_claim_count": 1,
        "visual_claim_count": 1,
        "debunk_count": 0,
        "lp_page_image_count": 1,
        "raw_discord_html_committed": False,
        "generated_site_committed": False,
        "solve_claim": False,
    }

    assert list(validator.iter_errors(payload)) == []
    payload["solve_claim"] = True
    assert list(validator.iter_errors(payload))
