"""Topic classification for Stage 4A views."""

from __future__ import annotations

from libreprimus.discord_full_review.models import TOPIC_DEFINITIONS


def classify_topics(record: dict) -> list[str]:
    haystack = " ".join(
        [
            str(record.get("redacted_text", "")),
            " ".join(str(item) for item in record.get("public_links", [])),
            " ".join(str(item) for item in record.get("method_keywords", [])),
            " ".join(str(item) for item in record.get("visual_keywords", [])),
            " ".join(str(item) for item in record.get("numeric_values", [])),
        ]
    ).lower()
    topics = [
        topic
        for topic, keywords in TOPIC_DEFINITIONS.items()
        if any(keyword in haystack for keyword in keywords)
    ]
    if not topics and ("?" in haystack or "maybe" in haystack):
        topics.append("open-questions-strong-leads")
    return topics
