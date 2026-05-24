"""Stage 5AJ UsefulFilesAndIdeas inventory and bundle metadata helpers."""

from __future__ import annotations

import mimetypes
from pathlib import Path
from typing import Any

from PIL import Image

from .export import read_records, read_yaml, repo_relative, resolve, write_json, write_jsonl, write_records, write_yaml
from .hashing import hash_file
from .models import (
    RESEARCH_BUNDLE_PLAN_PATH,
    STAGE5AI_READINESS_PATH,
    STAGE5AJ_BUNDLE_ROOT,
    STAGE5AJ_CONTENT_INDEX_SUMMARY_PATH,
    STAGE5AJ_DEEP_RESEARCH_UPDATE_PATH,
    STAGE5AJ_ID,
    STAGE5AJ_INVENTORY_PATH,
    STAGE5AJ_MISSING_SOURCE_PLAN_PATH,
    STAGE5AJ_OUTPUT_DIR,
    STAGE5AJ_READINESS_PATH,
    STAGE5AJ_REPORTS,
    STAGE5AJ_SOURCE_CARD_SUMMARY_PATH,
    STAGE5AJ_SOURCE_ROOT,
    STAGE5AJ_SOURCE_STAGE_ID,
    STAGE5AJ_WEBSITE_UPDATE_PATH,
)


LOCAL_SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "lp_excel_workbook_local": {
        "title": "LP Excel delimiter-preserving Liber Primus workbook",
        "priority": "A1",
        "source_tier": "tier3_reproducible_community_data",
        "filenames": {"lp excel.xlsx"},
        "bundle_ids": [
            "02-liber-primus-images-and-transcriptions",
            "03-page-49-51-token-block",
            "04-cuneiform-base60-base59",
            "05-red-markers-and-visual-numerics",
            "07-boundary-mobius-repeated-fragments",
        ],
        "clue_categories": [
            "delimiter_preserving_lp_transcript",
            "manual_highlight_repeat_fragments",
            "section_boundary_repeat_network",
            "lp_count_policy_reconciliation",
            "excel_highlight_color_annotations",
            "workbook_formula_and_image_inventory",
        ],
        "recommended_capture_modes": [
            "xlsx_hash",
            "workbook_sheet_inventory",
            "workbook_cell_metadata",
            "workbook_highlight_metadata",
            "workbook_formula_inventory",
            "workbook_image_inventory",
            "delimiter_policy_extract",
            "rune_count_extract",
            "section_stream_extract",
        ],
    },
    "translations_decryptions_xlsx_local": {
        "title": "Translations/decryptions solved-page spreadsheet export",
        "priority": "A1",
        "source_tier": "tier3_reproducible_community_data",
        "filenames": {"tranlsations decryptions.xlsx", "translations decryptions.xlsx"},
        "bundle_ids": [
            "02-liber-primus-images-and-transcriptions",
            "08-tools-gpprime-dwh-gematria",
            "10-known-negative-retired-ideas",
        ],
        "clue_categories": [
            "p56_p57_gp_sum_3301_1033",
            "unverified_shift_pattern_warning",
            "workbook_formula_and_image_inventory",
        ],
        "recommended_capture_modes": [
            "xlsx_hash",
            "sheet_inventory",
            "prime_sums_extract",
            "p56_p57_fixture_extract",
            "solved_page_shift_vector_extract",
            "embedded_image_inventory",
        ],
    },
    "usefulfiles_important_links_local": {
        "title": "UsefulFilesAndIdeas important links list",
        "priority": "A1",
        "source_tier": "tier3_reproducible_community_data",
        "filenames": {"important links.txt", "important link.txt"},
        "bundle_ids": [
            "03-page-49-51-token-block",
            "06-outguess-stego-hidden-formatting",
            "08-tools-gpprime-dwh-gematria",
            "09-community-hypotheses",
        ],
        "clue_categories": ["source_gap_closure", "reddit_claims_targeted_capture"],
        "recommended_capture_modes": [
            "text_hash",
            "url_extraction",
            "source_manifest_extension",
            "link_deduplication",
            "source_priority_classification",
        ],
    },
    "usefulfiles_ideas_local": {
        "title": "UsefulFilesAndIdeas idea seeds",
        "priority": "A2",
        "source_tier": "tier4_social_claim_or_screenshot",
        "filenames": {"ideas.txt"},
        "bundle_ids": ["09-community-hypotheses", "10-known-negative-retired-ideas"],
        "clue_categories": ["brown_corpus_word_length_controls", "bibliographic_liber_primus_euler_lead"],
        "recommended_capture_modes": ["text_hash", "idea_seed_index", "future_null_control_notes"],
    },
    "gematria_primus_image_local": {
        "title": "Gematria Primus visual table image",
        "priority": "A2",
        "source_tier": "tier3_reproducible_community_data",
        "filenames": {"gematrria primus.jpg", "gematria primus.jpg", "gematrria primus.jpeg", "gematria primus.jpeg", "gematrriaprimus.jpg", "gematriaprimus.jpg"},
        "bundle_ids": ["02-liber-primus-images-and-transcriptions", "05-red-markers-and-visual-numerics", "08-tools-gpprime-dwh-gematria"],
        "clue_categories": ["visual_gematria_reference"],
        "recommended_capture_modes": ["image_hash", "image_metadata"],
    },
}


