"""Validation helpers for Stage 5AK community-facts integration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_yaml, resolve
from .models import STAGE5AK_FALSE_FLAGS, STAGE5AK_REPORTS


def validate_stage5ak(
    *,
    inventory_path: Path,
    source_card_summary_path: Path,
    content_index_summary_path: Path,
    attachment_index_path: Path,
    clue_categories_path: Path,
    claim_policy_path: Path,
    claim_records_path: Path,
    correction_log_path: Path,
    arithmetic_preflight_path: Path,
    website_update_path: Path,
    deep_research_update_path: Path,
    readiness_path: Path,
    missing_source_plan_path: Path,
    guardrail_path: Path,
    next_stage_decision_path: Path,
    summary_path: Path,
    results_dir: Path,
) -> tuple[dict[str, Any], list[str]]:
    """Validate Stage 5AK committed records and ignored generated reports."""

    errors: list[str] = []
    inventory = _safe_yaml(errors, inventory_path)
    cards = _safe_yaml(errors, source_card_summary_path)
    content = _safe_yaml(errors, content_index_summary_path)
    attachments = _safe_yaml(errors, attachment_index_path)
    categories = _safe_yaml(errors, clue_categories_path)
    policy = _safe_yaml(errors, claim_policy_path)
    claims = _safe_yaml(errors, claim_records_path)
    corrections = _safe_yaml(errors, correction_log_path)
    arithmetic = _safe_yaml(errors, arithmetic_preflight_path)
    website = _safe_yaml(errors, website_update_path)
    _safe_yaml(errors, deep_research_update_path)
    readiness = _safe_yaml(errors, readiness_path)
    missing = _safe_yaml(errors, missing_source_plan_path)
    guardrail = _safe_yaml(errors, guardrail_path)
    decision = _safe_yaml(errors, next_stage_decision_path)
    summary = _safe_yaml(errors, summary_path)

    if inventory.get("local_folder_exists") is not True:
        errors.append("community_facts_folder_missing")
    if inventory.get("message_log_detected") is not True:
        errors.append("message_log_missing")
    if attachments.get("attachment_index_records", 0) < 10:
        errors.append("attachment_index_records_missing")
    if categories.get("new_clue_category_records", 0) < 15:
        errors.append("community_clue_categories_missing")
    if claims.get("claim_record_count", 0) < 12:
        errors.append("community_claim_records_missing")
    if corrections.get("correction_record_count", 0) < 3:
        errors.append("community_correction_records_missing")
    if arithmetic.get("arithmetic_preflight_records", 0) < 10:
        errors.append("arithmetic_preflight_records_missing")
    if arithmetic.get("arithmetic_error_count", 0) < 1:
        errors.append("arithmetic_error_not_recorded")
    if cards.get("website_publication_allowed_count", 0) != 0 or website.get("public_website_ready_count", 0) != 0:
        errors.append("public_website_publication_not_blocked")
    if readiness.get("bundles_ready_for_private_deep_research", 0) < 10:
        errors.append("private_deep_research_readiness_regressed")
    if readiness.get("bundles_public_website_ready", 0) != 0:
        errors.append("public_website_ready_nonzero")
    if policy.get("execution_ready") is not False:
        errors.append("claim_policy_execution_ready")
    for record in claims.get("records", []):
        if record.get("execution_ready") is not False:
            errors.append(f"claim_execution_ready:{record.get('claim_id')}")
        if record.get("solve_claim") is not False:
            errors.append(f"claim_solve_claim:{record.get('claim_id')}")
        if record.get("website_publication_allowed") is not False:
            errors.append(f"claim_publication_allowed:{record.get('claim_id')}")
    for key, expected in STAGE5AK_FALSE_FLAGS.items():
        if key == "third_party_raw_tracked_new":
            continue
        if guardrail.get(key) is not expected:
            errors.append(f"guardrail_violation:{key}={guardrail.get(key)}")
        if key in summary and summary.get(key) is not expected:
            errors.append(f"summary_guardrail_violation:{key}={summary.get(key)}")
    if guardrail.get("new_cuda_kernels_added") != 0 or summary.get("new_cuda_kernels_added") != 0:
        errors.append("new_cuda_kernels_added_nonzero")
    selected = [record for record in decision.get("records", []) if record.get("selected") is True]
    if len(selected) != 1:
        errors.append(f"selected_decision_count_mismatch:{len(selected)}")
    elif any(
        selected[0].get(field) is not False
        for field in ["scored_experiment_recommended_next", "benchmark_recommended_next", "unsolved_page_cuda_recommended_next", "website_expansion_recommended_next"]
    ):
        errors.append("forbidden_next_stage_selected")
    if missing.get("network_fetch_performed") is not False:
        errors.append("missing_source_plan_network_fetch")
    out_root = resolve(results_dir)
    for filename in STAGE5AK_REPORTS.values():
        if not (out_root / filename).exists():
            errors.append(f"missing_generated_report:{filename}")
    counts = {
        "local_folder_exists": inventory.get("local_folder_exists", False),
        "community_facts_file_count": inventory.get("community_facts_file_count", 0),
        "attachment_count": attachments.get("attachment_index_records", 0),
        "claim_record_count": claims.get("claim_record_count", 0),
        "correction_record_count": corrections.get("correction_record_count", 0),
        "arithmetic_preflight_records": arithmetic.get("arithmetic_preflight_records", 0),
        "source_card_updates": cards.get("source_card_updates", cards.get("source_card_records", 0)),
        "content_index_updates": content.get("content_index_updates", content.get("content_index_records", 0)),
        "bundles_ready_for_private_deep_research": readiness.get("bundles_ready_for_private_deep_research", 0),
        "website_ingest_metadata_ready": website.get("website_ingest_metadata_ready", False),
        "bundles_public_website_ready": readiness.get("bundles_public_website_ready", 0),
        "network_fetch_performed": guardrail.get("network_fetch_performed", False),
        "online_repo_clone_performed": guardrail.get("online_repo_clone_performed", False),
        "google_drive_storage_used": guardrail.get("google_drive_storage_used", False),
        "stage5ak_valid": not errors,
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
