"""Allowlist and rejection policy for Stage 4K source locking."""

from __future__ import annotations

from urllib.parse import urlparse, urlunparse

from libreprimus.source_lock_snapshots.models import ALLOWLISTED_STAGE4K_IDS, SourceCandidate

ALLOWLISTED_DOMAINS = (
    "github.com",
    "raw.githubusercontent.com",
    "uncovering-cicada.fandom.com",
    "web.archive.org",
    "archive.org",
    "cygwin.com",
)

REJECTED_DOMAIN_FRAGMENTS = (
    "discordapp.com",
    "discord.com",
    "media.discordapp.net",
    "cdn.discordapp.com",
    "twemoji",
    "googleusercontent.com",
    "gravatar.com",
)


def canonicalize_url(url: str) -> str:
    """Return a stable URL string for deduplication and records."""

    parsed = urlparse(url.strip())
    scheme = parsed.scheme.lower() or "https"
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/") if parsed.path != "/" else parsed.path
    return urlunparse((scheme, netloc, path, "", parsed.query, ""))


def domain(url: str) -> str:
    """Return lowercase URL host without a leading www."""

    host = urlparse(url).netloc.lower()
    return host.removeprefix("www.")


def is_rejected_url(url: str) -> bool:
    """Return true when URL is explicitly out of scope or unsafe/noisy."""

    host = domain(url)
    return any(fragment in host for fragment in REJECTED_DOMAIN_FRAGMENTS)


def is_allowlisted_url(url: str) -> bool:
    """Return true when URL host is in the Stage 4K public-source allowlist."""

    host = domain(url)
    return any(host == allowed or host.endswith(f".{allowed}") for allowed in ALLOWLISTED_DOMAINS)


def is_priority_candidate(candidate: SourceCandidate) -> bool:
    """Return true when the candidate is in the small Stage 4K priority set."""

    if candidate.candidate_id in ALLOWLISTED_STAGE4K_IDS:
        return True
    return candidate.candidate_id.removeprefix("stage4j-") in ALLOWLISTED_STAGE4K_IDS


def allowlist_policy_record() -> dict:
    """Return the committed Stage 4K public source-lock policy record."""

    return {
        "record_type": "public_source_lock_policy",
        "policy_id": "stage4k-public-source-lock-policy-v0",
        "allowlisted_domains": list(ALLOWLISTED_DOMAINS),
        "rejected_domains": list(REJECTED_DOMAIN_FRAGMENTS),
        "snapshot_policies": [
            "metadata_only",
            "ignored_local_snapshot",
            "committed_small_text_snapshot",
            "commit_addressed_reference",
            "archive_reference_only",
            "deferred_manual_review",
            "rejected_unsafe_or_noisy",
        ],
        "network_requires_allow_network": True,
        "notes": [
            "Stage 4K locks a small allowlisted source subset only.",
            "GitHub sources prefer commit-addressed references.",
            "Binary, image, audio, font, PDF, and archive artefacts are metadata-only by default.",
        ],
        "raw_private_data_committed": False,
        "binary_committed": False,
        "image_committed": False,
        "audio_committed": False,
        "font_committed": False,
        "archive_committed": False,
        "solve_claim": False,
    }