def inventory_usefulfiles(
    *,
    source_root: Path = STAGE5AJ_SOURCE_ROOT,
    results_dir: Path = STAGE5AJ_OUTPUT_DIR,
    out: Path = STAGE5AJ_INVENTORY_PATH,
) -> dict[str, Any]:
    """Inventory UsefulFilesAndIdeas without committing raw files."""

    root = resolve(source_root)
    records: list[dict[str, Any]] = []
    if root.exists():
        for path in sorted(root.rglob("*"), key=lambda item: item.as_posix().lower()):
            if not path.is_file():
                continue
            hashed = hash_file(path)
            source_id = source_id_for_filename(path.name)
            image_metadata = _image_metadata(path) if path.suffix.lower() in {".jpg", ".jpeg", ".png"} else {}
            record = {
                "record_type": "stage5aj_usefulfiles_local_inventory_record",
                "schema": "schemas/source-harvester/usefulfiles-local-inventory-record-v0.schema.json",
                "stage_id": STAGE5AJ_ID,
                "source_stage_id": STAGE5AJ_SOURCE_STAGE_ID,
                "source_id": source_id,
                "file_name": path.name,
                "relative_path": repo_relative(path),
                "extension": path.suffix.lower(),
                "size_bytes": hashed["size_bytes"],
                "sha256": hashed["sha256"],
                "mime_guess": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
                "source_type": "local_user_upload",
                "priority": source_spec(source_id).get("priority", "deferred") if source_id else "deferred",
                "collection_status": "local_ready" if source_id else "local_unclassified",
                "raw_file_committed": False,
                "generated_outputs_committed": False,
                "solve_claim": False,
                **image_metadata,
            }
            records.append(record)
    summary = {
        "record_type": "stage5aj_usefulfiles_local_inventory",
        "schema": "schemas/source-harvester/usefulfiles-local-inventory-record-v0.schema.json",
        "stage_id": STAGE5AJ_ID,
        "source_stage_id": STAGE5AJ_SOURCE_STAGE_ID,
        "source_root": source_root.as_posix(),
        "local_folder_exists": root.exists(),
        "usefulfiles_local_file_count": len(records),
        "usefulfiles_total_size_bytes": sum(int(record["size_bytes"]) for record in records),
        "xlsx_files_found": sum(1 for record in records if record["extension"] == ".xlsx"),
        "important_links_found": any(record["source_id"] == "usefulfiles_important_links_local" for record in records),
        "ideas_found": any(record["source_id"] == "usefulfiles_ideas_local" for record in records),
        "gematria_image_found": any(record["source_id"] == "gematria_primus_image_local" for record in records),
        "source_ids_added": sorted({record["source_id"] for record in records if record.get("source_id")}),
        "raw_data_committed": False,
        "generated_outputs_committed": False,
        "solve_claim": False,
    }
    write_records(out, records, **summary)
    write_json(results_dir / STAGE5AJ_REPORTS["inventory"], {**summary, "records": records})
    return {**summary, "records": records}


