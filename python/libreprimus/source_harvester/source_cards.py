"""Stage 5AI source-card generation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_records, write_json, write_jsonl, write_records
from .models import (
    STAGE5AI_BUNDLE_ROOT,
    STAGE5AI_ID,
    STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
    STAGE5AI_OUTPUT_DIR,
    STAGE5AI_REPORTS,
    STAGE5AI_SOURCE_CARD_SUMMARY_PATH,
    STAGE5AI_SOURCE_STAGE_ID,
)


TEXT_EXTENSIONS = {".txt", ".md", ".markdown", ".html", ".htm", ".json", ".yaml", ".yml", ".csv"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".ogg"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi", ".webm"}
DOC_EXTENSIONS = {".pdf", ".docx", ".doc", ".xlsx", ".xls"}


def build_source_cards(
    *,
    local_linkage_path: Path,
    candidate_summary_path: Path,
    classification_path: Path,
    bundle_plan_path: Path,
    bundle_root: Path = STAGE5AI_BUNDLE_ROOT,
    results_dir: Path = STAGE5AI_OUTPUT_DIR,
    out: Path = STAGE5AI_SOURCE_CARD_SUMMARY_PATH,
) -> dict[str, Any]:
    """Build website-ingestible source-card metadata for matched and unclassified sources."""

    del candidate_summary_path
    linkages = read_records(local_linkage_path)
    bundle_plan = read_records(bundle_plan_path)
    classifications = {record["source_id"]: record for record in read_records(classification_path)}
    source_to_bundles: dict[str, list[str]] = {}
    source_to_categories: dict[str, list[str]] = {}
    for bundle in bundle_plan:
        bundle_id = bundle["bundle_id"]
        for source_id in bundle.get("included_source_ids", []):
            source_to_bundles.setdefault(source_id, []).append(bundle_id)
            source_to_categories.setdefault(source_id, []).extend(bundle.get("included_clue_categories", []))
    for source_id, classification in classifications.items():
        source_to_bundles[source_id] = list(classification["provisional_bundle_ids"])
        source_to_categories[source_id] = list(classification["provisional_clue_categories"])

    cards = []
    for linkage in linkages:
        source_id = str(linkage.get("source_id", ""))
        local_status = str(linkage.get("local_match_status", ""))
        if local_status not in {"matched_exact", "matched_probable", "not_expected_local"}:
            continue
        if local_status == "not_expected_local" and source_id not in classifications:
            continue
        paths = [str(path) for path in linkage.get("matched_paths", [])]
        classification = classifications.get(source_id, {})
        private = _is_private_or_sensitive(source_id, paths, classification)
        source_type = str(linkage.get("source_type", "local_user_upload"))
        card = {
            "source_id": source_id,
            "title": _title(source_id),
            "source_type": source_type,
            "source_tier": _source_tier(source_type, private),
            "priority": str(linkage.get("expected_priority", "deferred")),
            "bundle_ids": source_to_bundles.get(source_id, []),
            "clue_categories": sorted(set(source_to_categories.get(source_id, []))),
            "local_match_status": local_status,
            "local_source_paths_redacted_or_relative": paths,
            "hashes": [],
            "file_counts": _file_counts(paths),
            "content_types": _content_types(paths),
            "readiness_status": "local_metadata_ready",
            "risk_level": "private_or_sensitive" if private else "review_required",
            "what_it_supports": "Local provenance and extraction planning only.",
            "what_it_does_not_support": "No solve claim, canonical corpus activation, or public publication.",
            "do_not_assume": [
                "Do not treat local availability as source truth.",
                "Do not publish raw or generated extract bodies without future review.",
            ],
            "known_questions": ["Which source-lock policy should govern future publication review?"],
            "recommended_future_use": "Use as private Deep Research input metadata after review.",
            "raw_content_publication_allowed": False,
            "generated_extract_publication_allowed": False,
            "website_publication_allowed": False,
            "publication_status": "blocked_private_or_sensitive" if private else "generated_extract_review_required",
            "redaction_required": private,
            "solve_claim": False,
        }
        cards.append(card)
    cards.sort(key=lambda card: card["source_id"])
    summary = {
        "record_type": "stage5ai_curated_source_card_summary",
        "schema": "schemas/source-harvester/curated-source-card-summary-v0.schema.json",
        "stage_id": STAGE5AI_ID,
        "source_stage_id": STAGE5AI_SOURCE_STAGE_ID,
        "local_inventory_stage_id": STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
        "source_card_records": len(cards),
        "matched_local_source_cards": sum(1 for card in cards if card["local_match_status"] in {"matched_exact", "matched_probable"}),
        "unclassified_source_cards": sum(1 for card in cards if str(card["source_id"]).startswith("local_unclassified_")),
        "private_or_sensitive_source_cards": sum(1 for card in cards if card["publication_status"] == "blocked_private_or_sensitive"),
        "website_publication_allowed_count": 0,
        "raw_content_publication_allowed": False,
        "generated_extract_publication_allowed": False,
        "solve_claim": False,
    }
    root = _ensure_bundle_root(bundle_root)
    write_jsonl(root / "source_cards.jsonl", cards)
    write_jsonl(results_dir / STAGE5AI_REPORTS["source_cards"], cards)
    write_records(out, cards, **summary)
    write_json(results_dir / "curated_source_card_summary.json", {**summary, "records": cards})
    return {**summary, "records": cards}


def _ensure_bundle_root(bundle_root: Path) -> Path:
    bundle_root.mkdir(parents=True, exist_ok=True)
    return bundle_root


def _title(source_id: str) -> str:
    return source_id.replace("_", " ").replace("-", " ").title()


def _source_tier(source_type: str, private: bool) -> str:
    if private:
        return "tier4_social_claim_or_screenshot"
    if source_type in {"github_repo", "github_org"}:
        return "tier1_committed_repo_record"
    if source_type in {"dropbox_folder", "local_user_upload"}:
        return "tier3_reproducible_community_data"
    return "unknown"


def _is_private_or_sensitive(source_id: str, paths: list[str], classification: dict[str, Any]) -> bool:
    joined = " ".join([source_id, *paths]).lower()
    return (
        "discord" in joined
        or "communityobservations" in joined
        or classification.get("publication_status") == "blocked_private_or_sensitive"
    )


def _content_types(paths: list[str]) -> list[str]:
    content_types = set()
    for path in paths:
        suffix = Path(path).suffix.lower()
        if suffix in TEXT_EXTENSIONS:
            content_types.add("text")
        elif suffix in IMAGE_EXTENSIONS:
            content_types.add("image")
        elif suffix in AUDIO_EXTENSIONS:
            content_types.add("audio")
        elif suffix in VIDEO_EXTENSIONS:
            content_types.add("video")
        elif suffix in DOC_EXTENSIONS:
            content_types.add("document")
        elif suffix in {".zip", ".7z", ".tar", ".gz"}:
            content_types.add("archive")
        elif suffix:
            content_types.add("attachment")
        else:
            content_types.add("directory")
    return sorted(content_types or {"metadata"})


def _file_counts(paths: list[str]) -> dict[str, int]:
    counts = {"path_count": len(paths), "file_count": 0, "dir_count": 0}
    for path in paths:
        local = Path(path)
        if local.is_file():
            counts["file_count"] += 1
        elif local.is_dir():
            counts["dir_count"] += 1
    return counts
