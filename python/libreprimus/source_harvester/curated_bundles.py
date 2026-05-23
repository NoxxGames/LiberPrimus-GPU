"""Stage 5AI curated research bundle skeleton generation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .export import read_records, write_json, write_jsonl, write_records, write_yaml
from .models import (
    STAGE5AI_BUNDLE_GENERATION_SUMMARY_PATH,
    STAGE5AI_BUNDLE_ROOT,
    STAGE5AI_ID,
    STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
    STAGE5AI_OUTPUT_DIR,
    STAGE5AI_POLICY_PATH,
    STAGE5AI_REPORTS,
    STAGE5AI_SOURCE_STAGE_ID,
)


def build_curated_bundles(
    *,
    local_linkage_path: Path,
    bundle_readiness_path: Path,
    bundle_plan_path: Path,
    classification_path: Path,
    source_root: Path,
    bundle_root: Path = STAGE5AI_BUNDLE_ROOT,
    results_dir: Path = STAGE5AI_OUTPUT_DIR,
    out_policy: Path = STAGE5AI_POLICY_PATH,
    out_summary: Path = STAGE5AI_BUNDLE_GENERATION_SUMMARY_PATH,
) -> dict[str, Any]:
    """Generate ignored curated bundle skeletons and compact committed summaries."""

    del local_linkage_path, classification_path, source_root
    bundle_root.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)
    source_cards = _read_jsonl(bundle_root / "source_cards.jsonl")
    bundle_plan = read_records(bundle_plan_path)
    readiness = {record["bundle_id"]: record for record in read_records(bundle_readiness_path)}
    content_records: list[dict[str, Any]] = []
    bundle_records = []
    for bundle in sorted(bundle_plan, key=lambda item: item.get("recommended_deep_research_order", 999)):
        bundle_id = bundle["bundle_id"]
        bundle_dir = bundle_root / bundle_id
        _create_bundle_dirs(bundle_dir)
        cards = [card for card in source_cards if bundle_id in card.get("bundle_ids", [])]
        local_content_count = 0
        bundle_content_records = []
        for card in cards:
            record = _content_record(bundle_id, card)
            bundle_content_records.append(record)
            content_records.append(record)
            local_content_count += 1
            _write_generated_metadata(bundle_dir, card, record)
        write_jsonl(bundle_dir / "source_cards.jsonl", cards)
        write_jsonl(bundle_dir / "content_index.jsonl", bundle_content_records)
        write_jsonl(bundle_dir / "attachment_index.jsonl", [])
        write_yaml(
            bundle_dir / "manifest.yaml",
            {
                "bundle_id": bundle_id,
                "title": bundle["title"],
                "stage_id": STAGE5AI_ID,
                "source_stage_id": STAGE5AI_SOURCE_STAGE_ID,
                "local_inventory_stage_id": STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
                "readiness_status": _bundle_status(readiness.get(bundle_id, {}), local_content_count),
                "matched_source_ids": readiness.get(bundle_id, {}).get("matched_source_ids", []),
                "missing_source_ids": readiness.get(bundle_id, {}).get("missing_source_ids", []),
                "source_card_count": len(cards),
                "content_record_count": len(bundle_content_records),
                "website_expansion_performed": False,
                "solve_claim": False,
            },
        )
        _write_bundle_markdown(bundle_dir, bundle)
        write_json(
            bundle_dir / "website_card.json",
            {
                "bundle_id": bundle_id,
                "title": bundle["title"],
                "publication_status": "generated_extract_review_required" if cards else "metadata_only",
                "website_publication_allowed": False,
                "source_card_count": len(cards),
                "content_record_count": len(bundle_content_records),
                "solve_claim": False,
            },
        )
        bundle_records.append(
            {
                "bundle_id": bundle_id,
                "title": bundle["title"],
                "sequential_order": bundle.get("recommended_deep_research_order"),
                "readiness_status": _bundle_status(readiness.get(bundle_id, {}), local_content_count),
                "source_card_count": len(cards),
                "content_record_count": len(bundle_content_records),
                "missing_source_ids": readiness.get(bundle_id, {}).get("missing_source_ids", []),
                "generated_skeleton": True,
                "extracted_local_content": local_content_count > 0,
                "public_website_ready": False,
                "solve_claim": False,
            }
        )
    _write_root_files(bundle_root, bundle_records, content_records)
    policy = _policy_record()
    write_yaml(out_policy, policy)
    summary = {
        "record_type": "stage5ai_bundle_generation_summary",
        "schema": "schemas/source-harvester/stage5ai-curated-research-bundle-summary-v0.schema.json",
        "stage_id": STAGE5AI_ID,
        "source_stage_id": STAGE5AI_SOURCE_STAGE_ID,
        "local_inventory_stage_id": STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
        "bundle_root": bundle_root.as_posix(),
        "curated_bundle_records": len(bundle_records),
        "bundles_with_generated_skeleton": sum(1 for record in bundle_records if record["generated_skeleton"]),
        "bundles_with_extracted_local_content": sum(1 for record in bundle_records if record["extracted_local_content"]),
        "bundles_public_website_ready": 0,
        "content_index_records": len(content_records),
        "generated_bundle_bodies_committed": False,
        "website_expansion_performed": False,
        "solve_claim": False,
        "records": bundle_records,
    }
    write_records(out_summary, bundle_records, **{key: value for key, value in summary.items() if key != "records"})
    write_json(results_dir / STAGE5AI_REPORTS["bundle_generation"], summary)
    write_jsonl(results_dir / STAGE5AI_REPORTS["content_index"], content_records)
    return summary


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _create_bundle_dirs(bundle_dir: Path) -> None:
    for relative in ("extracted_text", "tables", "image_metadata"):
        (bundle_dir / relative).mkdir(parents=True, exist_ok=True)


def _content_record(bundle_id: str, card: dict[str, Any]) -> dict[str, Any]:
    source_id = card["source_id"]
    content_types = list(card.get("content_types", []))
    primary_type = content_types[0] if content_types else "metadata"
    if primary_type == "image":
        relative = f"{bundle_id}/image_metadata/{source_id}.json"
    else:
        relative = f"{bundle_id}/extracted_text/{source_id}-metadata.md"
    return {
        "content_id": f"{bundle_id}::{source_id}",
        "bundle_id": bundle_id,
        "source_id": source_id,
        "content_kind": "metadata_only" if primary_type in {"image", "audio", "video", "document", "archive", "directory"} else "text_or_metadata_extract",
        "title": card["title"],
        "relative_generated_path": relative,
        "source_hash": None,
        "extract_hash": None,
        "text_length": 0,
        "table_count": 0,
        "image_metadata_count": 1 if primary_type == "image" else 0,
        "attachment_count": len(card.get("local_source_paths_redacted_or_relative", [])),
        "license_or_rights_note": "Stage 5AI metadata only; publication requires later review.",
        "publication_status": card.get("publication_status", "generated_extract_review_required"),
        "review_status": "review_required",
        "sensitive_or_private": card.get("publication_status") == "blocked_private_or_sensitive",
        "redaction_required": bool(card.get("redaction_required", False)),
        "do_not_assume_tags": ["metadata_is_not_evidence", "no_solve_claim"],
        "clue_category_tags": card.get("clue_categories", []),
        "website_publication_allowed": False,
        "solve_claim": False,
    }


def _write_generated_metadata(bundle_dir: Path, card: dict[str, Any], content_record: dict[str, Any]) -> None:
    target = bundle_dir.parent / content_record["relative_generated_path"]
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.suffix == ".json":
        write_json(
            target,
            {
                "source_id": card["source_id"],
                "title": card["title"],
                "paths": card.get("local_source_paths_redacted_or_relative", []),
                "metadata_only": True,
                "ocr_performed": False,
                "image_forensics_performed": False,
                "solve_claim": False,
            },
        )
        return
    text = "\n".join(
        [
            f"# {card['title']}",
            "",
            "Stage 5AI generated metadata extract. This is not raw source publication.",
            "",
            f"- source_id: `{card['source_id']}`",
            f"- publication_status: `{card.get('publication_status')}`",
            "- raw_content_publication_allowed: `false`",
            "- solve_claim: `false`",
            "",
        ]
    )
    target.write_text(text, encoding="utf-8")


def _write_bundle_markdown(bundle_dir: Path, bundle: dict[str, Any]) -> None:
    do_not_assume = "\n".join(f"- {note}" for note in bundle.get("do_not_assume_notes", []))
    questions = "\n".join(f"- What source-lock or review step is still missing for `{source}`?" for source in bundle.get("included_source_ids", []))
    (bundle_dir / "README.md").write_text(f"# {bundle['title']}\n\nGenerated Stage 5AI private research-input bundle skeleton.\n", encoding="utf-8")
    (bundle_dir / "do_not_assume.md").write_text(f"# Do Not Assume\n\n{do_not_assume}\n- Do not treat this bundle as a solve claim.\n", encoding="utf-8")
    (bundle_dir / "known_questions.md").write_text(f"# Known Questions\n\n{questions}\n", encoding="utf-8")
    (bundle_dir / "deep_research_context.md").write_text(
        f"# Deep Research Context\n\nBundle `{bundle['bundle_id']}` should be reviewed in order {bundle.get('recommended_deep_research_order')} using generated metadata, not raw `third_party` paths directly.\n",
        encoding="utf-8",
    )


def _write_root_files(bundle_root: Path, bundle_records: list[dict[str, Any]], content_records: list[dict[str, Any]]) -> None:
    write_yaml(
        bundle_root / "master_manifest.yaml",
        {
            "stage_id": STAGE5AI_ID,
            "bundle_count": len(bundle_records),
            "content_record_count": len(content_records),
            "website_expansion_performed": False,
            "solve_claim": False,
            "bundles": bundle_records,
        },
    )
    write_jsonl(bundle_root / "content_index.jsonl", content_records)
    write_jsonl(bundle_root / "missing_sources.jsonl", [])
    (bundle_root / "README.md").write_text("# Stage 5AI Research Inputs\n\nGenerated and ignored curated bundle bodies.\n", encoding="utf-8")
    (bundle_root / "do_not_assume_global.md").write_text("# Global Do Not Assume\n\n- Do not treat curated metadata as evidence or a solve claim.\n", encoding="utf-8")
    (bundle_root / "known_questions_global.md").write_text("# Global Known Questions\n\n- Which missing A1/A2 sources should be closed first?\n", encoding="utf-8")
    write_jsonl(bundle_root / "extraction_warnings.jsonl", [])


def _bundle_status(readiness_record: dict[str, Any], local_content_count: int) -> str:
    if local_content_count <= 0:
        return "skeleton_only" if readiness_record.get("missing_source_ids") else "not_ready_missing_sources"
    if readiness_record.get("missing_source_ids"):
        return "partial_curated_extract_ready_for_private_deep_research"
    return "curated_extract_ready_for_private_deep_research"


def _policy_record() -> dict[str, Any]:
    return {
        "record_type": "stage5ai_curated_bundle_extraction_policy",
        "schema": "schemas/source-harvester/curated-bundle-extraction-policy-v0.schema.json",
        "stage_id": STAGE5AI_ID,
        "source_stage_id": STAGE5AI_SOURCE_STAGE_ID,
        "local_inventory_stage_id": STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
        "raw_content_commit_allowed": False,
        "generated_extract_commit_allowed": False,
        "private_or_sensitive_publication_allowed": False,
        "ocr_allowed": False,
        "ai_ml_interpretation_allowed": False,
        "stego_tool_execution_allowed": False,
        "audio_transcription_allowed": False,
        "image_transform_allowed": False,
        "hash_preimage_search_allowed": False,
        "hypothesis_execution_allowed": False,
        "website_expansion_performed": False,
        "solve_claim": False,
    }