def build_usefulfiles_source_cards(
    *,
    inventory_path: Path,
    xlsx_summary_path: Path,
    important_links_path: Path,
    manifest_extension_path: Path,
    bundle_plan_path: Path = RESEARCH_BUNDLE_PLAN_PATH,
    out_source_card_summary: Path = STAGE5AJ_SOURCE_CARD_SUMMARY_PATH,
    out_content_index_summary: Path = STAGE5AJ_CONTENT_INDEX_SUMMARY_PATH,
    results_dir: Path = STAGE5AJ_OUTPUT_DIR,
) -> dict[str, Any]:
    """Create source-card and content-index summary updates for Stage 5AJ."""

    del bundle_plan_path
    inventory = read_yaml(inventory_path)
    xlsx = read_yaml(xlsx_summary_path)
    links = read_yaml(important_links_path)
    extension_records = read_records(manifest_extension_path)
    inventory_records = inventory.get("records", [])
    cards = []
    for record in inventory_records:
        source_id = record.get("source_id")
        if not source_id:
            continue
        spec = source_spec(str(source_id))
        cards.append(_local_source_card(record, spec))
    for record in extension_records:
        if record.get("source_type") == "local_user_upload":
            continue
        cards.append(_url_source_card(record))
    cards.sort(key=lambda item: (item["bundle_ids"][0] if item["bundle_ids"] else "", item["source_id"]))
    content_records = [_content_record(card) for card in cards]
    source_summary = {
        "record_type": "stage5aj_usefulfiles_source_card_summary",
        "schema": "schemas/source-harvester/curated-source-card-summary-v0.schema.json",
        "stage_id": STAGE5AJ_ID,
        "source_stage_id": STAGE5AJ_SOURCE_STAGE_ID,
        "source_card_records": len(cards),
        "local_source_card_records": sum(1 for card in cards if card["source_type"] == "local_user_upload"),
        "url_source_card_records": sum(1 for card in cards if card["source_type"] != "local_user_upload"),
        "publication_review_required_count": len(cards),
        "website_publication_allowed_count": 0,
        "private_deep_research_extract_ready_count": len(cards),
        "xlsx_workbooks_summarized": xlsx.get("xlsx_workbooks_summarized", 0),
        "important_links_urls_found": links.get("important_links_urls_found", 0),
        "raw_content_publication_allowed": False,
        "generated_extract_publication_allowed": False,
        "solve_claim": False,
    }
    content_summary = {
        "record_type": "stage5aj_usefulfiles_content_index_summary",
        "schema": "schemas/source-harvester/curated-content-index-summary-v0.schema.json",
        "stage_id": STAGE5AJ_ID,
        "source_stage_id": STAGE5AJ_SOURCE_STAGE_ID,
        "content_index_records": len(content_records),
        "source_card_records": len(cards),
        "website_publication_allowed_count": 0,
        "private_deep_research_ready_count": len(content_records),
        "generated_extract_review_required_count": len(content_records),
        "blocked_private_or_sensitive_count": 0,
        "raw_bodies_committed": False,
        "generated_outputs_committed": False,
        "solve_claim": False,
    }
    write_records(out_source_card_summary, cards, **source_summary)
    write_records(out_content_index_summary, content_records, **content_summary)
    write_jsonl(results_dir / "source_card_index.jsonl", cards)
    write_jsonl(results_dir / "content_extract_index.jsonl", content_records)
    return {**source_summary, "content_index_records": len(content_records)}


