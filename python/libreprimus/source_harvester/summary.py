"""Stage 5AF summary and next-stage decision builders."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from .export import read_records, read_yaml, write_json, write_records, write_yaml
from .manifest import manifest_records
from .models import (
    DRY_RUN_SUMMARY_PATH,
    NEXT_STAGE_DECISION_PATH,
    OUTPUT_DIR,
    SUMMARY_PATH,
    SUMMARY_REPORT,
    common_record_flags,
)


def build_next_stage_decision(*, tool_validation_clean: bool = True) -> list[dict[str, Any]]:
    """Build deterministic Stage 5AF next-stage option records."""

    selected_id = (
        "stage5ag_run_source_harvester_on_user_downloads"
        if tool_validation_clean
        else "stage5ag_harvester_gap_closure"
    )
    options = [
        (
            "stage5ag_run_source_harvester_on_user_downloads",
            "Stage 5AG - run source harvester on user-provided downloads and build initial source-lock inventory",
            "Run the validated harvester against local user-provided downloads only, keeping raw outputs ignored.",
            "Codex",
        ),
        (
            "stage5ag_cicada_archive_source_lock_initial_ingestion",
            "Stage 5AG - Cicada archive source-lock initial ingestion",
            "Useful after local user downloads are present and inventoryable.",
            "Codex",
        ),
        (
            "stage5ag_visual_page_image_provenance_inventory",
            "Stage 5AG - visual page-image provenance inventory",
            "Deferred until source-image bundles exist locally.",
            "Codex",
        ),
        (
            "stage5ag_deep_research_source_inventory_and_reliability",
            "Stage 5AG - Deep Research source inventory and reliability",
            "Deferred until the first harvested/source-locked bundle exists.",
            "Deep Research",
        ),
        (
            "stage5ag_harvester_gap_closure",
            "Stage 5AG - source harvester gap closure",
            "Fallback only if Stage 5AF validation exposes implementation gaps.",
            "Codex",
        ),
        (
            "stage5ag_bounded_cpu_native_scored_experiment_manifest_gate",
            "Stage 5AG - bounded CPU/native scored experiment manifest gate",
            "Rejected for next step because source-lock/provenance must precede hypotheses.",
            "Codex",
        ),
        (
            "stage5ag_benchmark_planning",
            "Stage 5AG - benchmark planning",
            "Rejected for next step because Stage 5AF is source-lock tooling only.",
            "Codex",
        ),
        (
            "stage5ag_unsolved_page_cuda_pilot",
            "Stage 5AG - unsolved-page CUDA pilot",
            "Rejected because unsolved-page CUDA remains blocked.",
            "Codex",
        ),
        (
            "future_website_expansion_unnumbered",
            "Future unnumbered website expansion",
            "Rejected because website expansion remains deferred.",
            "Codex",
        ),
    ]
    records = []
    for option_id, title, reason, prompt_type in options:
        selected = option_id == selected_id
        records.append(
            {
                "record_type": "stage5af_source_harvester_next_stage_decision",
                "schema": "schemas/source-harvester/source-harvester-next-stage-decision-record-v0.schema.json",
                **common_record_flags(),
                "option_id": option_id,
                "selected": selected,
                "recommended_next_prompt_type": prompt_type if selected else None,
                "recommended_next_stage_title": title,
                "recommended_next_stage_reason": reason,
                "deep_research_recommended_next": selected and prompt_type == "Deep Research",
                "scored_experiment_recommended_next": False,
                "benchmark_recommended_next": False,
                "unsolved_page_cuda_recommended_next": False,
                "website_expansion_recommended_next": False,
                "execution_enabled": False,
            }
        )
    return records


def summarize_stage5af(
    *,
    source_manifest_path: Path,
    collection_priorities_path: Path,
    clue_target_categories_path: Path,
    research_bundle_plan_path: Path,
    tool_policy_path: Path,
    dry_run_summary_path: Path = DRY_RUN_SUMMARY_PATH,
    next_stage_decision_out: Path = NEXT_STAGE_DECISION_PATH,
    summary_out: Path = SUMMARY_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    """Build the committed Stage 5AF aggregate summary."""

    sources = manifest_records(source_manifest_path)
    priorities = read_records(collection_priorities_path)
    categories = read_records(clue_target_categories_path)
    bundles = read_records(research_bundle_plan_path)
    tool_policy = read_yaml(tool_policy_path)
    dry_run = read_yaml(dry_run_summary_path)
    decisions = build_next_stage_decision(tool_validation_clean=True)
    write_records(
        next_stage_decision_out,
        decisions,
        record_type="stage5af_source_harvester_next_stage_decisions",
        schema="schemas/source-harvester/source-harvester-next-stage-decision-record-v0.schema.json",
    )
    selected = next(record for record in decisions if record["selected"])
    priority_counts = dict(sorted(Counter(record["priority"] for record in sources).items()))
    source_type_counts = dict(sorted(Counter(record["source_type"] for record in sources).items()))
    summary = {
        "record_type": "stage5af_source_harvester_summary",
        **common_record_flags(),
        "status": "complete",
        "source_manifest_records": len(sources),
        "collection_priority_records": len(priorities),
        "clue_target_category_records": len(categories),
        "research_bundle_plan_records": len(bundles),
        "tool_policy_records": 1 if isinstance(tool_policy, dict) else 0,
        "dry_run_plan_records": int(dry_run.get("dry_run_plan_records", 0)),
        "source_harvester_package_added": True,
        "cli_group_added": True,
        "priority_counts": priority_counts,
        "source_type_counts": source_type_counts,
        "manual_collection_required_count": sum(
            1 for record in sources if record.get("manual_collection_required") is True
        ),
        "network_allowed_default": False,
        "download_allowed_default": False,
        "browser_allowed_default": False,
        "google_drive_storage_allowed": False,
        "local_storage_only": True,
        "recommended_next_prompt_type": selected["recommended_next_prompt_type"],
        "recommended_next_stage_title": selected["recommended_next_stage_title"],
        "recommended_next_stage_reason": selected["recommended_next_stage_reason"],
        "deep_research_recommended_next": selected["deep_research_recommended_next"],
    }
    write_yaml(summary_out, summary)
    write_json(out_dir / SUMMARY_REPORT, summary)
    return summary
