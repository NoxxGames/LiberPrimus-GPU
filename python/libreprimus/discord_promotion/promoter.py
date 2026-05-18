"""Stage 3O Discord source-promotion runner."""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from libreprimus.discord_promotion.export import iter_jsonl, read_json, write_json, write_jsonl, write_yaml
from libreprimus.discord_promotion.models import (
    MAX_METHOD_CLAIMS,
    MAX_NUMERIC_OBSERVATIONS,
    MAX_SOURCE_LINKS,
    SOURCE,
    SOURCE_CLASS_BY_KIND,
)
from libreprimus.discord_promotion.ranking import link_priority, method_priority, numeric_priority
from libreprimus.discord_promotion.redaction import safe_public_url
from libreprimus.paths import repo_root

RUN_ID = "stage3o-discord-source-promotion"


def promote_discord_sources(
    *,
    ingestion_dir: Path,
    out_dir: Path,
    promoted_links_out: Path,
    promoted_methods_out: Path,
    promoted_numerics_out: Path,
    allow_missing: bool = False,
    allow_warnings: bool = False,
) -> dict[str, Any]:
    """Promote public, redacted Stage 3N discoveries into committed review records."""
    resolved_ingestion = _resolve(ingestion_dir)
    resolved_out = _resolve(out_dir)
    warnings: list[str] = []
    if not resolved_ingestion.is_dir():
        if allow_missing:
            warnings.append("stage3n_ingestion_dir_missing_promotion_skipped")
            return _write_empty_outputs(
                resolved_out=resolved_out,
                promoted_links_out=_resolve(promoted_links_out),
                promoted_methods_out=_resolve(promoted_methods_out),
                promoted_numerics_out=_resolve(promoted_numerics_out),
                warnings=warnings,
            )
        raise FileNotFoundError(resolved_ingestion)

    link_file = resolved_ingestion / "discord_extracted_links.jsonl"
    method_file = resolved_ingestion / "discord_method_claim_candidates.jsonl"
    numeric_file = resolved_ingestion / "discord_numeric_observation_candidates.jsonl"
    if not link_file.is_file() or not method_file.is_file() or not numeric_file.is_file():
        if allow_missing:
            warnings.append("stage3n_generated_files_missing_promotion_skipped")
            return _write_empty_outputs(
                resolved_out=resolved_out,
                promoted_links_out=_resolve(promoted_links_out),
                promoted_methods_out=_resolve(promoted_methods_out),
                promoted_numerics_out=_resolve(promoted_numerics_out),
                warnings=warnings,
            )
        raise FileNotFoundError("Missing Stage 3N generated Discord extraction files")

    promoted_links, rejected_links = _promote_links(link_file)
    promoted_methods = _promote_methods(method_file)
    promoted_numerics = _promote_numerics(numeric_file)
    summary = _build_summary(
        out_dir=resolved_out,
        promoted_links=promoted_links,
        promoted_methods=promoted_methods,
        promoted_numerics=promoted_numerics,
        rejected_links=rejected_links,
        warnings=warnings,
    )
    resolved_out.mkdir(parents=True, exist_ok=True)
    write_jsonl(resolved_out / "promotion_candidates.jsonl", promoted_links + promoted_methods + promoted_numerics)
    write_jsonl(resolved_out / "rejected_private_or_unsafe_links.jsonl", rejected_links)
    write_jsonl(resolved_out / "warnings.jsonl", [{"warning": warning} for warning in warnings])
    write_json(resolved_out / "promotion_summary.json", summary)
    write_yaml(
        _resolve(promoted_links_out),
        {
            "record_type": "discord_promoted_public_source_links_stage3o",
            "source": SOURCE,
            "records": promoted_links,
        },
    )
    write_yaml(
        _resolve(promoted_methods_out),
        {
            "record_type": "discord_promoted_method_claim_candidates_stage3o",
            "source": SOURCE,
            "records": promoted_methods,
        },
    )
    write_yaml(
        _resolve(promoted_numerics_out),
        {
            "record_type": "discord_promoted_numeric_observation_candidates_stage3o",
            "source": SOURCE,
            "records": promoted_numerics,
        },
    )
    if warnings and not allow_warnings:
        raise RuntimeError("; ".join(warnings))
    return summary