def update_deep_research_packs(
    *,
    stage5ai_bundle_root: Path,
    usefulfiles_inventory_path: Path,
    source_card_summary_path: Path,
    content_index_summary_path: Path,
    bundle_root: Path = STAGE5AJ_BUNDLE_ROOT,
    results_dir: Path = STAGE5AJ_OUTPUT_DIR,
    out_website_update: Path = STAGE5AJ_WEBSITE_UPDATE_PATH,
    out_deep_research_update: Path = STAGE5AJ_DEEP_RESEARCH_UPDATE_PATH,
    out_readiness: Path = STAGE5AJ_READINESS_PATH,
    out_missing_source_plan: Path = STAGE5AJ_MISSING_SOURCE_PLAN_PATH,
) -> dict[str, Any]:
    """Write ignored Stage 5AJ bundle update indexes and compact committed summaries."""

    del usefulfiles_inventory_path
    source_cards = read_records(source_card_summary_path)
    content_records = read_records(content_index_summary_path)
    prior_readiness = read_yaml(STAGE5AI_READINESS_PATH)
    prior_ready = int(prior_readiness.get("bundles_ready_for_private_deep_research", 0))
    bundle_root_resolved = resolve(bundle_root)
    bundle_root_resolved.mkdir(parents=True, exist_ok=True)
    (bundle_root_resolved / "README.md").write_text(
        "# Stage 5AJ Research Inputs\n\nGenerated and ignored UsefulFilesAndIdeas bundle update metadata.\n",
        encoding="utf-8",
    )
    write_jsonl(bundle_root / "source_cards.jsonl", source_cards)
    write_jsonl(bundle_root / "content_index.jsonl", content_records)
    write_yaml(
        bundle_root / "master_manifest.yaml",
        {
            "stage_id": STAGE5AJ_ID,
            "source_stage_id": STAGE5AJ_SOURCE_STAGE_ID,
            "source_card_count": len(source_cards),
            "content_record_count": len(content_records),
            "stage5ai_bundle_root": stage5ai_bundle_root.as_posix(),
            "website_expansion_performed": False,
            "deep_research_performed": False,
            "solve_claim": False,
        },
    )
    write_jsonl(bundle_root / "extraction_warnings.jsonl", [])
    website = {
        "record_type": "stage5aj_website_ingest_update_summary",
        "schema": "schemas/source-harvester/deep-research-pack-update-summary-v0.schema.json",
        "stage_id": STAGE5AJ_ID,
        "source_stage_id": STAGE5AJ_SOURCE_STAGE_ID,
        "website_ingest_metadata_ready": True,
        "website_ingest_source_card_records": len(source_cards),
        "website_ingest_content_records": len(content_records),
        "website_expansion_performed": False,
        "public_website_ready_count": 0,
        "publication_review_required_count": len(content_records),
        "solve_claim": False,
    }
    deep = {
        "record_type": "stage5aj_deep_research_pack_update_summary",
        "schema": "schemas/source-harvester/deep-research-pack-update-summary-v0.schema.json",
        "stage_id": STAGE5AJ_ID,
        "source_stage_id": STAGE5AJ_SOURCE_STAGE_ID,
        "deep_research_pack_records": len({record["bundle_id"] for record in content_records}),
        "deep_research_performed": False,
        "private_deep_research_ready_count": len(content_records),
        "source_card_update_records": len(source_cards),
        "content_index_update_records": len(content_records),
        "solve_claim": False,
    }
    readiness_records = _bundle_readiness_records(content_records, prior_readiness)
    readiness = {
        "record_type": "stage5aj_research_bundle_readiness",
        "schema": "schemas/source-harvester/deep-research-pack-update-summary-v0.schema.json",
        "stage_id": STAGE5AJ_ID,
        "source_stage_id": STAGE5AJ_SOURCE_STAGE_ID,
        "bundle_readiness_before": prior_ready,
        "bundle_readiness_after": sum(1 for record in readiness_records if record["ready_for_private_deep_research"]),
        "bundles_ready_for_private_deep_research": sum(
            1 for record in readiness_records if record["ready_for_private_deep_research"]
        ),
        "bundles_public_website_ready": 0,
        "website_ingest_metadata_ready": True,
        "solve_claim": False,
    }
    missing_records = _missing_source_records()
    missing = {
        "record_type": "stage5aj_missing_source_plan_update",
        "schema": "schemas/source-harvester/missing-source-plan-v0.schema.json",
        "stage_id": STAGE5AJ_ID,
        "source_stage_id": STAGE5AJ_SOURCE_STAGE_ID,
        "missing_source_records": len(missing_records),
        "now_local_count": sum(1 for record in missing_records if record["status"] == "now_local"),
        "new_online_source_added_count": sum(1 for record in missing_records if record["status"] == "new_online_source_added"),
        "still_missing_online_fetch_count": sum(1 for record in missing_records if record["status"] == "still_missing_online_fetch"),
        "private_or_publication_blocked_count": sum(1 for record in missing_records if record["status"] == "private_or_publication_blocked"),
        "network_fetch_performed": False,
        "solve_claim": False,
    }
    write_yaml(out_website_update, website)
    write_yaml(out_deep_research_update, deep)
    write_records(out_readiness, readiness_records, **readiness)
    write_records(out_missing_source_plan, missing_records, **missing)
    write_json(results_dir / "website_ingest_update_report.json", website)
    write_json(results_dir / STAGE5AJ_REPORTS["deep_research_update"], deep)
    return {**deep, "website": website, "readiness": readiness, "missing": missing}


