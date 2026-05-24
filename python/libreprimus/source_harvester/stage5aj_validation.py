"""Validation helpers for Stage 5AJ UsefulFiles integration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_yaml, resolve
from .models import STAGE5AJ_FALSE_FLAGS, STAGE5AJ_REPORTS


def validate_stage5aj(
    *,
    inventory_path: Path,
    manifest_extension_path: Path,
    source_card_summary_path: Path,
    content_index_summary_path: Path,
    xlsx_summary_path: Path,
    important_links_path: Path,
    new_clue_categories_path: Path,
    fidelity_policy_path: Path,
    redaction_policy_path: Path,
    scraper_policy_path: Path,
    website_update_path: Path,
    deep_research_update_path: Path,
    readiness_path: Path,
    missing_source_plan_path: Path,
    guardrail_path: Path,
    next_stage_decision_path: Path,
    summary_path: Path,
    results_dir: Path,
) -> tuple[dict[str, Any], list[str]]:
    """Validate Stage 5AJ committed records and ignored generated reports."""

    errors: list[str] = []
    inventory = _safe_yaml(errors, inventory_path)
    manifest = _safe_yaml(errors, manifest_extension_path)
    cards = _safe_yaml(errors, source_card_summary_path)
    content = _safe_yaml(errors, content_index_summary_path)
    xlsx = _safe_yaml(errors, xlsx_summary_path)
    links = _safe_yaml(errors, important_links_path)
    categories = _safe_yaml(errors, new_clue_categories_path)
    fidelity = _safe_yaml(errors, fidelity_policy_path)
    redaction = _safe_yaml(errors, redaction_policy_path)
    scraper = _safe_yaml(errors, scraper_policy_path)
    website = _safe_yaml(errors, website_update_path)
    deep = _safe_yaml(errors, deep_research_update_path)
    readiness = _safe_yaml(errors, readiness_path)
    missing = _safe_yaml(errors, missing_source_plan_path)
    guardrail = _safe_yaml(errors, guardrail_path)
    decision = _safe_yaml(errors, next_stage_decision_path)
    summary = _safe_yaml(errors, summary_path)

    if inventory.get("local_folder_exists") is not True:
        errors.append("usefulfiles_folder_missing")
    if manifest.get("local_source_records", 0) < 5:
        errors.append("local_source_records_missing")
    if xlsx.get("xlsx_workbooks_detected", 0) < 2:
        errors.append("xlsx_workbooks_missing")
    if xlsx.get("lp_excel_detected") is not True:
        errors.append("lp_excel_not_detected")
    if xlsx.get("translations_decryptions_detected") is not True:
        errors.append("translations_decryptions_not_detected")
    if links.get("important_links_urls_found", 0) < 1:
        errors.append("important_links_urls_missing")
    if categories.get("new_clue_category_records", 0) < 16:
        errors.append("new_clue_categories_missing")
    if cards.get("source_card_records", 0) != content.get("source_card_records", cards.get("source_card_records", 0)):
        errors.append("source_card_content_summary_mismatch")
    if website.get("website_expansion_performed") is not False:
        errors.append("website_expansion_performed")
    if website.get("public_website_ready_count", 0) != 0:
        errors.append("public_website_ready_nonzero")
    if deep.get("deep_research_performed") is not False:
        errors.append("deep_research_performed")
    if readiness.get("bundles_ready_for_private_deep_research", 0) < 1:
        errors.append("no_private_deep_research_ready_bundle")
    for key, expected in STAGE5AJ_FALSE_FLAGS.items():
        if key == "third_party_raw_tracked_new":
            continue
        if guardrail.get(key) is not expected:
            errors.append(f"guardrail_violation:{key}={guardrail.get(key)}")
        if key in summary and summary.get(key) is not expected:
            errors.append(f"summary_guardrail_violation:{key}={summary.get(key)}")
    if guardrail.get("new_cuda_kernels_added") != 0 or summary.get("new_cuda_kernels_added") != 0:
        errors.append("new_cuda_kernels_added_nonzero")
    if fidelity.get("private_deep_research_extract_view", {}).get("preserve_runes") is not True:
        errors.append("fidelity_private_rune_preservation_missing")
    if redaction.get("redaction_log_required") is not True:
        errors.append("redaction_log_not_required")
    if not scraper.get("capture_profiles"):
        errors.append("scraper_profiles_missing")
    selected = [record for record in decision.get("records", []) if record.get("selected") is True]
    if len(selected) != 1:
        errors.append(f"selected_decision_count_mismatch:{len(selected)}")
    elif selected[0].get("scored_experiment_recommended_next") is not False:
        errors.append("scored_experiment_recommended")
    if missing.get("network_fetch_performed") is not False:
        errors.append("missing_source_plan_network_fetch")
    out_root = resolve(results_dir)
    for filename in STAGE5AJ_REPORTS.values():
        if not (out_root / filename).exists():
            errors.append(f"missing_generated_report:{filename}")
    counts = {
        "local_folder_exists": inventory.get("local_folder_exists", False),
        "new_local_source_records": manifest.get("local_source_records", 0),
        "new_url_source_records": manifest.get("new_url_source_records", 0),
        "xlsx_workbooks_detected": xlsx.get("xlsx_workbooks_detected", 0),
        "important_links_urls_found": links.get("important_links_urls_found", 0),
        "source_card_updates": cards.get("source_card_records", 0),
        "content_index_updates": content.get("content_index_records", 0),
        "bundles_ready_for_private_deep_research": readiness.get("bundles_ready_for_private_deep_research", 0),
        "website_ingest_metadata_ready": website.get("website_ingest_metadata_ready", False),
        "bundles_public_website_ready": readiness.get("bundles_public_website_ready", 0),
        "network_fetch_performed": guardrail.get("network_fetch_performed", False),
        "online_repo_clone_performed": guardrail.get("online_repo_clone_performed", False),
        "google_drive_storage_used": guardrail.get("google_drive_storage_used", False),
        "stage5aj_valid": not errors,
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
