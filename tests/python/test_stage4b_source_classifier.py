from __future__ import annotations

from libreprimus.source_lock_triage.source_classifier import build_source_records, classify_url, normalize_url


def test_stage4b_allowlisted_urls_classify_correctly() -> None:
    result = classify_url("https://github.com/rtkd/iddqd?utm_source=x")

    assert result["decision"] == "allowlisted"
    assert result["normalized_url"] == "https://github.com/rtkd/iddqd"


def test_stage4b_emoji_and_cdn_noise_rejected() -> None:
    emoji = classify_url("https://twemoji.maxcdn.com/v/latest/svg/1f41d.svg")
    cdn = classify_url("https://cdn.jsdelivr.net/npm/package/index.js")

    assert emoji["decision"] == "rejected"
    assert cdn["decision"] == "rejected"


def test_stage4b_discord_private_urls_rejected() -> None:
    result = classify_url("https://cdn.discordapp.com/attachments/1/2/file.png?secret=abc")

    assert result["decision"] == "rejected"
    assert result["reason"] == "unsafe_or_noisy_domain"


def test_stage4b_duplicate_url_normalisation_works() -> None:
    public_links = [
        {"value": "https://github.com/rtkd/iddqd?utm_source=a", "index_id": "a"},
        {"value": "https://github.com/rtkd/iddqd/", "index_id": "b"},
    ]

    assert normalize_url(public_links[0]["value"]) == normalize_url(public_links[1]["value"])
    _records, summary = build_source_records(public_links)
    assert summary["duplicate_links_skipped"] == 1
