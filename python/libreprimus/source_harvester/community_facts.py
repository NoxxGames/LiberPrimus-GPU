"""Stage 5AK community-facts local source integration."""

from __future__ import annotations

import hashlib
import mimetypes
from pathlib import Path
from typing import Any

from .export import read_yaml, repo_relative, resolve, write_json, write_jsonl, write_records, write_yaml
from .hashing import hash_file
from .models import (
    RESEARCH_BUNDLE_PLAN_PATH,
    STAGE5AK_BUNDLE_ROOT,
    STAGE5AK_CONTENT_INDEX_SUMMARY_PATH,
    STAGE5AK_DEEP_RESEARCH_UPDATE_PATH,
    STAGE5AK_ID,
    STAGE5AK_INVENTORY_PATH,
    STAGE5AK_MISSING_SOURCE_PLAN_PATH,
    STAGE5AK_OUTPUT_DIR,
    STAGE5AK_READINESS_PATH,
    STAGE5AK_REPORTS,
    STAGE5AK_SOURCE_CARD_SUMMARY_PATH,
    STAGE5AK_SOURCE_ROOT,
    STAGE5AK_SOURCE_STAGE_ID,
    STAGE5AK_WEBSITE_UPDATE_PATH,
)


COMMUNITY_SOURCE_ID = "community_facts_observations_local"
COMMUNITY_BUNDLE_ID = "09-community-hypotheses"


def inventory_community_facts(
    *,
    source_root: Path = STAGE5AK_SOURCE_ROOT,
    results_dir: Path = STAGE5AK_OUTPUT_DIR,
    out: Path = STAGE5AK_INVENTORY_PATH,
) -> dict[str, Any]:
    """Inventory the local community-facts folder without committing raw content."""

    root = resolve(source_root)
    files = sorted([path for path in root.iterdir() if path.is_file()], key=lambda item: item.name.lower()) if root.exists() else []
    records = []
    for path in files:
        hashed = hash_file(path)
        records.append(
            {
                "record_type": "stage5ak_community_facts_local_file_record",
                "schema": "schemas/source-harvester/community-facts-local-inventory-record-v0.schema.json",
                "stage_id": STAGE5AK_ID,
                "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
                "source_id": COMMUNITY_SOURCE_ID,
                "file_name": path.name,
                "relative_path": repo_relative(path),
                "extension": path.suffix.lower(),
                "size_bytes": hashed["size_bytes"],
                "sha256": hashed["sha256"],
                "mime_guess": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
                "source_type": "local_user_upload",
                "collection_status": "local_ready",
                "raw_file_committed": False,
                "generated_outputs_committed": False,
                "solve_claim": False,
            }
        )
    message_log = next((path for path in files if path.name.lower() == "community-facts-collection.txt"), None)
    message_index = _message_index(message_log) if message_log else []
    source_record = _source_manifest_record(source_root)
    summary = {
        "record_type": "stage5ak_community_facts_local_inventory",
        "schema": "schemas/source-harvester/community-facts-local-inventory-record-v0.schema.json",
        "stage_id": STAGE5AK_ID,
        "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
        "source_id": COMMUNITY_SOURCE_ID,
        "source_root": source_root.as_posix(),
        "local_folder_exists": root.exists(),
        "community_facts_file_count": len(records),
        "community_facts_total_size_bytes": sum(int(record["size_bytes"]) for record in records),
        "message_log_detected": message_log is not None,
        "message_log_path": repo_relative(message_log) if message_log else None,
        "message_log_hash": hash_file(message_log)["sha256"] if message_log else None,
        "message_log_line_count": len(message_index),
        "attachment_images_detected": sum(1 for record in records if record["extension"] == ".webp"),
        "new_local_source_records": 1 if root.exists() else 0,
        "source_ids_added": [COMMUNITY_SOURCE_ID] if root.exists() else [],
        "source_manifest_record": source_record,
        "raw_text_committed": False,
        "raw_images_committed": False,
        "raw_data_committed": False,
        "generated_outputs_committed": False,
        "solve_claim": False,
    }
    write_records(out, records, **summary)
    write_json(results_dir / STAGE5AK_REPORTS["inventory"], {**summary, "records": records})
    write_json(results_dir / STAGE5AK_REPORTS["message_index"], {"records": message_index, "raw_message_body_committed": False})
    return {**summary, "records": records}