def _promote_links(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    candidates: dict[str, dict[str, Any]] = {}
    rejected: list[dict[str, Any]] = []
    for record in iter_jsonl(path):
        url = str(record.get("normalized_url") or record.get("url") or "")
        safe_url = safe_public_url(url)
        if safe_url is None:
            rejected.append(_rejected_link(record, "private_or_nonpublic_url"))
            continue
        parsed = urlparse(safe_url)
        domain = parsed.netloc.lower()
        url_kind = str(record.get("url_kind", "unknown"))
        priority = link_priority(domain, url_kind)
        entry = candidates.get(safe_url)
        if entry is None:
            candidates[safe_url] = {
                "promoted_id": f"stage3o-public-link-{len(candidates) + 1:04d}",
                "source": SOURCE,
                "source_record_type": "discord_extracted_link",
                "url": safe_url,
                "domain": domain,
                "url_kind": url_kind,
                "source_class": SOURCE_CLASS_BY_KIND.get(url_kind, "archived_claim"),
                "priority": priority,
                "occurrence_count": 1,
                "redacted": True,
                "review_status": "human_review_required",
                "trusted_as_canonical": False,
                "raw_message_committed": False,
                "usernames_committed": False,
                "notes": "Promoted public source-discovery link from redacted Stage 3N output.",
            }
        else:
            entry["occurrence_count"] = int(entry["occurrence_count"]) + 1
            entry["priority"] = min(int(entry["priority"]), priority)
    promoted = sorted(
        candidates.values(),
        key=lambda item: (int(item["priority"]), str(item["domain"]), str(item["url"])),
    )[:MAX_SOURCE_LINKS]
    return promoted, rejected


def _promote_methods(path: Path) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, tuple[str, ...], str], dict[str, Any]] = {}
    for record in iter_jsonl(path):
        keywords = tuple(sorted(str(keyword) for keyword in record.get("extracted_keywords", [])))
        key = (str(record.get("claim_type", "unknown")), keywords, str(record.get("redacted_summary", "")))
        entry = grouped.get(key)
        if entry is None:
            grouped[key] = {
                "promoted_id": f"stage3o-method-claim-{len(grouped) + 1:04d}",
                "source": SOURCE,
                "source_record_type": "discord_method_claim_candidate",
                "claim_type": key[0],
                "extracted_keywords": list(keywords),
                "redacted_summary": key[2],
                "occurrence_count": 1,
                "redacted": True,
                "review_status": "human_review_required",
                "trusted_as_canonical": False,
                "raw_message_committed": False,
                "usernames_committed": False,
                "notes": "Keyword-only Discord method-claim lead; not promoted as fact.",
            }
        else:
            entry["occurrence_count"] = int(entry["occurrence_count"]) + 1
    return sorted(
        grouped.values(),
        key=lambda item: (
            method_priority(item),
            -int(item["occurrence_count"]),
            str(item["claim_type"]),
        ),
    )[:MAX_METHOD_CLAIMS]


def _promote_numerics(path: Path) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, tuple[int, ...], tuple[str, ...]], dict[str, Any]] = {}
    for record in iter_jsonl(path):
        numbers = tuple(sorted(int(number) for number in record.get("numbers", [])))
        keywords = tuple(sorted(str(keyword) for keyword in record.get("context_keywords", [])))
        key = (str(record.get("candidate_kind", "unknown")), numbers, keywords)
        entry = grouped.get(key)
        if entry is None:
            grouped[key] = {
                "promoted_id": f"stage3o-numeric-observation-{len(grouped) + 1:04d}",
                "source": SOURCE,
                "source_record_type": "discord_numeric_observation_candidate",
                "candidate_kind": key[0],
                "numbers": list(numbers),
                "context_keywords": list(keywords),
                "redacted_summary": str(record.get("redacted_summary", "")),
                "occurrence_count": 1,
                "redacted": True,
                "review_status": "human_review_required",
                "trusted_as_canonical": False,
                "raw_message_committed": False,
                "usernames_committed": False,
                "notes": "Numeric Discord observation lead; not promoted as fact or seed.",
            }
        else:
            entry["occurrence_count"] = int(entry["occurrence_count"]) + 1
    return sorted(
        grouped.values(),
        key=lambda item: (numeric_priority(item), -int(item["occurrence_count"]), str(item["numbers"])),
    )[:MAX_NUMERIC_OBSERVATIONS]


