from __future__ import annotations

from libreprimus.discord_lead_promotion.corroboration import classify_lead, normalized_public_url


def test_private_unsafe_urls_are_rejected() -> None:
    assert normalized_public_url("https://cdn.discordapp.com/attachments/1/2/a.png?ex=token") is None
    assert normalized_public_url("ftp://example.com/file") is None
    assert classify_lead(url="https://cdn.discordapp.com/attachments/1/2/a.png", has_public_source=False) == "unsafe_or_private"


def test_known_public_sources_are_normalized() -> None:
    assert normalized_public_url("https://github.com/rtkd/iddqd/") == "https://github.com/rtkd/iddqd"
    assert (
        classify_lead(url="https://github.com/rtkd/iddqd", has_public_source=True)
        == "source_to_lock"
    )


def test_discord_only_uncited_claim_is_not_promoted() -> None:
    assert classify_lead(url=None, has_public_source=False, speculative=True) == "too_speculative"