def build_community_facts_source_cards(
    *,
    inventory_path: Path,
    attachment_index_path: Path,
    bundle_plan_path: Path = RESEARCH_BUNDLE_PLAN_PATH,
    out_source_card_summary: Path = STAGE5AK_SOURCE_CARD_SUMMARY_PATH,
    out_content_index_summary: Path = STAGE5AK_CONTENT_INDEX_SUMMARY_PATH,
    results_dir: Path = STAGE5AK_OUTPUT_DIR,
) -> dict[str, Any]:
    """Write community-facts source-card and content-index summaries."""

    del bundle_plan_path
    inventory = read_yaml(inventory_path)
    attachments = read_yaml(attachment_index_path)
    source_card = {
        "record_type": "stage5ak_community_facts_source_card",
        "schema": "schemas/source-harvester/community-facts-source-card-summary-v0.schema.json",
        "stage_id": STAGE5AK_ID,
        "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
        "source_id": COMMUNITY_SOURCE_ID,
        "title": "Community facts and number observations thread",
        "source_type": "local_user_upload",
        "priority": "A1",
        "source_tier": "tier4_social_claim_or_screenshot",
        "collection_status": "local_ready" if inventory.get("local_folder_exists") else "missing_local_folder",
        "local_path_hint": inventory.get("source_root"),
        "bundle_ids": [COMMUNITY_BUNDLE_ID, "05-red-markers-and-visual-numerics", "07-boundary-mobius-repeated-fragments"],
        "clue_categories": [
            "community_number_fact_thread",
            "no_fehu_section_count_graph",
            "p54_55_p56_p57_hash_length_equivalence",
            "p15_red_text_progressive_sum_square",
            "red_3299_fehu_count_prime_index",
            "whitespace_prime_sequence_claim",
            "count_policy_correction_log",
        ],
        "recommended_capture_modes": inventory.get("source_manifest_record", {}).get("recommended_capture_modes", []),
        "attachment_count": attachments.get("attachment_index_records", 0),
        "claim_record_layer_required": True,
        "raw_content_publication_allowed": False,
        "generated_extract_publication_allowed": False,
        "website_publication_allowed": False,
        "deep_research_private_allowed": True,
        "solve_claim": False,
    }
    content_records = [
        _content_record(source_card, "community_message_log_index", "private_metadata_extract"),
        _content_record(source_card, "ordered_attachment_index", "metadata_only"),
        _content_record(source_card, "community_claim_records", "metadata_only"),
        _content_record(source_card, "community_correction_log", "metadata_only"),
        _content_record(source_card, "arithmetic_preflight_metadata", "metadata_only"),
    ]
    source_summary = {
        "record_type": "stage5ak_community_facts_source_card_summary",
        "schema": "schemas/source-harvester/community-facts-source-card-summary-v0.schema.json",
        "stage_id": STAGE5AK_ID,
        "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
        "source_card_records": 1,
        "source_card_updates": 1,
        "local_source_card_records": 1,
        "publication_review_required_count": 1,
        "website_publication_allowed_count": 0,
        "private_deep_research_extract_ready_count": 1,
        "raw_content_publication_allowed": False,
        "generated_extract_publication_allowed": False,
        "solve_claim": False,
    }
    content_summary = {
        "record_type": "stage5ak_community_facts_content_index_summary",
        "schema": "schemas/source-harvester/community-facts-content-index-summary-v0.schema.json",
        "stage_id": STAGE5AK_ID,
        "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
        "content_index_records": len(content_records),
        "content_index_updates": len(content_records),
        "source_card_records": 1,
        "website_publication_allowed_count": 0,
        "private_deep_research_ready_count": len(content_records),
        "generated_extract_review_required_count": len(content_records),
        "raw_message_bodies_committed": False,
        "raw_image_bytes_committed": False,
        "generated_outputs_committed": False,
        "solve_claim": False,
    }
    write_records(out_source_card_summary, [source_card], **source_summary)
    write_records(out_content_index_summary, content_records, **content_summary)
    write_jsonl(results_dir / "source_card_index.jsonl", [source_card])
    write_jsonl(results_dir / "content_extract_index.jsonl", content_records)
    return {**source_summary, "content_index_records": len(content_records)}


