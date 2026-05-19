from __future__ import annotations

from libreprimus.source_lock_snapshots.allowlist import (
    canonicalize_url,
    is_allowlisted_url,
    is_rejected_url,
)


def test_stage4k_allowlisted_github_and_uncovering_urls_accepted() -> None:
    assert is_allowlisted_url("https://github.com/rtkd/iddqd")
    assert is_allowlisted_url("https://uncovering-cicada.fandom.com/wiki/OutGuess")


def test_stage4k_discord_and_emoji_cdn_urls_rejected() -> None:
    assert is_rejected_url("https://cdn.discordapp.com/attachments/example/file.png")
    assert is_rejected_url("https://twemoji.maxcdn.com/v/latest/svg/1f40d.svg")


def test_stage4k_canonicalize_deduplicates_trailing_slash() -> None:
    assert canonicalize_url("https://github.com/rtkd/iddqd/") == "https://github.com/rtkd/iddqd"