def _rejected_link(record: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "record_type": "discord_promotion_rejected_link",
        "source": SOURCE,
        "source_record_type": "discord_extracted_link",
        "link_id": record.get("link_id"),
        "domain": record.get("domain"),
        "url_kind": record.get("url_kind"),
        "reason": reason,
        "raw_message_committed": False,
        "usernames_committed": False,
        "notes": "Rejected from committed promotion set.",
    }


def _build_summary(
    *,
    out_dir: Path,
    promoted_links: list[dict[str, Any]],
    promoted_methods: list[dict[str, Any]],
    promoted_numerics: list[dict[str, Any]],
    rejected_links: list[dict[str, Any]],
    warnings: list[str],
) -> dict[str, Any]:
    domain_counts = Counter(str(record["domain"]) for record in promoted_links)
    return {
        "record_type": "discord_source_promotion_summary",
        "run_id": RUN_ID,
        "generated_at_utc": _utc_now(),
        "public_links_promoted_count": len(promoted_links),
        "method_claims_promoted_count": len(promoted_methods),
        "numeric_observations_promoted_count": len(promoted_numerics),
        "private_or_unsafe_links_rejected_count": len(rejected_links),
        "top_promoted_domains": dict(domain_counts.most_common(20)),
        "raw_message_bodies_committed": False,
        "usernames_committed": False,
        "private_attachment_urls_committed": False,
        "solve_claim": False,
        "output_paths": {
            "promotion_candidates": _display_path(out_dir / "promotion_candidates.jsonl"),
            "rejected_private_or_unsafe_links": _display_path(
                out_dir / "rejected_private_or_unsafe_links.jsonl"
            ),
            "summary": _display_path(out_dir / "promotion_summary.json"),
            "warnings": _display_path(out_dir / "warnings.jsonl"),
        },
        "warnings": warnings,
        "notes": "Promoted records are reviewable leads only, not Discord claims treated as facts.",
    }


def _write_empty_outputs(
    *,
    resolved_out: Path,
    promoted_links_out: Path,
    promoted_methods_out: Path,
    promoted_numerics_out: Path,
    warnings: list[str],
) -> dict[str, Any]:
    summary = _build_summary(
        out_dir=resolved_out,
        promoted_links=[],
        promoted_methods=[],
        promoted_numerics=[],
        rejected_links=[],
        warnings=warnings,
    )
    resolved_out.mkdir(parents=True, exist_ok=True)
    write_jsonl(resolved_out / "promotion_candidates.jsonl", [])
    write_jsonl(resolved_out / "rejected_private_or_unsafe_links.jsonl", [])
    write_jsonl(resolved_out / "warnings.jsonl", [{"warning": warning} for warning in warnings])
    write_json(resolved_out / "promotion_summary.json", summary)
    write_yaml(promoted_links_out, {"record_type": "discord_promoted_public_source_links_stage3o", "source": SOURCE, "records": []})
    write_yaml(promoted_methods_out, {"record_type": "discord_promoted_method_claim_candidates_stage3o", "source": SOURCE, "records": []})
    write_yaml(promoted_numerics_out, {"record_type": "discord_promoted_numeric_observation_candidates_stage3o", "source": SOURCE, "records": []})
    return summary


def load_summary(out_dir: Path) -> dict[str, Any]:
    return read_json(_resolve(out_dir) / "promotion_summary.json")


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root()).as_posix()
    except ValueError:
        return path.as_posix()
