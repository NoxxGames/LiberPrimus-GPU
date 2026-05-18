from __future__ import annotations

from libreprimus.discord_ingestion.attachment_extractor import attachment_candidates_from_links
from libreprimus.discord_ingestion.link_extractor import link_record


def test_attachment_extractor_redacts_private_urls() -> None:
    link = link_record(
        "https://cdn.discordapp.com/attachments/1/2/example.png?ex=secret",
        source_file_sha256="a" * 64,
        ordinal=1,
    )

    records = attachment_candidates_from_links([link])

    assert records[0]["media_kind"] == "image"
    assert records[0]["private_url_redacted"] is True
    assert "?" not in records[0]["url_or_path_redacted"]