def source_id_for_filename(filename: str) -> str | None:
    normalized = filename.lower().replace("_", " ").replace("-", " ")
    normalized = " ".join(normalized.split())
    for source_id, spec in LOCAL_SOURCE_SPECS.items():
        if normalized in spec["filenames"]:
            return source_id
    return None


def source_spec(source_id: str | None) -> dict[str, Any]:
    if source_id and source_id in LOCAL_SOURCE_SPECS:
        return LOCAL_SOURCE_SPECS[source_id]
    return {}


def _image_metadata(path: Path) -> dict[str, Any]:
    try:
        with Image.open(path) as image:
            return {
                "image_width": image.width,
                "image_height": image.height,
                "image_mode": image.mode,
                "image_format": image.format,
                "ocr_performed": False,
                "image_forensics_performed": False,
            }
    except OSError:
        return {"ocr_performed": False, "image_forensics_performed": False}


def _local_source_card(record: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "record_type": "stage5aj_usefulfiles_source_card",
        "stage_id": STAGE5AJ_ID,
        "source_id": record["source_id"],
        "title": spec.get("title", record["file_name"]),
        "source_type": "local_user_upload",
        "priority": spec.get("priority", "deferred"),
        "source_tier": spec.get("source_tier", "unknown"),
        "bundle_ids": spec.get("bundle_ids", []),
        "clue_categories": spec.get("clue_categories", []),
        "local_source_paths_redacted_or_relative": [record["relative_path"]],
        "recommended_capture_modes": spec.get("recommended_capture_modes", []),
        "content_types": [_content_type(record.get("extension", ""))],
        "publication_status": "generated_extract_review_required",
        "raw_content_publication_allowed": False,
        "generated_extract_publication_allowed": False,
        "website_publication_allowed": False,
        "private_deep_research_allowed": True,
        "redaction_required": False,
        "solve_claim": False,
    }


def _url_source_card(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "record_type": "stage5aj_usefulfiles_source_card",
        "stage_id": STAGE5AJ_ID,
        "source_id": record["source_id"],
        "title": record["title"],
        "source_type": record["source_type"],
        "priority": record["priority"],
        "source_tier": record["source_tier"],
        "bundle_ids": record.get("bundle_ids", []),
        "clue_categories": record.get("related_leads", []),
        "url": record.get("url"),
        "recommended_capture_modes": record.get("recommended_capture_modes", []),
        "content_types": ["web_metadata"],
        "publication_status": "generated_extract_review_required",
        "raw_content_publication_allowed": False,
        "generated_extract_publication_allowed": False,
        "website_publication_allowed": False,
        "private_deep_research_allowed": True,
        "redaction_required": record["source_type"].startswith("reddit"),
        "solve_claim": False,
    }


