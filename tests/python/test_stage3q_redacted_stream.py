from __future__ import annotations

from libreprimus.discord_review.redacted_stream import public_links_from_text, redact_text


def test_redactor_removes_usernames_ids_and_discord_private_urls() -> None:
    text = (
        "Alice <@123456789012345678> id 987654321098765432 "
        "https://cdn.discordapp.com/attachments/1/2/file.png?ex=private&token=secret "
        "https://example.org/public?q=3301&utm_source=x"
    )

    redacted = redact_text(text)

    assert "<@" not in redacted
    assert "987654321098765432" not in redacted
    assert "token=secret" not in redacted
    assert "cdn.discordapp.com/attachments" not in redacted
    assert "[redacted-discord-attachment:file.png]" in redacted


def test_public_external_urls_are_preserved_without_tracking() -> None:
    links = public_links_from_text("see https://example.org/path?q=3301&utm_source=x")

    assert links == ["https://example.org/path?q=3301"]
