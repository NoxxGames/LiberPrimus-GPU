from __future__ import annotations

from pathlib import Path

from libreprimus.discord_review.lead_builder import _lead
from libreprimus.discord_review.shard_writer import write_topic_shards


def test_shard_writer_writes_privacy_header(tmp_path: Path) -> None:
    lead = _lead(
        source_id="synthetic",
        topic="deep-web-hash-and-cookies",
        evidence_type="method_claim",
        public_links=[],
        numeric_values=[167, 761],
        method_keywords=["hash", "cookie"],
        redacted_summary="method keyword cluster: hash/cookie",
        suggested_next_action="Review only.",
        source_channel="synthetic",
    )

    records = write_topic_shards(out_dir=tmp_path, leads=[lead], generated_at="2026-05-18T00:00:00Z")

    assert records
    shard = tmp_path / "topic_shards/deep-web-hash-and-cookies.md"
    text = shard.read_text(encoding="utf-8")
    assert "raw_logs_committed: false" in text
    assert "usernames_redacted: true" in text
    assert "solve_claim: false" in text


def test_shard_writer_splits_when_size_limit_exceeded(tmp_path: Path) -> None:
    leads = [
        _lead(
            source_id=f"synthetic-{index}",
            topic="open-questions-and-strong-leads",
            evidence_type="method_claim",
            public_links=[],
            numeric_values=[],
            method_keywords=["prime"],
            redacted_summary="x" * 300,
            suggested_next_action="Review only.",
            source_channel="synthetic",
        )
        for index in range(6)
    ]

    records = write_topic_shards(out_dir=tmp_path, leads=leads, generated_at="2026-05-18T00:00:00Z", max_bytes=900)

    split_records = [record for record in records if record["topic"] == "open-questions-and-strong-leads"]
    assert len(split_records) > 1
