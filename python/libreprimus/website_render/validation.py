"""Validation helpers for Stage 5AM static website exports."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .loader import read_yaml, resolve, write_json, write_yaml
from .models import FALSE_GUARDRAILS, REQUIRED_ASSETS, REQUIRED_DATA_FILES, REQUIRED_PAGES
from .privacy import audit_site

NOINDEX = '<meta name="robots" content="noindex,nofollow,noarchive">'


def validate_static_site(
    *,
    site_root: Path,
    manifest_path: Path,
    privacy_audit_path: Path,
    results_dir: Path,
    out: Path,
) -> tuple[dict[str, Any], list[str]]:
    """Validate required static files and publication guardrails."""

    errors: list[str] = []
    root = resolve(site_root)
    manifest = _safe_yaml(errors, manifest_path)
    audit = _safe_yaml(errors, privacy_audit_path)
    for rel in [*REQUIRED_PAGES, *REQUIRED_DATA_FILES, *REQUIRED_ASSETS]:
        if not (root / rel).exists():
            errors.append(f"missing_static_export_file:{rel}")
    for rel in REQUIRED_PAGES:
        path = root / rel
        if path.exists():
            text = path.read_text(encoding="utf-8")
            if NOINDEX not in text:
                errors.append(f"missing_noindex:{rel}")
            if re.search(r'<script[^>]+src=["\']https?://', text, re.IGNORECASE):
                errors.append(f"external_script_dependency:{rel}")
            if re.search(r'<link[^>]+href=["\']https?://', text, re.IGNORECASE):
                errors.append(f"external_stylesheet_dependency:{rel}")
    robots = root / "robots.txt"
    if robots.exists() and "Disallow: /" not in robots.read_text(encoding="utf-8"):
        errors.append("robots_disallow_all_missing")
    if manifest.get("website_export_generated") is not True:
        errors.append("manifest_website_export_not_generated")
    if audit.get("privacy_audit_passed") is not True:
        errors.append("privacy_audit_failed")
    validation = {
        "record_type": "stage5am_static_site_validation",
        "schema": "schemas/website-render/static-site-validation-v0.schema.json",
        "stage_id": "stage-5am",
        "source_stage_id": "stage-5al",
        "site_root": site_root.as_posix(),
        "static_site_validation_passed": not errors,
        "required_pages_present": not any(error.startswith("missing_static_export_file") for error in errors),
        "robots_noindex_present": not any("noindex" in error for error in errors),
        "robots_disallow_all_present": "robots_disallow_all_missing" not in errors,
        "external_network_dependencies_present": any("external_" in error for error in errors),
        "raw_bodies_included": False,
        "private_ids_published": False,
        "public_website_publication_performed": False,
        "validation_error_count": len(errors),
        "errors": errors,
        "solve_claim": False,
    }
    write_yaml(out, validation)
    write_json(resolve(results_dir) / "static_site_validation.json", validation)
    return validation, errors


def validate_stage5am(
    *,
    render_policy: Path,
    render_inputs: Path,
    manifest: Path,
    validation: Path,
    privacy_audit: Path,
    upload_instructions: Path,
    guardrail: Path,
    next_stage_decision: Path,
    summary: Path,
    site_root: Path,
    results_dir: Path,
) -> tuple[dict[str, Any], list[str]]:
    """Validate committed Stage 5AM records and ignored static export."""

    errors: list[str] = []
    policy = _safe_yaml(errors, render_policy)
    inputs = _safe_yaml(errors, render_inputs)
    output = _safe_yaml(errors, manifest)
    site_validation = _safe_yaml(errors, validation)
    audit = _safe_yaml(errors, privacy_audit)
    upload = _safe_yaml(errors, upload_instructions)
    guard = _safe_yaml(errors, guardrail)
    decision = _safe_yaml(errors, next_stage_decision)
    summary_record = _safe_yaml(errors, summary)

    for name, payload in [
        ("policy", policy),
        ("inputs", inputs),
        ("manifest", output),
        ("validation", site_validation),
        ("privacy_audit", audit),
        ("upload_instructions", upload),
        ("guardrail", guard),
        ("next_stage_decision", decision),
        ("summary", summary_record),
    ]:
        if payload.get("solve_claim") is not False:
            errors.append(f"{name}:solve_claim_not_false")
        if payload.get("raw_bodies_included", False) is not False:
            errors.append(f"{name}:raw_bodies_included")
        if payload.get("private_ids_published", False) is not False:
            errors.append(f"{name}:private_ids_published")

    if policy.get("metadata_only") is not True:
        errors.append("render_policy_not_metadata_only")
    if output.get("website_export_generated") is not True:
        errors.append("website_export_not_generated")
    if site_validation.get("static_site_validation_passed") is not True:
        errors.append("static_site_validation_not_passed")
    if audit.get("privacy_audit_passed") is not True:
        errors.append("privacy_audit_not_passed")
    expected_upload_directory = output.get("upload_directory") or output.get("website_export_root")
    if upload.get("upload_directory") != expected_upload_directory:
        errors.append("upload_directory_mismatch")
    if summary_record.get("upload_instructions_created") is not True:
        errors.append("upload_instructions_not_created")
    if decision.get("selected_next_stage_title") != "Stage 5AN - Deep Research source inventory and reliability prompt":
        errors.append("next_stage_not_stage5an")
    if summary_record.get("status") != "complete":
        errors.append("summary_not_complete")
    for key, expected in FALSE_GUARDRAILS.items():
        if guard.get(key) is not expected:
            errors.append(f"guardrail_violation:{key}={guard.get(key)}")
        if key in summary_record and summary_record.get(key) is not expected:
            errors.append(f"summary_guardrail_violation:{key}={summary_record.get(key)}")
    if guard.get("new_cuda_kernels_added") != 0 or summary_record.get("new_cuda_kernels_added") != 0:
        errors.append("new_cuda_kernels_added_nonzero")

    site_root_present = resolve(site_root).exists()
    generated_summary_present = (resolve(results_dir) / "summary.json").exists()
    if site_root_present:
        fresh_audit = audit_site(site_root)
        if fresh_audit.get("privacy_audit_passed") is not True:
            errors.append("site_privacy_rescan_failed")

    counts = {
        "stage_id": "stage-5am",
        "static_site_validation_passed": site_validation.get("static_site_validation_passed", False) and not errors,
        "privacy_audit_passed": audit.get("privacy_audit_passed", False),
        "source_card_count": inputs.get("source_card_count", 0),
        "content_record_count": inputs.get("content_record_count", 0),
        "claim_record_count": inputs.get("claim_record_count", 0),
        "bundle_count": inputs.get("bundle_count", 0),
        "publication_gate_count": inputs.get("publication_gate_count", 0),
        "missing_source_count": inputs.get("missing_source_count", 0),
        "website_export_root": output.get("website_export_root"),
        "upload_directory": upload.get("upload_directory"),
        "deep_research_next_ready": decision.get("deep_research_next_ready", False),
        "site_root_present": site_root_present,
        "generated_summary_present": generated_summary_present,
        "validation_error_count": len(errors),
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
