"""Source allowlisting and Stage 4A public-link triage."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import json
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from libreprimus.source_lock_triage.models import ALLOWLIST_DOMAINS, NOISY_OR_UNSAFE_DOMAINS


SOURCE_CATALOG: tuple[dict[str, Any], ...] = (
    {
        "source_id": "stage4b-rtkd-iddqd",
        "title": "rtkd iddqd original files and transcript anchor",
        "url": "https://github.com/rtkd/iddqd",
        "source_class": "strong_community_technical",
        "classification": "public_source_to_lock",
        "evidence_strength": "high",
        "false_positive_risk": "low",
        "recommended_action": "source-lock now",
        "notes": "Strong public technical anchor for original files/transcripts; metadata only in Stage 4B.",
    },
    {
        "source_id": "stage4b-scream314-cicada3301",
        "title": "scream314 Cicada 3301 public history repository",
        "url": "https://github.com/scream314/cicada3301",
        "source_class": "strong_community_technical",
        "classification": "public_source_to_lock",
        "evidence_strength": "high",
        "false_positive_risk": "low",
        "recommended_action": "source-lock now",
        "notes": "Public puzzle-history and Liber Primus notes; non-canonical until independently locked.",
    },
    {
        "source_id": "stage4b-complete-cicada-archive",
        "title": "The Complete Cicada3301 Archive",
        "url": "https://github.com/cicada-solvers/The-Complete-Cicada3301-Archive",
        "source_class": "secondary_archive",
        "classification": "public_source_to_lock",
        "evidence_strength": "medium",
        "false_positive_risk": "medium",
        "recommended_action": "source-lock now",
        "notes": "Selected-file metadata only; Stage 4B does not blind-mirror the archive.",
    },
    {
        "source_id": "stage4b-uncovering-liber-primus",
        "title": "Uncovering Cicada Liber Primus solved methods page",
        "url": "https://uncovering-cicada.fandom.com/wiki/Liber_Primus",
        "source_class": "strong_community_technical",
        "classification": "public_source_to_lock",
        "evidence_strength": "high",
        "false_positive_risk": "low",
        "recommended_action": "source-lock now",
        "notes": "Community technical summary of solved and unsolved Liber Primus context.",
    },
    {
        "source_id": "stage4b-uncovering-lp-unsolved-pages",
        "title": "Uncovering Cicada Liber Primus Unsolved Pages",
        "url": "https://uncovering-cicada.fandom.com/wiki/Liber_Primus_Unsolved_Pages",
        "source_class": "strong_community_technical",
        "classification": "public_source_to_lock",
        "evidence_strength": "high",
        "false_positive_risk": "low",
        "recommended_action": "source-lock now",
        "notes": "Public unsolved-page inventory; reviewable, not canonical.",
    },
    {
        "source_id": "stage4b-uncovering-lp-transliteration",
        "title": "Uncovering Cicada Liber Primus Unsolved Page Transliteration",
        "url": "https://uncovering-cicada.fandom.com/wiki/Liber_Primus_Unsolved_Page_Transliteration",
        "source_class": "strong_community_technical",
        "classification": "public_source_to_lock",
        "evidence_strength": "high",
        "false_positive_risk": "medium",
        "recommended_action": "source-lock now",
        "notes": "Reference for transliteration and page-boundary cautions; source-lock before use.",
    },
    {
        "source_id": "stage4b-uncovering-frequency-analysis",
        "title": "Uncovering Cicada Frequency Analysis Liber Primus",
        "url": "https://uncovering-cicada.fandom.com/wiki/Frequency_Analysis_(Liber_Primus)",
        "source_class": "strong_community_technical",
        "classification": "public_source_to_lock",
        "evidence_strength": "medium",
        "false_positive_risk": "medium",
        "recommended_action": "source-lock now",
        "notes": "Useful anti-fantasy reference for cipher-family triage.",
    },
    {
        "source_id": "stage4b-uncovering-instar-emergence",
        "title": "Uncovering Cicada Instar emergence",
        "url": "https://uncovering-cicada.fandom.com/wiki/Instar_emergence_(mp3_and_hidden_poem)",
        "source_class": "strong_community_technical",
        "classification": "public_source_to_lock",
        "evidence_strength": "high",
        "false_positive_risk": "low",
        "recommended_action": "source-lock now",
        "notes": "Historical anchor for 761.mp3 and audio/stego fixture planning.",
    },
    {
        "source_id": "stage4b-uncovering-what-happened-2014",
        "title": "Uncovering Cicada What Happened Part 1 2014",
        "url": "https://uncovering-cicada.fandom.com/wiki/What_Happened_Part_1_(2014)",
        "source_class": "strong_community_technical",
        "classification": "public_source_to_lock",
        "evidence_strength": "high",
        "false_positive_risk": "low",
        "recommended_action": "source-lock now",
        "notes": "Historical anchor for Interconnectedness, OpenPuff, and number squares.",
    },
    {
        "source_id": "stage4b-uncovering-outguess",
        "title": "Uncovering Cicada OutGuess page",
        "url": "https://uncovering-cicada.fandom.com/wiki/OutGuess",
        "source_class": "strong_community_technical",
        "classification": "public_source_to_lock",
        "evidence_strength": "high",
        "false_positive_risk": "low",
        "recommended_action": "source-lock now",
        "notes": "Historical stego reference; not a broad-scan permission.",
    },
    {
        "source_id": "stage4b-wayback-outguess",
        "title": "Wayback OutGuess site snapshot",
        "url": "https://web.archive.org/web/*/http://www.outguess.org/",
        "source_class": "reference_only_tooling",
        "classification": "public_source_to_lock",
        "evidence_strength": "medium",
        "false_positive_risk": "low",
        "recommended_action": "source-lock now",
        "notes": "Tool provenance only; not puzzle evidence.",
    },
    {
        "source_id": "stage4b-cygwin-outguess",
        "title": "Cygwin OutGuess package page",
        "url": "https://cygwin.com/packages/summary/outguess.html",
        "source_class": "reference_only_tooling",
        "classification": "public_source_to_lock",
        "evidence_strength": "medium",
        "false_positive_risk": "low",
        "recommended_action": "source-lock now",
        "notes": "Install/tooling provenance only.",
    },
    {
        "source_id": "stage4b-charleswyt-mp3stego",
        "title": "Charleswyt MP3Stego repository",
        "url": "https://github.com/Charleswyt/MP3Stego",
        "source_class": "reference_only_tooling",
        "classification": "public_source_to_lock",
        "evidence_strength": "medium",
        "false_positive_risk": "medium",
        "recommended_action": "source-lock now",
        "notes": "Reference-only tooling for future regression controls.",
    },
    {
        "source_id": "stage4b-rtkd-iddqd-2013-02-tree",
        "title": "rtkd iddqd 2013/02 asset tree",
        "url": "https://github.com/rtkd/iddqd/tree/master/2013/02",
        "source_class": "strong_community_technical",
        "classification": "public_source_to_lock",
        "evidence_strength": "high",
        "false_positive_risk": "low",
        "recommended_action": "source-lock now",
        "notes": "Selected metadata target for 2013 artefact fixture planning.",
    },
    {
        "source_id": "stage4b-cicada-solvers-iddqd-lp-outguessed",
        "title": "cicada-solvers iddqd LP outguessed tree",
        "url": "https://github.com/cicada-solvers/iddqd/tree/master/lp_outguessed",
        "source_class": "strong_community_technical",
        "classification": "public_source_to_lock",
        "evidence_strength": "medium",
        "false_positive_risk": "medium",
        "recommended_action": "source-lock now",
        "notes": "High-value public tree surfaced by Stage 4A indexes; metadata only and not canonical.",
    },
    {
        "source_id": "stage4b-google-translations-workbook",
        "title": "Google translations workbook",
        "url": "https://docs.google.com/spreadsheets/d/1QsoYQ-NkJcwEuyOgMrD6DkHU2AUktwsfnQGnTURf1bU/edit",
        "source_class": "secondary_archive",
        "classification": "public_source_to_lock",
        "evidence_strength": "medium",
        "false_positive_risk": "medium",
        "recommended_action": "source-lock now",
        "notes": "Lock metadata/snapshot cautiously; not canonical solved text.",
    },
    {
        "source_id": "stage4b-complete-archive-magicsquares",
        "title": "Complete Archive magicsquares.txt",
        "url": "https://github.com/cicada-solvers/The-Complete-Cicada3301-Archive/blob/main/assets/2014/stage07/magicsquares.txt",
        "source_class": "secondary_archive",
        "classification": "public_source_to_lock",
        "evidence_strength": "high",
        "false_positive_risk": "low",
        "recommended_action": "source-lock now",
        "notes": "Concrete number-square artefact target; no raw file is fetched in Stage 4B.",
    },
    {
        "source_id": "stage4b-complete-archive-li676-status",
        "title": "Complete Archive li676 server status original text",
        "url": "https://github.com/cicada-solvers/The-Complete-Cicada3301-Archive/blob/main/assets/2014/li676-224_server-status_orig.txt",
        "source_class": "secondary_archive",
        "classification": "public_source_to_lock",
        "evidence_strength": "medium",
        "false_positive_risk": "medium",
        "recommended_action": "source-lock now",
        "notes": "Reference-only later source-lock target; no broad mirror.",
    },
    {
        "source_id": "stage4b-cicada3301-boards-number-square",
        "title": "Old forum number-square essays",
        "url": "https://cicada3301.boards.net/",
        "source_class": "speculative",
        "classification": "too_speculative",
        "evidence_strength": "low",
        "false_positive_risk": "high",
        "recommended_action": "quarantine",
        "notes": "Historical context only; not evidence without exact artefact locks.",
    },
    {
        "source_id": "stage4b-boxentriq-binary-tools",
        "title": "Generic binary and utility tools",
        "url": "https://www.boxentriq.com/",
        "source_class": "reference_only_tooling",
        "classification": "ignore_for_now",
        "evidence_strength": "low",
        "false_positive_risk": "medium",
        "recommended_action": "ignore",
        "notes": "Generic tooling is not source evidence unless directly referenced by a locked workflow.",
    },
)


def normalize_url(url: str) -> str:
    """Normalize a URL enough for deterministic deduplication without fetching it."""

    value = url.strip().rstrip(").,]")
    parsed = urlsplit(value)
    scheme = (parsed.scheme or "https").lower()
    host = parsed.netloc.lower()
    path = parsed.path.rstrip("/")
    query_pairs = [
        (key, val)
        for key, val in parse_qsl(parsed.query, keep_blank_values=True)
        if key.lower()
        not in {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "fbclid"}
    ]
    query = urlencode(query_pairs, doseq=True)
    return urlunsplit((scheme, host, path, query, ""))


def classify_url(url: str) -> dict[str, Any]:
    """Classify one URL according to Stage 4B allowlist and rejection rules."""

    normalized = normalize_url(url)
    parsed = urlsplit(normalized)
    host = parsed.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    if host in NOISY_OR_UNSAFE_DOMAINS or "discordapp" in host or "discord.com" == host:
        return {
            "normalized_url": normalized,
            "decision": "rejected",
            "reason": "unsafe_or_noisy_domain",
        }
    if host.endswith("jsdelivr.net") or "twemoji" in normalized.lower():
        return {
            "normalized_url": normalized,
            "decision": "rejected",
            "reason": "emoji_or_cdn_noise",
        }
    if host in ALLOWLIST_DOMAINS:
        return {
            "normalized_url": normalized,
            "decision": "allowlisted",
            "reason": "allowlisted_domain",
        }
    return {
        "normalized_url": normalized,
        "decision": "ignored",
        "reason": "not_in_stage4b_allowlist",
    }


def load_public_links(stage4a_dir: Path) -> list[dict[str, Any]]:
    """Load Stage 4A public-link index records if present."""

    path = stage4a_dir / "indexes" / "public_link_index.jsonl"
    if not path.is_file():
        return []
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                payload = json.loads(line)
                if isinstance(payload, dict):
                    records.append(payload)
    return records


def build_source_records(
    public_links: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Build committed source-triage records and generated link-triage counters."""

    normalized_counter: Counter[str] = Counter()
    rejected: list[dict[str, str]] = []
    ignored = 0
    allowed = 0
    duplicates = 0
    seen: set[str] = set()
    refs_by_url: dict[str, list[str]] = {}

    for record in public_links:
        raw_url = str(record.get("value", ""))
        classification = classify_url(raw_url)
        normalized = str(classification["normalized_url"])
        normalized_counter[normalized] += 1
        if normalized in seen:
            duplicates += 1
        seen.add(normalized)
        if classification["decision"] == "rejected":
            rejected.append(
                {
                    "url": raw_url,
                    "normalized_url": normalized,
                    "reason": str(classification["reason"]),
                }
            )
        elif classification["decision"] == "ignored":
            ignored += 1
        else:
            allowed += 1
        ref = str(record.get("index_id") or record.get("message_ref") or "")
        if ref:
            refs_by_url.setdefault(normalized, []).append(ref)

    output: list[dict[str, Any]] = []
    for catalog in SOURCE_CATALOG:
        normalized = normalize_url(str(catalog["url"]))
        output.append(
            {
                "record_type": "stage4b_source_triage_record",
                "source_id": catalog["source_id"],
                "title": catalog["title"],
                "url": catalog["url"],
                "normalized_url": normalized,
                "source_class": catalog["source_class"],
                "classification": catalog["classification"],
                "evidence_strength": catalog["evidence_strength"],
                "false_positive_risk": catalog["false_positive_risk"],
                "recommended_action": catalog["recommended_action"],
                "stage4a_link_refs": sorted(refs_by_url.get(normalized, []))[:10],
                "retrieval_status": "metadata_recorded_not_fetched_stage4b",
                "trusted_as_canonical": False,
                "solve_claim": False,
                "notes": catalog["notes"],
            }
        )

    summary = {
        "links_loaded": len(public_links),
        "allowlisted_links_seen": allowed,
        "rejected_unsafe_or_noisy_links": len(rejected),
        "ignored_links": ignored,
        "duplicate_links_skipped": duplicates,
        "unique_normalized_links": len(normalized_counter),
        "rejected_links": rejected,
    }
    return output, summary
