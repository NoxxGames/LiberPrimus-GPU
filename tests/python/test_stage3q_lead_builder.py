from __future__ import annotations

from libreprimus.discord_review.lead_builder import _lead


def test_lead_builder_creates_redacted_review_lead() -> None:
    lead = _lead(
        source_id="synthetic",
        topic="source-links-and-datasets",
        evidence_type="source_link",
        public_links=["https://github.com/example/repo"],
        numeric_values=[3301],
        method_keywords=["github"],
        redacted_summary="Public source link only.",
        suggested_next_action="Review public source.",
        source_channel="synthetic-channel",
    )

    assert lead["record_type"] == "discord_review_lead_record"
    assert lead["raw_message_committed"] is False
    assert lead["username_committed"] is False
    assert lead["private_url_committed"] is False
    assert lead["trusted_as_canonical"] is False
    assert lead["solve_claim"] is False
