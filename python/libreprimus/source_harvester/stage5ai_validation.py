"""Validation helpers for Stage 5AI curated research bundles."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_yaml, resolve
from .models import STAGE5AI_FALSE_FLAGS, STAGE5AI_REPORTS


def validate_stage5ai(
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
    summary_path: Path,
    bundle_root: Path,
    results_dir: Path,
) -> tuple[dict[str, Any], list[str]]:
    """Validate committed Stage 5AI records and ignored generated indexes."""

    errors: list[str] = []
    policy = _safe_yaml(errors, policy_path)
    cards = _safe_yaml(errors, source_card_summary_path)
    content = _safe_yaml(errors, content_index_summary_path)
    website = _safe_yaml(errors, website_ingest_format_path)
    deep_research = _safe_yaml(errors, deep_research_pack_format_path)
    bundles = _safe_yaml(errors, bundle_generation_summary_path)
    classification = _safe_yaml(errors, classification_path)
    missing = _safe_yaml(errors, missing_source_plan_path)
    readiness = _safe_yaml(errors, readiness_path)
    guardrail = _safe_yaml(errors, guardrail_path)
    decision = _safe_yaml(errors, next_stage_decision_path)
    summary = _safe_yaml(errors, summary_path)

    if policy.get("raw_content_commit_allowed") is not False:
        errors.append("raw_content_commit_allowed")
    if policy.get("generated_extract_commit_allowed") is not False:
        errors.append("generated_extract_commit_allowed")
    for key, expected in STAGE5AI_FALSE_FLAGS.items():
        if key == "third_party_raw_tracked_new":
            continue
        if guardrail.get(key) is not expected:
            errors.append(f"guardrail_violation:{key}={guardrail.get(key)}")
    if guardrail.get("new_cuda_kernels_added") != 0:
        errors.append("new_cuda_kernels_added_nonzero")
    if summary.get("stage_id") != "stage-5ai" or summary.get("status") != "complete":
        errors.append("summary_stage_or_status_unexpected")
    _expect_equal(errors, "summary_source_card_count", summary.get("source_card_records"), cards.get("source_card_records"))
    _expect_equal(errors, "summary_content_count", summary.get("content_index_records"), content.get("content_index_records"))
    _expect_equal(errors, "summary_bundle_count", summary.get("curated_bundle_records"), bundles.get("curated_bundle_records"))
    _expect_equal(errors, "summary_deep_research_count", summary.get("deep_research_pack_records"), deep_research.get("deep_research_pack_records"))
    _expect_equal(errors, "summary_missing_count", summary.get("missing_source_records"), missing.get("missing_source_records"))
    _expect_equal(errors, "summary_classification_count", summary.get("unclassified_source_classification_records"), classification.get("classification_records"))
    if website.get("website_ingest_metadata_ready") is not True:
        errors.append("website_ingest_metadata_not_ready")
    if website.get("public_website_ready_count", 0) != 0:
        errors.append("public_website_ready_count_nonzero")
    if readiness.get("bundles_with_generated_skeleton", 0) < 10:
        errors.append("not_all_bundle_skeletons_generated")
    if readiness.get("bundles_ready_for_private_deep_research", 0) < 1:
        errors.append("no_private_deep_research_bundle_ready")
    selected = [record for record in decision.get("records", []) if record.get("selected") is True]
    if len(selected) != 1:
        errors.append(f"selected_decision_count_mismatch:{len(selected)}")
    elif selected[0].get("scored_experiment_recommended_next") is not False:
        errors.append("scored_experiment_recommended")
    root = resolve(bundle_root)
    for relative in (
        "master_manifest.yaml",
        "source_cards.jsonl",
        "content_index.jsonl",
        "website_ingest_index.json",
        "deep_research_pack_index.json",
        "missing_sources.jsonl",
        "do_not_assume_global.md",
        "known_questions_global.md",
    ):
        if not (root / relative).exists():
            errors.append(f"missing_bundle_root_file:{relative}")
    for bundle_dir in sorted(root.glob("[0-9][0-9]-*")):
        for filename in ("manifest.yaml", "known_questions.md", "do_not_assume.md", "deep_research_context.md"):
            if not (bundle_dir / filename).exists():
                errors.append(f"missing_bundle_file:{bundle_dir.name}/{filename}")
    out_root = resolve(results_dir)
    for filename in STAGE5AI_REPORTS.values():
        if not (out_root / filename).exists():
            errors.append(f"missing_generated_report:{filename}")
    counts = {
        "curated_bundle_records": summary.get("curated_bundle_records", 0),
        "source_card_records": summary.get("source_card_records", 0),
        "content_index_records": summary.get("content_index_records", 0),
        "website_ingest_source_card_records": summary.get("website_ingest_source_card_records", 0),
        "website_ingest_content_records": summary.get("website_ingest_content_records", 0),
        "deep_research_pack_records": summary.get("deep_research_pack_records", 0),
        "missing_source_records": summary.get("missing_source_records", 0),
        "unclassified_source_classification_records": summary.get("unclassified_source_classification_records", 0),
        "bundles_with_generated_skeleton": summary.get("bundles_with_generated_skeleton", 0),
        "bundles_with_extracted_local_content": summary.get("bundles_with_extracted_local_content", 0),
        "bundles_ready_for_private_deep_research": summary.get("bundles_ready_for_private_deep_research", 0),
        "bundles_public_website_ready": summary.get("bundles_public_website_ready", 0),
        "deep_research_recommended_next": summary.get("deep_research_recommended_next", False),
        "network_fetch_performed": summary.get("network_fetch_performed", False),
        "online_repo_clone_performed": summary.get("online_repo_clone_performed", False),
        "google_drive_storage_used": summary.get("google_drive_storage_used", False),
        "stage5ai_valid": not errors,
    }
    return counts, errors


def _safe_yaml(errors: list[str], path: Path) -> dict[str, Any]:
    try:
        payload = read_yaml(path)
    except (OSError, ValueError) as exc:
        errors.append(f"yaml_load_failed:{path}:{exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"yaml_not_mapping:{path}")
        return {}
    return payload


def _expect_equal(errors: list[str], name: str, left: Any, right: Any) -> None:
    if left != right:
        errors.append(f"{name}_mismatch:{left}!={right}")
