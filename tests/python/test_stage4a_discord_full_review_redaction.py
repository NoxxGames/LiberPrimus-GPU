from __future__ import annotations

from libreprimus.discord_full_review.redaction import public_links_from_text, redact_text, sanitize_url


def test_stage4a_redactor_removes_user_ids_mentions_and_discord_urls() -> None:
    text = "Hello <@123456789012345678> https://cdn.discordapp.com/attachments/1/2/file.jpg?secret=1 999999999999999999"
    redacted = redact_text(text)

    assert "123456789012345678" not in redacted
    assert "999999999999999999" not in redacted
    assert "cdn.discordapp.com" not in redacted
    assert "[redacted-discord-url:file.jpg]" in redacted


def test_stage4a_public_links_preserved_and_queries_trimmed() -> None:
    assert public_links_from_text("see https://example.org/a?q=keep&token=drop") == ["https://example.org/a?q=keep"]
    public, redacted = sanitize_url("https://discord.com/channels/1/2/3")
    assert public is None
    assert redacted.startswith("[redacted-discord-url:")
