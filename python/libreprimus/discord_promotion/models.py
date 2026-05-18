"""Shared constants for Stage 3O Discord source promotion."""

from __future__ import annotations

SOURCE = "discord_admin_export_stage3n"
MAX_SOURCE_LINKS = 500
MAX_METHOD_CLAIMS = 200
MAX_NUMERIC_OBSERVATIONS = 200

HIGH_PRIORITY_DOMAINS = {
    "github.com",
    "raw.githubusercontent.com",
    "uncovering-cicada.fandom.com",
    "archive.org",
    "web.archive.org",
    "reddit.com",
    "www.reddit.com",
    "pastebin.com",
    "docs.google.com",
    "drive.google.com",
    "static.wikia.nocookie.net",
}

MEDIUM_PRIORITY_KINDS = {"image", "audio", "pdf", "html", "internet_archive"}

SOURCE_CLASS_BY_KIND = {
    "github": "strong_community_technical",
    "fandom": "archived_claim",
    "reddit": "archived_claim",
    "pastebin": "archived_claim",
    "google_docs": "archived_claim",
    "internet_archive": "secondary_archive",
    "image": "secondary_archive",
    "audio": "secondary_archive",
    "pdf": "secondary_archive",
    "html": "archived_claim",
    "unknown": "archived_claim",
}

KNOWN_NUMBERS = {3301, 1033, 761, 167, 509, 503, 563, 569, 29, 31, 13, 3722101}
DISCORD_DOMAINS = {
    "discord.com",
    "discord.gg",
    "discordapp.com",
    "cdn.discordapp.com",
    "media.discordapp.net",
    "cdn.discordapp.net",
}
