from __future__ import annotations

from libreprimus.discord_ingestion.claim_extractor import extract_claim_candidates


def test_claim_extractor_uses_keyword_clusters_without_body_text() -> None:
    records = extract_claim_candidates(
        "I tried p56 prime totient and it failed; no result.",
        source_file_sha256="b" * 64,
        ordinal=1,
    )

    assert records
    assert records[0]["claim_type"] == "tried_and_failed"
    assert records[0]["raw_message_committed"] is False
    assert "I tried" not in records[0]["redacted_summary"]
