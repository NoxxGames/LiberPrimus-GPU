"""Stage 5AI readiness, guardrail, next-stage, and summary records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_records, read_yaml, write_json, write_jsonl, write_records, write_yaml
from .local_inventory import _staged_raw_files_present, _tracked_raw_files_present
from .models import (
    STAGE5AI_BUNDLE_ROOT,
    STAGE5AI_FALSE_FLAGS,
    STAGE5AI_GUARDRAIL_PATH,
    STAGE5AI_ID,
    STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
    STAGE5AI_NEXT_STAGE_DECISION_PATH,
    STAGE5AI_OUTPUT_DIR,
    STAGE5AI_READINESS_PATH,
    STAGE5AI_REPORTS,
    STAGE5AI_SOURCE_STAGE_ID,
    STAGE5AI_SUMMARY_PATH,
)


def build_stage5ai_guardrail(
    *,
    bundle_root: Path = STAGE5AI_BUNDLE_ROOT,
    results_dir: Path = STAGE5AI_OUTPUT_DIR,
    out: Path = STAGE5AI_GUARDRAIL_PATH,
) -> dict[str, Any]:
    """Write Stage 5AI guardrail record."""

    guardrail = {
        "record_type": "stage5ai_curated_extraction_guardrail",
        "schema": "schemas/source-harvester/stage5ai-curated-research-bundle-summary-v0.schema.json",
        "stage_id": STAGE5AI_ID,
        "source_stage_id": STAGE5AI_SOURCE_STAGE_ID,
        "local_source_inventory_stage": STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
        **STAGE5AI_FALSE_FLAGS,
        "third_party_raw_staged": _staged_raw_files_present(Path("third_party")),
        "third_party_raw_tracked_new": _tracked_raw_files_present(Path("third_party")),
        "generated_research_input_root": bundle_root.as_posix(),
        "generated_bundle_bodies_ignored": True,
        "new_cuda_kernels_added": 0,
        "no_solve_claim": True,
        "no_gpu_ci_safe": True,
        "ci_network_required": False,
    }
    write_yaml(out, guardrail)
    write_json(results_dir / "guardrail.json", guardrail)
    return guardrail


def build_stage5ai_readiness(
    *,
    bundle_root: Path = STAGE5AI_BUNDLE_ROOT,
    stage5ag_readiness_path: Path,
    out: Path = STAGE5AI_READINESS_PATH,
) -> dict[str, Any]:
    """Upgrade Stage 5AG bundle readiness based on generated private bundle skeletons."""

    stage5ag = {record["bundle_id"]: record for record in read_records(stage5ag_readiness_path)}
    records = []
    for bundle_dir in sorted(path for path in bundle_root.iterdir() if path.is_dir()):
        bundle_id = bundle_dir.name
        content_count = _jsonl_count(bundle_dir / "content_index.jsonl")
        status = _readiness_status(stage5ag.get(bundle_id, {}), content_count)
        records.append(
            {
                "record_type": "stage5ai_research_bundle_readiness_record",
                "schema": "schemas/source-harvester/stage5ai-curated-research-bundle-summary-v0.schema.json",
                "stage_id": STAGE5AI_ID,
                "source_stage_id": STAGE5AI_SOURCE_STAGE_ID,
                "local_inventory_stage_id": STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
                "bundle_id": bundle_id,
                "generated_skeleton": (bundle_dir / "manifest.yaml").exists(),
                "content_index_records": content_count,
                "readiness_status": status,
                "ready_for_private_deep_research": "ready_for_private_deep_research" in status,
                "public_website_ready": False,
                "missing_source_ids": stage5ag.get(bundle_id, {}).get("missing_source_ids", []),
                "solve_claim": False,
            }
        )
    summary = {
        "record_type": "stage5ai_research_bundle_readiness",
        "schema": "schemas/source-harvester/stage5ai-curated-research-bundle-summary-v0.schema.json",
        "stage_id": STAGE5AI_ID,
        "source_stage_id": STAGE5AI_SOURCE_STAGE_ID,
        "local_inventory_stage_id": STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
        "curated_bundle_records": len(records),
        "bundles_with_generated_skeleton": sum(1 for record in records if record["generated_skeleton"]),
        "bundles_with_extracted_local_content": sum(1 for record in records if record["content_index_records"] > 0),
        "bundles_ready_for_private_deep_research": sum(1 for record in records if record["ready_for_private_deep_research"]),
        "bundles_public_website_ready": 0,
        "website_ingest_metadata_ready": True,
        "solve_claim": False,
    }
    write_records(out, records, **summary)
    return {**summary, "records": records}


def build_stage5ai_next_stage_decision(
    *,
    readiness_path: Path,
    missing_source_plan_path: Path,
    out: Path = STAGE5AI_NEXT_STAGE_DECISION_PATH,
) -> dict[str, Any]:
    """Select the next stage after Stage 5AI."""

    readiness = read_yaml(readiness_path)
    missing = read_yaml(missing_source_plan_path)
    selected_id = _select_next(readiness, missing)
    records = []
    for option_id, title, reason in _decision_options():
        selected = option_id == selected_id
        records.append(
            {
                "record_type": "stage5ai_next_stage_decision_record",
                "schema": "schemas/source-harvester/stage5ai-curated-research-bundle-summary-v0.schema.json",
                "stage_id": STAGE5AI_ID,
                "source_stage_id": STAGE5AI_SOURCE_STAGE_ID,
                "option_id": option_id,
                "selected": selected,
                "recommended_next_prompt_type": "Deep Research" if selected_id.startswith("stage5aj_deep_research") and selected else ("Codex" if selected else None),
                "recommended_next_stage_title": title,
                "recommended_next_stage_reason": reason,
                "deep_research_recommended_next": selected and selected_id.startswith("stage5aj_deep_research"),
                "scored_experiment_recommended_next": False,
                "benchmark_recommended_next": False,
                "unsolved_page_cuda_recommended_next": False,
                "website_expansion_recommended_next": False,
                "execution_enabled": False,
                "solve_claim": False,
            }
        )
    write_records(
        out,
        records,
        record_type="stage5ai_next_stage_decisions",
        schema="schemas/source-harvester/stage5ai-curated-research-bundle-summary-v0.schema.json",
        stage_id=STAGE5AI_ID,
        source_stage_id=STAGE5AI_SOURCE_STAGE_ID,
        selected_option_id=selected_id,
        solve_claim=False,
    )
    return {"records": records, "selected_option_id": selected_id}


def build_stage5ai_summary(
    *,
    policy_path: Path,
    source_card_summary_path: Path,
    content_index_summary_path: Path,
    website_ingest_format_path: Path,
    deep_research_pack_format_path: Path,
    bundle_generation_summary_path: Path,
    classification_path: Path,
    missing_source_plan_path: Path,
    readiness_path: Path,
    guardrail_path: Path,
    next_stage_decision_path: Path,
    out: Path = STAGE5AI_SUMMARY_PATH,
    results_dir: Path = STAGE5AI_OUTPUT_DIR,
    bundle_root: Path = STAGE5AI_BUNDLE_ROOT,
) -> dict[str, Any]:
    """Build the committed Stage 5AI aggregate summary."""

    del policy_path
    cards = read_yaml(source_card_summary_path)
    content = read_yaml(content_index_summary_path)
    website = read_yaml(website_ingest_format_path)
    deep_research = read_yaml(deep_research_pack_format_path)
    bundles = read_yaml(bundle_generation_summary_path)
    classification = read_yaml(classification_path)
    missing = read_yaml(missing_source_plan_path)
    readiness = read_yaml(readiness_path)
    guardrail = read_yaml(guardrail_path)
    selected = [record for record in read_records(next_stage_decision_path) if record.get("selected") is True][0]
    summary = {
        "record_type": "stage5ai_curated_research_bundle_summary",
        "schema": "schemas/source-harvester/stage5ai-curated-research-bundle-summary-v0.schema.json",
        "stage_id": STAGE5AI_ID,
        "status": "complete",
        "source_stage_id": STAGE5AI_SOURCE_STAGE_ID,
        "local_inventory_stage_id": STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
        "source_root": "third_party",
        "bundle_root": bundle_root.as_posix(),
        "results_dir": results_dir.as_posix(),
        "curated_bundle_records": bundles.get("curated_bundle_records", 0),
        "source_card_records": cards.get("source_card_records", 0),
        "content_index_records": content.get("content_index_records", 0),
        "website_ingest_source_card_records": website.get("website_ingest_source_card_records", 0),
        "website_ingest_content_records": website.get("website_ingest_content_records", 0),
        "deep_research_pack_records": deep_research.get("deep_research_pack_records", 0),
        "missing_source_records": missing.get("missing_source_records", 0),
        "unclassified_source_classification_records": classification.get("classification_records", 0),
        "bundles_with_generated_skeleton": readiness.get("bundles_with_generated_skeleton", 0),
        "bundles_with_extracted_local_content": readiness.get("bundles_with_extracted_local_content", 0),
        "bundles_ready_for_private_deep_research": readiness.get("bundles_ready_for_private_deep_research", 0),
        "bundles_public_website_ready": 0,
        "bundles_requiring_publication_review": content.get("generated_extract_review_required_count", 0),
        "bundles_blocked_private_or_sensitive": content.get("blocked_private_or_sensitive_count", 0),
        "website_ingest_metadata_ready": website.get("website_ingest_metadata_ready", False),
        "website_expansion_performed": False,
        "deep_research_recommended_next": selected.get("deep_research_recommended_next", False),
        "recommended_next_prompt_type": selected.get("recommended_next_prompt_type"),
        "recommended_next_stage_title": selected.get("recommended_next_stage_title"),
        "recommended_next_stage_reason": selected.get("recommended_next_stage_reason"),
        **{key: guardrail.get(key, False) for key in STAGE5AI_FALSE_FLAGS},
        "new_cuda_kernels_added": 0,
        "no_solve_claim": True,
        "no_gpu_ci_safe": True,
        "ci_network_required": False,
    }
    write_yaml(out, summary)
    write_json(results_dir / STAGE5AI_REPORTS["summary"], summary)
    write_jsonl(results_dir / STAGE5AI_REPORTS["warnings"], [])
    return summary


def _jsonl_count(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def _readiness_status(stage5ag_record: dict[str, Any], content_count: int) -> str:
    if content_count <= 0:
        return "skeleton_only" if stage5ag_record else "not_ready_missing_sources"
    if stage5ag_record.get("missing_source_ids"):
        return "partial_curated_extract_ready_for_private_deep_research"
    return "curated_extract_ready_for_private_deep_research"


def _select_next(readiness: dict[str, Any], missing: dict[str, Any]) -> str:
    if readiness.get("bundles_ready_for_private_deep_research", 0) > 0:
        return "stage5aj_deep_research_source_inventory_and_reliability_prompt"
    if missing.get("missing_a1_a2_count", 0) > 0:
        return "stage5aj_source_gap_closure_for_missing_priority_sources"
    return "stage5aj_visual_page_image_provenance_inventory"


def _decision_options() -> list[tuple[str, str, str]]:
    return [
        (
            "stage5aj_deep_research_source_inventory_and_reliability_prompt",
            "Stage 5AJ - Deep Research source inventory and reliability prompt",
            "At least one curated private bundle exists; Deep Research should consume Stage 5AI bundle manifests, not raw third_party paths.",
        ),
        (
            "stage5aj_source_gap_closure_for_missing_priority_sources",
            "Stage 5AJ - source gap closure for missing priority sources",
            "Use if no curated bundle is ready and missing A1/A2 sources dominate.",
        ),
        (
            "stage5aj_online_fetch_for_missing_manifest_sources",
            "Stage 5AJ - online fetch for missing manifest sources",
            "Deferred; online fetch requires explicit future scope.",
        ),
        (
            "stage5aj_visual_page_image_provenance_inventory",
            "Stage 5AJ - visual page-image provenance inventory",
            "Use if image-heavy material is curated but not ready for text-oriented Deep Research.",
        ),
        (
            "stage5aj_cicada_archive_source_lock_initial_ingestion",
            "Stage 5AJ - Cicada archive source-lock initial ingestion",
            "Deferred until a future source-lock stage scopes exact archive records.",
        ),
        (
            "stage5aj_page49_51_token_block_extraction",
            "Stage 5AJ - page 49-51 token block extraction",
            "Deferred until exact transcript/profile source gaps close.",
        ),
        (
            "stage5aj_cuneiform_red_marker_visual_numeric_extraction",
            "Stage 5AJ - cuneiform/red-marker visual numeric extraction",
            "Deferred; visual claims remain review-gated.",
        ),
        (
            "stage5aj_discord_private_lead_redaction_plan",
            "Stage 5AJ - Discord private lead redaction plan",
            "Deferred; private/social material requires redaction planning before public use.",
        ),
        (
            "stage5aj_bounded_cpu_native_scored_experiment_manifest_gate",
            "Stage 5AJ - bounded CPU/native scored experiment manifest gate",
            "Rejected because Stage 5AI is curation only.",
        ),
        ("stage5aj_benchmark_planning", "Stage 5AJ - benchmark planning", "Rejected; benchmarks remain out of scope."),
        ("stage5aj_unsolved_page_cuda_pilot", "Stage 5AJ - unsolved-page CUDA pilot", "Rejected; unsolved-page CUDA remains blocked."),
        ("future_website_expansion_unnumbered", "Future unnumbered website expansion", "Deferred; Stage 5AI only prepares website-ingest metadata."),
    ]