def update_community_deep_research_packs(
    *,
    stage5aj_bundle_root: Path,
    source_card_summary_path: Path,
    content_index_summary_path: Path,
    claim_records_path: Path,
    correction_log_path: Path,
    bundle_root: Path = STAGE5AK_BUNDLE_ROOT,
    results_dir: Path = STAGE5AK_OUTPUT_DIR,
    out_website_update: Path = STAGE5AK_WEBSITE_UPDATE_PATH,
    out_deep_research_update: Path = STAGE5AK_DEEP_RESEARCH_UPDATE_PATH,
    out_readiness: Path = STAGE5AK_READINESS_PATH,
    out_missing_source_plan: Path = STAGE5AK_MISSING_SOURCE_PLAN_PATH,
) -> dict[str, Any]:
    """Create ignored Stage 5AK private bundle scaffolds and committed summaries."""

    cards = read_yaml(source_card_summary_path)
    content = read_yaml(content_index_summary_path)
    claims = read_yaml(claim_records_path)
    corrections = read_yaml(correction_log_path)
    bundle_target = resolve(bundle_root)
    bundle_target.mkdir(parents=True, exist_ok=True)
    (bundle_target / ".gitkeep").write_text("keep\n", encoding="utf-8")
    (bundle_target / "README.md").write_text(
        "# Stage 5AK community-facts Deep Research addendum\n\n"
        "Generated local body files for private Deep Research only. Do not commit raw message bodies, images, or generated extracts.\n",
        encoding="utf-8",
    )
    write_yaml(bundle_target / "master_manifest.yaml", _private_manifest(stage5aj_bundle_root, claims))
    write_jsonl(bundle_target / "source_cards.jsonl", read_yaml(source_card_summary_path).get("records", []))
    write_jsonl(bundle_target / "content_index.jsonl", read_yaml(content_index_summary_path).get("records", []))
    write_jsonl(bundle_target / "community_claim_records.jsonl", claims.get("records", []))
    write_jsonl(bundle_target / "correction_log.jsonl", corrections.get("records", []))
    (bundle_target / "do_not_assume_global.md").write_text(_global_do_not_assume(), encoding="utf-8")
    (bundle_target / "known_questions_global.md").write_text(_global_known_questions(), encoding="utf-8")
    (bundle_target / "deep_research_addendum_context.md").write_text(_global_context(), encoding="utf-8")
    for bundle_id in _community_bundle_ids():
        _write_bundle_addendum(bundle_target / bundle_id, bundle_id, claims.get("records", []))
    website = {
        "record_type": "stage5ak_website_ingest_update_summary",
        "schema": "schemas/source-harvester/community-facts-content-index-summary-v0.schema.json",
        "stage_id": STAGE5AK_ID,
        "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
        "website_ingest_updates": cards.get("source_card_records", 0) + content.get("content_index_records", 0),
        "website_ingest_metadata_ready": True,
        "public_website_ready_count": 0,
        "publication_status": "blocked_private_or_sensitive_until_review",
        "metadata_publication_allowed_after_review": True,
        "raw_message_bodies_publication_allowed": False,
        "raw_image_publication_allowed": False,
        "website_expansion_performed": False,
        "solve_claim": False,
    }
    deep = {
        "record_type": "stage5ak_deep_research_pack_update_summary",
        "schema": "schemas/source-harvester/deep-research-pack-update-summary-v0.schema.json",
        "stage_id": STAGE5AK_ID,
        "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
        "deep_research_pack_updates": 1,
        "deep_research_pack_records": 1,
        "community_facts_addendum_ready": True,
        "private_deep_research_ready": True,
        "raw_message_bodies_committed": False,
        "raw_image_bytes_committed": False,
        "deep_research_performed": False,
        "solve_claim": False,
    }
    readiness = {
        "record_type": "stage5ak_research_bundle_readiness",
        "schema": "schemas/source-harvester/deep-research-pack-update-summary-v0.schema.json",
        "stage_id": STAGE5AK_ID,
        "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
        "bundle_readiness_before": 10,
        "bundle_readiness_after": 10,
        "community_facts_addendum_ready": True,
        "private_deep_research_ready": True,
        "bundles_ready_for_private_deep_research": 10,
        "bundles_public_website_ready": 0,
        "public_website_ready": 0,
        "solve_claim": False,
    }
    missing = {
        "record_type": "stage5ak_missing_source_plan_update",
        "schema": "schemas/source-harvester/deep-research-pack-update-summary-v0.schema.json",
        "stage_id": STAGE5AK_ID,
        "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
        "missing_source_records": 1,
        "records": [
            {
                "source_id": COMMUNITY_SOURCE_ID,
                "status": "now_local",
                "no_network_fetch_required": True,
                "public_review_required": True,
                "allow_network_fetch": False,
                "solve_claim": False,
            }
        ],
        "network_fetch_performed": False,
        "online_repo_clone_performed": False,
        "google_drive_storage_used": False,
        "solve_claim": False,
    }
    write_yaml(out_website_update, website)
    write_yaml(out_deep_research_update, deep)
    write_yaml(out_readiness, readiness)
    write_yaml(out_missing_source_plan, missing)
    write_json(results_dir / STAGE5AK_REPORTS["website_update"], website)
    write_json(results_dir / STAGE5AK_REPORTS["deep_research_update"], deep)
    return {"website": website, "deep": deep, "readiness": readiness, "missing": missing}


