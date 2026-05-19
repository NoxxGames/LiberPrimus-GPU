"""Shared constants for Stage 4B source-lock triage."""

from __future__ import annotations

from pathlib import Path

DEFAULT_STAGE4A_DIR = Path("experiments/results/discord-full-review/stage4a")
DEFAULT_OUTPUT_DIR = Path("experiments/results/source-lock-triage/stage4b")
DEFAULT_PROMOTED_SOURCES = Path("data/observations/archive/stage4b-promoted-source-records.yaml")
DEFAULT_SOURCE_HEALTH = Path("data/locks/third-party/stage4b-source-health-records.yaml")
DEFAULT_VISUAL_OBSERVATIONS = Path(
    "data/observations/visual/stage4b-visual-observation-records.yaml"
)
DEFAULT_NEGATIVE_CONTROLS = Path("data/observations/research/stage4b-negative-control-records.yaml")
DEFAULT_COOKIE_SOURCE_RECORDS = Path(
    "data/observations/web/stage4b-cookie-candidate-source-records.yaml"
)
DEFAULT_MANIFEST_DIR = Path("experiments/manifests/stage4b-disabled")

EVIDENCE_STRENGTHS = {"high", "medium", "low", "speculative"}
FALSE_POSITIVE_RISKS = {"low", "medium", "high", "extreme"}
CLASSIFICATIONS = {
    "public_source_to_lock",
    "observation_to_review",
    "experiment_candidate",
    "negative_control_candidate",
    "debunk_or_false_positive",
    "duplicate_of_existing_work",
    "too_speculative",
    "unsafe_or_private",
    "ignore_for_now",
}
RECOMMENDED_ACTIONS = {
    "source-lock now",
    "observation-review now",
    "queue bounded experiment",
    "add negative control",
    "duplicate existing work",
    "quarantine",
    "ignore",
}

ALLOWLIST_DOMAINS = {
    "github.com",
    "raw.githubusercontent.com",
    "uncovering-cicada.fandom.com",
    "archive.org",
    "web.archive.org",
    "commons.wikimedia.org",
    "docs.google.com",
    "sheets.google.com",
    "pastebin.com",
    "cicada3301.boards.net",
    "3301.gq",
    "cygwin.com",
}

NOISY_OR_UNSAFE_DOMAINS = {
    "cdn.discordapp.com",
    "media.discordapp.net",
    "discord.com",
    "cdn.jsdelivr.net",
    "twemoji.maxcdn.com",
    "images-ext-1.discordapp.net",
    "images-ext-2.discordapp.net",
}
