"""Stage 5AG guardrail, next-stage decision, and summary builders."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_records, read_yaml, write_json, write_records, write_yaml
from .local_inventory import _raw_content_under_root_is_ignored, _staged_raw_files_present, _tracked_raw_files_present
from .models import (
    STAGE5AG_GUARDRAIL_PATH,
    STAGE5AG_ID,
    STAGE5AG_NEXT_STAGE_DECISION_PATH,
    STAGE5AG_OUTPUT_DIR,
    STAGE5AG_SOURCE_STAGE_ID,
    STAGE5AG_SUMMARY_PATH,
    STAGE5AG_FALSE_FLAGS,
    SUMMARY_REPORT,
    WARNINGS_REPORT,
)


def build_stage5ag_guardrail(
    *,
    source_root: Path,
    results_dir: Path = STAGE5AG_OUTPUT_DIR,
    out: Path = STAGE5AG_GUARDRAIL_PATH,
) -> dict[str, Any]:
    """Write Stage 5AG local-only guardrail record."""

    source_root_path = Path(source_root)
    guardrail = {
        "record_type": "stage5ag_local_source_guardrail",
        "schema": "schemas/source-harvester/local-source-guardrail-record-v0.schema.json",
        "stage_id": STAGE5AG_ID,
        "source_stage_id": STAGE5AG_SOURCE_STAGE_ID,
        **STAGE5AG_FALSE_FLAGS,
        "third_party_raw_staged": _staged_raw_files_present(source_root_path),
        "third_party_raw_tracked_new": _tracked_raw_files_present(source_root_path),
        "source_root_raw_content_ignored": _raw_content_under_root_is_ignored(source_root_path),
        "new_cuda_kernels_added": 0,
        "no_solve_claim": True,
        "no_gpu_ci_safe": True,
        "ci_network_required": False,
    }
    write_yaml(out, guardrail)
    write_json(results_dir / "guardrail.json", guardrail)
    return guardrail


def build_stage5ag_next_stage_decision(
    *,
    root_inventory_path: Path,
    local_linkage_path: Path,
    bundle_readiness_path: Path,
    out: Path = STAGE5AG_NEXT_STAGE_DECISION_PATH,
) -> dict[str, Any]:
    """Select the next bounded source-lock stage."""

    root = read_yaml(root_inventory_path)
    linkage = read_yaml(local_linkage_path)
    bundles = read_yaml(bundle_readiness_path)
    selected_id = _select_next(root, linkage, bundles)
    records = []
    for option_id, title, reason in _options():
        selected = option_id == selected_id
        records.append(
            {
                "record_type": "stage5ag_source_harvester_next_stage_decision",
                "schema": "schemas/source-harvester/stage5ag-source-harvester-next-stage-decision-record-v0.schema.json",
                "stage_id": STAGE5AG_ID,
                "source_stage_id": STAGE5AG_SOURCE_STAGE_ID,
                "option_id": option_id,
                "selected": selected,
                "recommended_next_prompt_type": "Codex" if selected else None,
                "recommended_next_stage_title": title,
                "recommended_next_stage_reason": reason,
                "deep_research_recommended_next": False,
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
        record_type="stage5ag_source_harvester_next_stage_decisions",
        schema="schemas/source-harvester/stage5ag-source-harvester-next-stage-decision-record-v0.schema.json",
        stage_id=STAGE5AG_ID,
        source_stage_id=STAGE5AG_SOURCE_STAGE_ID,
    )
    return {"records": records, "selected_option_id": selected_id}


def build_stage5ag_summary(
    *,
    root_inventory_path: Path,
    file_summary_path: Path,
    archive_summary_path: Path,
    hash_summary_path: Path,
    local_linkage_path: Path,
    candidate_summary_path: Path,
    gap_report_path: Path,
    bundle_readiness_path: Path,
    guardrail_path: Path,
    next_stage_decision_path: Path,
    out: Path = STAGE5AG_SUMMARY_PATH,
    results_dir: Path = STAGE5AG_OUTPUT_DIR,
) -> dict[str, Any]:
    """Build the committed Stage 5AG aggregate summary."""

    root = read_yaml(root_inventory_path)
    file_summary = read_yaml(file_summary_path)
    archive_summary = read_yaml(archive_summary_path)
    hash_summary = read_yaml(hash_summary_path)
    linkage = read_yaml(local_linkage_path)
    candidates = read_yaml(candidate_summary_path)
    bundles = read_yaml(bundle_readiness_path)
    guardrail = read_yaml(guardrail_path)
    selected = [record for record in read_records(next_stage_decision_path) if record.get("selected") is True][0]
    summary = {
        "record_type": "stage5ag_source_harvester_summary",
        "schema": "schemas/source-harvester/stage5ag-source-harvester-summary-v0.schema.json",
        "stage_id": STAGE5AG_ID,
        "status": "complete",
        "source_stage_id": STAGE5AG_SOURCE_STAGE_ID,
        "source_root": root.get("source_root", "third_party"),
        "source_root_exists": root.get("root_exists", False),
        "source_root_ignored": root.get("root_is_ignored", False),
        "total_local_files": root.get("total_files", 0),
        "total_local_dirs": root.get("total_dirs", 0),
        "total_local_size_bytes": root.get("total_size_bytes", 0),
        "archive_file_count": archive_summary.get("archive_record_count", 0),
        "supported_archive_count": archive_summary.get("supported_archive_count", 0),
        "unsupported_archive_count": archive_summary.get("unsupported_archive_count", 0),
        "image_file_count": root.get("image_counts", 0),
        "pdf_file_count": root.get("pdf_counts", 0),
        "docx_file_count": root.get("docx_counts", 0),
        "text_file_count": root.get("text_counts", 0),
        "html_file_count": root.get("html_counts", 0),
        "audio_file_count": root.get("audio_counts", 0),
        "video_file_count": root.get("video_counts", 0),
        "hashed_file_count": hash_summary.get("total_hashed_files", 0),
        "unique_hash_count": hash_summary.get("unique_hash_count", 0),
        "duplicate_hash_group_count": hash_summary.get("duplicate_hash_groups", 0),
        "manifest_records_consumed": linkage.get("manifest_records_consumed", 0),
        "manifest_records_matched": linkage.get("matched_count", 0),
        "manifest_records_missing": linkage.get("missing_count", 0),
        "manifest_records_ambiguous": linkage.get("ambiguous_count", 0),
        "local_unclassified_source_count": linkage.get("unclassified_local_count", 0),
        "source_lock_candidates_ready": candidates.get("ready_count", 0),
        "source_lock_candidates_needing_review": candidates.get("needs_review_count", 0),
        "research_bundle_records": bundles.get("bundle_records", 0),
        "research_bundles_ready_for_extraction_prep": bundles.get("ready_for_extraction_prep_count", 0),
        "research_bundles_partial": bundles.get("partial_count", 0),
        "research_bundles_not_ready": bundles.get("not_ready_count", 0),
        "local_archive_inventory_performed": archive_summary.get("local_archive_inventory_performed", False),
        "raw_archives_processed": archive_summary.get("local_archive_inventory_performed", False),
        "raw_archive_content_committed": False,
        **{key: guardrail.get(key, False) for key in STAGE5AG_FALSE_FLAGS},
        "new_cuda_kernels_added": 0,
        "no_solve_claim": True,
        "no_gpu_ci_safe": True,
        "ci_network_required": False,
        "recommended_next_prompt_type": selected.get("recommended_next_prompt_type"),
        "recommended_next_stage_title": selected.get("recommended_next_stage_title"),
        "recommended_next_stage_reason": selected.get("recommended_next_stage_reason"),
        "deep_research_recommended_next": selected.get("deep_research_recommended_next"),
        "file_inventory_records": file_summary.get("inventory_record_count", 0),
        "gap_report_records": read_yaml(gap_report_path).get("gap_count", 0),
    }
    write_yaml(out, summary)
    write_json(results_dir / SUMMARY_REPORT, summary)
    write_json(results_dir / WARNINGS_REPORT, [])
    return summary


def _select_next(root: dict[str, Any], linkage: dict[str, Any], bundles: dict[str, Any]) -> str:
    if not root.get("root_exists"):
        return "stage5ah_source_lock_gap_closure_for_missing_priority_sources"
    if linkage.get("matched_count", 0) >= 3 and (bundles.get("ready_for_extraction_prep_count", 0) + bundles.get("partial_count", 0)) > 0:
        return "stage5ah_curated_research_bundle_extraction_from_local_inventory"
    if linkage.get("missing_count", 0) > linkage.get("matched_count", 0):
        return "stage5ah_source_lock_gap_closure_for_missing_priority_sources"
    return "stage5ah_harvester_tool_gap_closure"


def _options() -> list[tuple[str, str, str]]:
    return [
        (
            "stage5ah_curated_research_bundle_extraction_from_local_inventory",
            "Stage 5AH - curated research bundle extraction from local source inventory",
            "Local third-party material is inventoried; next step is ignored curated extraction metadata, not interpretation.",
        ),
        (
            "stage5ah_source_lock_gap_closure_for_missing_priority_sources",
            "Stage 5AH - source-lock gap closure for missing priority sources",
            "Several priority sources are still missing or manual-export-only.",
        ),
        (
            "stage5ah_online_fetch_for_missing_manifest_sources",
            "Stage 5AH - online fetch for missing manifest sources",
            "Deferred because Stage 5AG is local-only and online fetch requires explicit future scope.",
        ),
        (
            "stage5ah_deep_research_source_inventory_and_reliability",
            "Stage 5AH - Deep Research source inventory and reliability",
            "Deferred until at least one curated extracted bundle exists.",
        ),
        (
            "stage5ah_visual_page_image_provenance_inventory",
            "Stage 5AH - visual page-image provenance inventory",
            "Deferred until local image variants are curated into source-lock bundles.",
        ),
        (
            "stage5ah_cicada_archive_source_lock_initial_ingestion",
            "Stage 5AH - Cicada archive source-lock initial ingestion",
            "Useful after local archive inventory is curated into a bounded extraction plan.",
        ),
        (
            "stage5ah_harvester_tool_gap_closure",
            "Stage 5AH - harvester tool gap closure",
            "Fallback if Stage 5AG exposes local inventory tooling gaps.",
        ),
        (
            "stage5ah_bounded_cpu_native_scored_experiment_manifest_gate",
            "Stage 5AH - bounded CPU/native scored experiment manifest gate",
            "Rejected because source-lock/provenance work must precede hypotheses.",
        ),
        ("stage5ah_benchmark_planning", "Stage 5AH - benchmark planning", "Rejected because benchmark planning is out of scope."),
        ("stage5ah_unsolved_page_cuda_pilot", "Stage 5AH - unsolved-page CUDA pilot", "Rejected because unsolved-page CUDA remains blocked."),
        ("future_website_expansion_unnumbered", "Future unnumbered website expansion", "Deferred; Stage 5AG does not expand the website."),
    ]
