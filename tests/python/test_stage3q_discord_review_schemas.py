from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


def test_stage3q_discord_review_schemas_parse() -> None:
    repo = Path(__file__).resolve().parents[2]
    for name in [
        "discord-redacted-message-record-v0.schema.json",
        "discord-topic-shard-record-v0.schema.json",
        "discord-review-lead-record-v0.schema.json",
        "discord-review-bundle-summary-v0.schema.json",
    ]:
        payload = json.loads((repo / "schemas/history" / name).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(payload)


def test_stage3q_review_lead_schema_enforces_privacy_flags() -> None:
    repo = Path(__file__).resolve().parents[2]
    schema = json.loads(
        (repo / "schemas/history/discord-review-lead-record-v0.schema.json").read_text(encoding="utf-8")
    )
    payload = {
        "record_type": "discord_review_lead_record",
        "lead_id": "lead-1",
        "topic": "source-links-and-datasets",
        "source_channel": "synthetic",
        "approximate_date": "unknown",
        "evidence_type": "source_link",
        "public_links": ["https://github.com/example/repo"],
        "numeric_values": [],
        "method_keywords": ["github"],
        "redacted_summary": "public source link",
        "suggested_next_action": "review public source",
        "caution_notes": "review lead only",
        "review_status": "human_review_required",
        "raw_message_committed": False,
        "username_committed": False,
        "private_url_committed": False,
        "trusted_as_canonical": False,
        "solve_claim": False,
    }
    errors = list(Draft202012Validator(schema).iter_errors(payload))
    assert errors == []