def _message_index(path: Path) -> list[dict[str, Any]]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    records = []
    for index, line in enumerate(lines, start=1):
        records.append(
            {
                "message_locator": f"{path.name}:L{index}",
                "line_number": index,
                "line_sha256": hashlib.sha256(line.encode("utf-8")).hexdigest(),
                "body": line,
            }
        )
    return records


def _source_manifest_record(source_root: Path) -> dict[str, Any]:
    return {
        "source_id": COMMUNITY_SOURCE_ID,
        "title": "Community facts and number observations thread",
        "source_type": "local_user_upload",
        "priority": "A1",
        "source_tier": "tier4_social_claim_or_screenshot",
        "collection_status": "local_ready",
        "local_path_hint": source_root.as_posix(),
        "recommended_capture_modes": [
            "text_hash",
            "message_log_index",
            "attachment_image_metadata",
            "ordered_attachment_index",
            "community_claim_record_extraction",
            "correction_log",
            "arithmetic_preflight_metadata",
        ],
        "manual_collection_required": False,
        "allow_network_fetch": False,
        "allow_dynamic_browser": False,
        "raw_commit_allowed": False,
        "google_drive_storage_allowed": False,
        "what_it_supports": [
            "community_number_fact_thread",
            "no_fehu_section_count_graph",
            "p54_55_p56_p57_hash_length_equivalence",
            "p15_red_text_progressive_sum_square",
            "red_3299_fehu_count_prime_index",
            "p56_p57_fehu_boundary_prime_observations",
            "final_jpg_gp_runs_road_phrase",
            "artwork_red_header_gp_match",
            "pixel_measurement_prime_dimension_claims",
            "whitespace_prime_sequence_claim",
            "cicada_prime_index_number_network",
            "transcript_word_count_conflict",
            "count_policy_correction_log",
        ],
        "what_it_does_not_support": [
            "solve_claims",
            "execution_ready_status",
            "canonical_corpus_activation",
            "page_boundary_finalisation",
        ],
        "publication_status": "blocked_private_or_sensitive_until_review",
        "deep_research_private_allowed": True,
        "website_publication_allowed": False,
        "solve_claim": False,
        "notes": [
            "Discord/forum-derived observations; high false-positive risk.",
            "Source-lock and claim-catalogue material only.",
            "Attachments are ordered according to thread order, but message-to-image mapping is inferred unless explicit.",
        ],
    }


def _content_record(source_card: dict[str, Any], content_kind: str, extract_policy: str) -> dict[str, Any]:
    return {
        "record_type": "stage5ak_community_facts_content_index_record",
        "schema": "schemas/source-harvester/community-facts-content-index-summary-v0.schema.json",
        "stage_id": STAGE5AK_ID,
        "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
        "source_id": source_card["source_id"],
        "content_id": f"{source_card['source_id']}:{content_kind}",
        "content_kind": content_kind,
        "extract_policy": extract_policy,
        "private_deep_research_allowed": True,
        "website_publication_allowed": False,
        "raw_message_body_committed": False,
        "raw_image_bytes_committed": False,
        "solve_claim": False,
    }


def _private_manifest(stage5aj_bundle_root: Path, claims: dict[str, Any]) -> dict[str, Any]:
    return {
        "record_type": "stage5ak_private_deep_research_manifest",
        "stage_id": STAGE5AK_ID,
        "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
        "inherits_stage5aj_bundle_root": stage5aj_bundle_root.as_posix(),
        "community_claim_records": claims.get("claim_record_count", 0),
        "private_deep_research_allowed": True,
        "website_publication_allowed": False,
        "raw_message_bodies_committed": False,
        "raw_image_bytes_committed": False,
        "solve_claim": False,
    }


def _community_bundle_ids() -> list[str]:
    return [
        "05-red-markers-and-visual-numerics",
        "07-boundary-mobius-repeated-fragments",
        "08-tools-gpprime-dwh-gematria",
        "09-community-hypotheses",
        "10-known-negative-retired-ideas",
    ]


