"""Index extraction from redacted Stage 4A message records."""

from __future__ import annotations

from typing import Any

from libreprimus.discord_full_review.export import sha256_text
from libreprimus.discord_full_review.topic_classifier import classify_topics


def index_records_from_message(record: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    output = {
        "public_links": [],
        "image_references": [],
        "attachment_references": [],
        "method_claims": [],
        "numeric_claims": [],
        "visual_claims": [],
        "debunks": [],
    }
    for link in record.get("public_links", []):
        output["public_links"].append(_index_record(record, "public_link", value=link))
    for image in record.get("image_refs", []):
        output["image_references"].append({**image, "topic_tags": classify_topics(record)})
    for attachment in record.get("attachment_refs", []):
        output["attachment_references"].append({**attachment, "topic_tags": classify_topics(record)})
    if record.get("method_keywords"):
        output["method_claims"].append(_index_record(record, "method_claim", value=", ".join(record["method_keywords"])))
    if record.get("numeric_values"):
        output["numeric_claims"].append(_index_record(record, "numeric_claim", value=", ".join(str(v) for v in record["numeric_values"][:20])))
    if record.get("visual_keywords"):
        output["visual_claims"].append(_index_record(record, "visual_claim", value=", ".join(record["visual_keywords"])))
    if record.get("debunk_keywords"):
        output["debunks"].append(_index_record(record, "debunk", value=", ".join(record["debunk_keywords"])))
    return output


def _index_record(record: dict[str, Any], index_type: str, *, value: str) -> dict[str, Any]:
    key = f"{index_type}:{record.get('message_ref')}:{value}"
    return {
        "record_type": "discord_full_review_index_record",
        "index_id": f"idx-{sha256_text(key)[:20]}",
        "index_type": index_type,
        "message_ref": record.get("message_ref"),
        "channel_id": record.get("channel_id"),
        "channel_name": record.get("channel_name"),
        "value": value,
        "topic_tags": classify_topics(record),
        "redacted_excerpt": str(record.get("redacted_text", ""))[:500],
        "raw_message_committed": False,
        "username_committed": False,
        "user_id_committed": False,
        "message_id_committed": False,
        "private_url_committed": False,
        "solve_claim": False,
    }
