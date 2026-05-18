from __future__ import annotations

from libreprimus.discord_ingestion.link_extractor import classify_url, extract_plaintext_urls
from libreprimus.discord_ingestion.redaction import normalize_url


def test_link_extractor_finds_href_like_plaintext_urls() -> None:
    urls = extract_plaintext_urls("See https://github.com/x/y and https://pastebin.com/abc.")

    assert "https://github.com/x/y" in urls
    assert "https://pastebin.com/abc" in urls


def test_domain_classifier_covers_stage3n_source_types() -> None:
    cases = {
        "https://github.com/cicada-solvers/archive": "github",
        "https://example.fandom.com/wiki/Page": "fandom",
        "https://reddit.com/r/cicada": "reddit",
        "https://pastebin.com/abc": "pastebin",
        "https://docs.google.com/document/d/abc": "google_docs",
        "https://web.archive.org/web/2020/https://example.com": "internet_archive",
        "https://cdn.discordapp.com/attachments/1/2/a.png?ex=secret": "discord_attachment",
        "https://example.com/image.jpg": "image",
        "https://example.com/audio.mp3": "audio",
        "https://example.com/file.pdf": "pdf",
    }

    for url, expected in cases.items():
        assert classify_url(url) == expected


def test_discord_attachment_query_strings_are_redacted() -> None:
    normalized = normalize_url("https://cdn.discordapp.com/attachments/1/2/a.png?ex=secret&is=token")

    assert normalized == "https://cdn.discordapp.com/attachments/1/2/a.png"