def _write_bundle_addendum(bundle_dir: Path, bundle_id: str, claims: list[dict[str, Any]]) -> None:
    bundle_dir.mkdir(parents=True, exist_ok=True)
    relevant = [record for record in claims if bundle_id in _bundle_ids_for_claim(record.get("claim_family", ""))]
    (bundle_dir / "README.md").write_text(
        f"# {bundle_id} community-facts addendum\n\n"
        "Generated local Deep Research context. Treat all claims as unverified metadata unless later source-locked and reviewed.\n",
        encoding="utf-8",
    )
    write_yaml(
        bundle_dir / "manifest.yaml",
        {
            "record_type": "stage5ak_bundle_specific_deep_research_manifest",
            "stage_id": STAGE5AK_ID,
            "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
            "bundle_id": bundle_id,
            "community_claim_records": len(relevant),
            "raw_message_bodies_committed": False,
            "raw_image_bytes_committed": False,
            "website_publication_allowed": False,
            "solve_claim": False,
        },
    )
    write_jsonl(bundle_dir / "source_cards.jsonl", [])
    write_jsonl(bundle_dir / "content_index.jsonl", [])
    write_jsonl(bundle_dir / "community_claim_records.jsonl", relevant)
    (bundle_dir / "known_questions.md").write_text(_bundle_questions(bundle_id), encoding="utf-8")
    (bundle_dir / "do_not_assume.md").write_text(_global_do_not_assume(), encoding="utf-8")
    (bundle_dir / "deep_research_context.md").write_text(_global_context(), encoding="utf-8")


def _bundle_ids_for_claim(claim_family: str) -> list[str]:
    mapping = {
        "p15_red_text_progressive_sum_square": ["05-red-markers-and-visual-numerics", "09-community-hypotheses"],
        "red_3299_fehu_count_prime_index": ["05-red-markers-and-visual-numerics", "09-community-hypotheses"],
        "artwork_red_header_gp_match": ["05-red-markers-and-visual-numerics", "09-community-hypotheses"],
        "p54_55_p56_p57_hash_length_equivalence": ["07-boundary-mobius-repeated-fragments", "09-community-hypotheses"],
        "p56_p57_fehu_boundary_prime_observations": ["07-boundary-mobius-repeated-fragments", "09-community-hypotheses"],
        "cicada_prime_index_number_network": ["08-tools-gpprime-dwh-gematria", "09-community-hypotheses"],
        "base60_emirp_index_observations": ["08-tools-gpprime-dwh-gematria", "09-community-hypotheses"],
        "doublet_route_index_observations": ["08-tools-gpprime-dwh-gematria", "09-community-hypotheses"],
        "no_fehu_section_count_graph": ["10-known-negative-retired-ideas", "09-community-hypotheses"],
        "pixel_measurement_prime_dimension_claims": ["10-known-negative-retired-ideas", "09-community-hypotheses"],
        "whitespace_prime_sequence_claim": ["10-known-negative-retired-ideas", "09-community-hypotheses"],
        "final_jpg_gp_runs_road_phrase": ["10-known-negative-retired-ideas", "09-community-hypotheses"],
    }
    return mapping.get(claim_family, ["09-community-hypotheses"])


def _global_do_not_assume() -> str:
    return (
        "# Do not assume\n\n"
        "- Community-facts claims are not truth records.\n"
        "- Arithmetic preflight is not transcript, image, or intention evidence.\n"
        "- Claim records are not execution permission.\n"
        "- Raw message bodies and images are not public website material.\n"
        "- No OCR, image forensics, hypothesis execution, CUDA, or benchmarks were run in Stage 5AK.\n"
    )


def _global_known_questions() -> str:
    return (
        "# Known questions\n\n"
        "- Which claims have exact transcript/profile sources?\n"
        "- Which image references have source-locked originals and declared coordinate policies?\n"
        "- Which arithmetic facts survive null controls and multiple-testing controls?\n"
        "- Which correction-log entries supersede older community counts?\n"
    )


def _global_context() -> str:
    return (
        "# Stage 5AK Deep Research addendum context\n\n"
        "The community-facts folder is a local Discord/forum-derived observation collection. Stage 5AK records "
        "source-card metadata, ordered attachment metadata, claim families, correction records, and explicit arithmetic "
        "preflight checks only. It does not test hypotheses or make solve claims.\n"
    )


def _bundle_questions(bundle_id: str) -> str:
    return (
        f"# Known questions for {bundle_id}\n\n"
        "- Which source locks are needed before this claim family can be reviewed?\n"
        "- Which null controls are required before any future bounded verifier?\n"
        "- Which claims should remain only negative-control or false-positive audit material?\n"
    )
