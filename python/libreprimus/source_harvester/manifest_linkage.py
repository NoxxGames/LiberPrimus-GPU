"""Stage 5AG manifest-to-local-source linkage helpers."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .export import read_records, repo_relative, resolve, write_json, write_records
from .models import (
    MISSING_SOURCES_REPORT,
    SOURCE_MANIFEST_LINKAGE_REPORT,
    STAGE5AG_ID,
    STAGE5AG_LOCAL_LINKAGE_PATH,
    STAGE5AG_MANIFEST_EXTENSION_PATH,
    STAGE5AG_OUTPUT_DIR,
    STAGE5AG_SOURCE_STAGE_ID,
    UNCLASSIFIED_LOCAL_SOURCES_REPORT,
)

KNOWN_LOCAL_HINTS: dict[str, str] = {
    "The-Complete-Cicada3301-Archive-main": "complete_cicada3301_archive",
    "The-Complete-Cicada3301-Archive": "complete_cicada3301_archive",
    "CicadaSolversIddqd": "cicada_solvers_iddqd",
    "iddqd": "cicada_solvers_iddqd",
    "LiberPrimusPages": "liber_primus_dropbox_files",
    "DiskCipherStuff": "disk_cipher_theory_bundle_local",
    "GPPrimeView": "gp_prime_view",
    "dwh-hashkit": "tweqx_dwh_hashkit",
    "3301-hash-alarm": "tweqx_3301_hash_alarm",
}

NESTED_ARCHIVE_HINTS: dict[str, str] = {
    "2012": "user_uploaded_2012_archive",
    "2013": "user_uploaded_2013_archive",
    "2014": "user_uploaded_2014_archive",
    "2015": "user_uploaded_2015_archive",
    "2016": "user_uploaded_2016_archive",
    "2017": "user_uploaded_2017_archive",
    "assets": "user_uploaded_assets_archive",
    "ArchiveDir": "user_uploaded_archive_dir",
    "EXTRA WIKI PAGES": "user_uploaded_extra_wiki_pages",
}


def link_local_sources(
    *,
    manifest_path: Path,
    source_root: Path,
    results_dir: Path = STAGE5AG_OUTPUT_DIR,
    out: Path = STAGE5AG_LOCAL_LINKAGE_PATH,
    out_extension: Path = STAGE5AG_MANIFEST_EXTENSION_PATH,
) -> dict[str, Any]:
    """Link Stage 5AF manifest records to local top-level source material."""

    root = resolve(source_root)
    manifest_records = read_records(manifest_path)
    local_candidates = _local_candidates(root)
    extension_records = build_local_manifest_extensions(local_candidates)
    all_source_ids = {record["source_id"] for record in manifest_records}.union(
        record["source_id"] for record in extension_records
    )
    path_to_source_ids: dict[str, list[str]] = {}
    for candidate in local_candidates:
        source_id = candidate.get("matched_source_id")
        if source_id:
            path_to_source_ids.setdefault(source_id, []).append(candidate["path"])
    for extension_record in extension_records:
        local_path = extension_record.get("local_path")
        if isinstance(local_path, str) and local_path:
            path_to_source_ids.setdefault(extension_record["source_id"], []).append(local_path)

    records = []
    for manifest_record in manifest_records + extension_records:
        source_id = manifest_record["source_id"]
        matched_paths = sorted(set(path_to_source_ids.get(source_id, [])))
        status = "matched_exact" if matched_paths else "missing"
        if matched_paths and source_id.startswith("local_unclassified_"):
            status = "not_expected_local"
        if not matched_paths and manifest_record.get("manual_collection_required") is False and manifest_record.get("allow_network_fetch") is True:
            status = "missing"
        records.append(
            {
                "record_type": "stage5ag_manifest_local_linkage_record",
                "schema": "schemas/source-harvester/manifest-local-linkage-record-v0.schema.json",
                "stage_id": STAGE5AG_ID,
                "source_stage_id": STAGE5AG_SOURCE_STAGE_ID,
                "source_id": source_id,
                "expected_priority": manifest_record.get("priority", "deferred"),
                "source_type": manifest_record.get("source_type", "unknown"),
                "manual_collection_required": bool(manifest_record.get("manual_collection_required")),
                "local_match_status": status,
                "matched_paths": matched_paths,
                "confidence": "high" if matched_paths and status != "not_expected_local" else ("low" if matched_paths else "none"),
                "notes": _linkage_notes(status, bool(matched_paths)),
                "solve_claim": False,
            }
        )

    unclassified = [
        candidate
        for candidate in local_candidates
        if not candidate.get("matched_source_id") or candidate.get("matched_source_id") not in all_source_ids
    ]
    linkage = {
        "record_type": "stage5ag_manifest_local_linkage",
        "schema": "schemas/source-harvester/manifest-local-linkage-record-v0.schema.json",
        "stage_id": STAGE5AG_ID,
        "source_stage_id": STAGE5AG_SOURCE_STAGE_ID,
        "manifest_records_consumed": len(manifest_records),
        "extension_records": len(extension_records),
        "matched_count": sum(1 for record in records if record["local_match_status"].startswith("matched")),
        "missing_count": sum(1 for record in records if record["local_match_status"] == "missing"),
        "ambiguous_count": sum(1 for record in records if record["local_match_status"] == "ambiguous"),
        "unclassified_local_count": len(unclassified),
        "local_sources": local_candidates,
        "records": records,
        "solve_claim": False,
    }
    output_dir = resolve(results_dir)
    write_json(output_dir / SOURCE_MANIFEST_LINKAGE_REPORT, linkage)
    write_json(output_dir / MISSING_SOURCES_REPORT, [record for record in records if record["local_match_status"] == "missing"])
    write_json(output_dir / UNCLASSIFIED_LOCAL_SOURCES_REPORT, unclassified)
    write_records(out, records, **{key: linkage[key] for key in ("record_type", "schema", "stage_id", "source_stage_id", "manifest_records_consumed", "extension_records", "matched_count", "missing_count", "ambiguous_count", "unclassified_local_count", "solve_claim")})
    write_records(
        out_extension,
        extension_records,
        record_type="stage5ag_local_source_manifest_extension",
        schema="schemas/source-harvester/local-source-manifest-extension-record-v0.schema.json",
        stage_id=STAGE5AG_ID,
        source_stage_id=STAGE5AG_SOURCE_STAGE_ID,
    )
    return linkage


def build_local_manifest_extensions(local_candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build local-only source extension records for Stage 5AG."""

    records = [_disk_cipher_record()]
    for candidate in local_candidates:
        if candidate.get("matched_source_id"):
            continue
        source_id = f"local_unclassified_{_slug(candidate['entry_name'])}"
        records.append(
            {
                "source_id": source_id,
                "title": f"Unclassified local source: {candidate['entry_name']}",
                "source_type": "local_user_upload",
                "priority": "deferred",
                "source_tier": "unknown",
                "collection_status": "needs_manual_classification",
                "recommended_capture_modes": ["file_inventory", "hash_inventory"],
                "manual_collection_required": False,
                "allow_network_fetch": False,
                "allow_dynamic_browser": False,
                "raw_commit_allowed": False,
                "google_drive_storage_allowed": False,
                "what_it_supports": ["local_source_inventory_triage"],
                "what_it_does_not_support": ["solve_claims", "execution_ready_status"],
                "related_leads": [],
                "notes": "Stage 5AG local-only unclassified source record; requires manual classification.",
                "local_path": candidate["path"],
                "solve_claim": False,
            }
        )
    return [_extension_record(record) for record in records]


