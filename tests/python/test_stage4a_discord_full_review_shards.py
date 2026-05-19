from __future__ import annotations

from libreprimus.discord_full_review.channel_shards import split_messages


def test_stage4a_huge_channel_splits_into_multiple_parts() -> None:
    messages = [
        {
            "message_ref": f"msg-{index}",
            "approximate_timestamp": None,
            "redacted_text": "cuneiform base60 " + ("x" * 200),
            "public_links": [],
        }
        for index in range(901)
    ]

    shards = split_messages(messages)

    assert len(shards) >= 3
    assert sum(len(shard) for shard in shards) == 901
