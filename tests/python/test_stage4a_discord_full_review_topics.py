from __future__ import annotations

from libreprimus.discord_full_review.topic_classifier import classify_topics


def test_stage4a_topic_classifier_allows_multiple_topic_views() -> None:
    record = {
        "redacted_text": "Cuneiform base60 Onion 7 hash cookie outguess audio",
        "public_links": [],
        "method_keywords": [],
        "visual_keywords": [],
        "numeric_values": [],
    }

    topics = classify_topics(record)

    assert "cuneiform-base60" in topics
    assert "onion7-number-squares" in topics
    assert "deep-web-hash-cookies" in topics
    assert "outguess-stego-audio" in topics