def _local_candidates(root: Path) -> list[dict[str, Any]]:
    if not root.exists():
        return []
    candidates: list[dict[str, Any]] = []
    for item in sorted(root.iterdir(), key=lambda path: path.name.lower()):
        if _is_tracked_scaffold(item) or _is_scaffold_only_directory(item):
            continue
        candidates.append(_candidate_for_item(item, root=root))
    complete_archive = root / "The-Complete-Cicada3301-Archive-main"
    if complete_archive.is_dir():
        for name, source_id in NESTED_ARCHIVE_HINTS.items():
            item = complete_archive / name
            if item.exists():
                candidates.append(_candidate_for_item(item, root=root, source_id=source_id))
    return candidates


def _candidate_for_item(item: Path, *, root: Path, source_id: str | None = None) -> dict[str, Any]:
    matched_source_id = source_id or KNOWN_LOCAL_HINTS.get(item.name)
    if not matched_source_id and item.suffix.lower() == ".zip":
        matched_source_id = NESTED_ARCHIVE_HINTS.get(item.stem)
    return {
        "path": repo_relative(item),
        "entry_name": item.name,
        "entry_type": "directory" if item.is_dir() else "file",
        "matched_source_id": matched_source_id,
        "match_confidence": "high" if matched_source_id else "none",
        "unclassified": matched_source_id is None,
        "manual_review_required": matched_source_id is None,
    }


def _linkage_notes(status: str, matched: bool) -> str:
    if status == "not_expected_local":
        return "Local ignored material found but no Stage 5AF manifest source matched; manual classification required."
    if matched:
        return "Local ignored material found."
    return "No local material matched in Stage 5AG inventory."


def _disk_cipher_record() -> dict[str, Any]:
    return {
        "source_id": "disk_cipher_theory_bundle_local",
        "title": "Discord disk-cipher / Alberti theory bundle",
        "source_type": "local_user_upload",
        "priority": "A2",
        "source_tier": "tier4_social_claim_or_screenshot",
        "collection_status": "local_inventory_candidate",
        "recommended_capture_modes": ["local_zip_hash", "file_inventory", "attachment_inventory"],
        "manual_collection_required": False,
        "allow_network_fetch": False,
        "allow_dynamic_browser": False,
        "raw_commit_allowed": False,
        "google_drive_storage_allowed": False,
        "what_it_supports": [
            "disk_cipher_alberti_hypothesis_source_lock",
            "book_cover_rotation_rule_claims",
            "punctuation_dot_branching_claims",
            "page39_claimed_output_review",
        ],
        "what_it_does_not_support": ["solve_claims", "execution_ready_status"],
        "related_leads": [
            "disk_cipher_alberti_lp_branching",
            "visual_depictions_rotation_reflection",
            "rune_pixel_variants",
        ],
        "notes": "Source-lock and formalisation candidate only; high false-positive risk.",
        "solve_claim": False,
    }


def _extension_record(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "record_type": "stage5ag_local_source_manifest_extension_record",
        "schema": "schemas/source-harvester/local-source-manifest-extension-record-v0.schema.json",
        "stage_id": STAGE5AG_ID,
        "source_stage_id": STAGE5AG_SOURCE_STAGE_ID,
        **record,
    }


def _is_tracked_scaffold(item: Path) -> bool:
    return item.name in {"README.md", ".gitkeep"}


def _is_scaffold_only_directory(item: Path) -> bool:
    if not item.is_dir():
        return False
    children = list(item.rglob("*"))
    if not children:
        return True
    files = [child for child in children if child.is_file()]
    if any(child.is_dir() for child in children) and not files:
        return False
    return bool(files) and all(child.name in {"README.md", ".gitkeep"} for child in files)


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "unknown"