def _content_record(card: dict[str, Any]) -> dict[str, Any]:
    bundle_id = card.get("bundle_ids", ["09-community-hypotheses"])[0]
    return {
        "record_type": "stage5aj_content_index_record",
        "stage_id": STAGE5AJ_ID,
        "content_id": f"{bundle_id}::{card['source_id']}",
        "bundle_id": bundle_id,
        "source_id": card["source_id"],
        "title": card["title"],
        "content_kind": "metadata_only",
        "relative_generated_path": f"{bundle_id}/extracted_text/{card['source_id']}-metadata.md",
        "publication_status": card["publication_status"],
        "private_deep_research_ready": True,
        "website_publication_allowed": False,
        "redaction_required": card["redaction_required"],
        "solve_claim": False,
    }


def _content_type(extension: str) -> str:
    if extension == ".xlsx":
        return "workbook"
    if extension == ".txt":
        return "text"
    if extension in {".jpg", ".jpeg", ".png"}:
        return "image_metadata"
    return "metadata"


def _bundle_readiness_records(
    content_records: list[dict[str, Any]], prior_readiness: dict[str, Any]
) -> list[dict[str, Any]]:
    prior_records = {
        record["bundle_id"]: record
        for record in prior_readiness.get("records", [])
        if isinstance(record, dict) and record.get("bundle_id")
    }
    bundle_ids = set(prior_records) | {record["bundle_id"] for record in content_records}
    records = []
    for bundle in sorted(bundle_ids):
        count = sum(1 for record in content_records if record["bundle_id"] == bundle)
        prior_ready = bool(prior_records.get(bundle, {}).get("ready_for_private_deep_research", False))
        now_ready = prior_ready or count > 0
        records.append(
            {
                "record_type": "stage5aj_research_bundle_readiness_record",
                "stage_id": STAGE5AJ_ID,
                "bundle_id": bundle,
                "content_index_update_records": count,
                "stage5ai_ready_for_private_deep_research": prior_ready,
                "ready_for_private_deep_research": now_ready,
                "public_website_ready": False,
                "readiness_status": (
                    "usefulfiles_update_ready_for_private_deep_research"
                    if count > 0
                    else "stage5ai_readiness_preserved"
                ),
                "solve_claim": False,
            }
        )
    return records


def _missing_source_records() -> list[dict[str, Any]]:
    return [
        {
            "record_type": "stage5aj_missing_source_plan_record",
            "stage_id": STAGE5AJ_ID,
            "source_id": "solved_page_google_sheet",
            "status": "now_local",
            "replacement_source_id": "translations_decryptions_xlsx_local",
            "network_fetch_required": False,
            "solve_claim": False,
        },
        {
            "record_type": "stage5aj_missing_source_plan_record",
            "stage_id": STAGE5AJ_ID,
            "source_id": "chapterized_rune_map_google_doc",
            "status": "still_missing_manual_export",
            "network_fetch_required": False,
            "solve_claim": False,
        },
        {
            "record_type": "stage5aj_missing_source_plan_record",
            "stage_id": STAGE5AJ_ID,
            "source_id": "fandom_stage5aj_new_links",
            "status": "new_online_source_added",
            "network_fetch_required": True,
            "solve_claim": False,
        },
        {
            "record_type": "stage5aj_missing_source_plan_record",
            "stage_id": STAGE5AJ_ID,
            "source_id": "reddit_stage5aj_targeted_posts",
            "status": "new_online_source_added",
            "network_fetch_required": True,
            "solve_claim": False,
        },
        {
            "record_type": "stage5aj_missing_source_plan_record",
            "stage_id": STAGE5AJ_ID,
            "source_id": "discord_private_leads",
            "status": "private_or_publication_blocked",
            "network_fetch_required": False,
            "solve_claim": False,
        },
    ]
