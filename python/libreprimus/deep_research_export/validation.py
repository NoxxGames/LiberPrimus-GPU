"""Validation for Stage 5AN private Deep Research exports."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .file_selection import ABSOLUTE_PATH_PATTERNS, PRIVATE_ID_PATTERNS
from .inputs import read_json, read_yaml, resolve
from .models import NOINDEX, REQUIRED_COMBINED_FILES, REQUIRED_HOSTED_FILES


def validate_stage5an(
    *,
    content_pack_root: Path,
    hosted_export_root: Path,
    combined_webroot: Path,
    policy: Path,
    inputs: Path,
    manifest_summary: Path,
    hosted_summary: Path,
    combined_summary: Path,
    file_selection_summary: Path,
    publication_gate_audit: Path,
    upload_instructions: Path,
    consumption_guide: Path,
    guardrail: Path,
    next_stage_decision: Path,
    summary: Path,
) -> tuple[dict[str, Any], list[str]]:
    """Validate Stage 5AN committed records and generated private outputs."""

    errors: list[str] = []
    records = {
        "policy": _safe_yaml(errors, policy),
        "inputs": _safe_yaml(errors, inputs),
        "manifest_summary": _safe_yaml(errors, manifest_summary),
        "hosted_summary": _safe_yaml(errors, hosted_summary),
        "combined_summary": _safe_yaml(errors, combined_summary),
        "file_selection_summary": _safe_yaml(errors, file_selection_summary),
        "publication_gate_audit": _safe_yaml(errors, publication_gate_audit),
        "upload_instructions": _safe_yaml(errors, upload_instructions),
        "consumption_guide": _safe_yaml(errors, consumption_guide),
        "guardrail": _safe_yaml(errors, guardrail),
        "next_stage_decision": _safe_yaml(errors, next_stage_decision),
        "summary": _safe_yaml(errors, summary),
    }
    for name, payload in records.items():
        if payload.get("solve_claim") is not False:
            errors.append(f"{name}:solve_claim_not_false")
    pack_root = resolve(content_pack_root)
    hosted_root = resolve(hosted_export_root)
    combined_root = resolve(combined_webroot)
    if not pack_root.exists():
        errors.append("content_pack_root_missing")
    if not (pack_root / "deep-research-content-pack-stage5an.zip").exists():
        errors.append("content_pack_zip_missing")
    manifest_path = pack_root / "deep-research-content-pack-stage5an-manifest.json"
    if not manifest_path.exists():
        errors.append("content_pack_manifest_missing")
        manifest: dict[str, Any] = {}
    else:
        manifest = read_json(manifest_path)
    for record in manifest.get("included_files", []):
        rel = record.get("relative_path")
        if not rel or not (pack_root / rel).exists():
            errors.append(f"included_file_missing:{rel}")
        if not record.get("sha256"):
            errors.append(f"included_file_missing_sha256:{rel}")
        if not record.get("publication_status") or not record.get("review_status"):
            errors.append(f"included_file_missing_publication_status:{rel}")
        if record.get("path_kind") == "raw_source_ignored":
            errors.append(f"raw_source_included:{rel}")
    if not hosted_root.exists():
        errors.append("hosted_export_root_missing")
    for rel in REQUIRED_HOSTED_FILES:
        if not (hosted_root / rel).exists():
            errors.append(f"hosted_required_file_missing:{rel}")
    if not combined_root.exists():
        errors.append("combined_webroot_missing")
    for rel in REQUIRED_COMBINED_FILES:
        if not (combined_root / rel).exists():
            errors.append(f"combined_required_file_missing:{rel}")
    _check_noindex(errors, hosted_root / "index.html", "hosted_index")
    _check_noindex(errors, combined_root / "index.html", "combined_index")
    _scan_metadata_files(errors, hosted_root)
    _scan_metadata_files(errors, combined_root)
    if records["publication_gate_audit"].get("publication_gate_audit_passed") is not True:
        errors.append("publication_gate_audit_not_passed")
    if records["upload_instructions"].get("sftp_upload_directory") != "website-export/stage5an/webserver-root/":
        errors.append("upload_directory_mismatch")
    if records["consumption_guide"].get("private_content_url") != "http://liberprimus-gpu-data.info/private-content/":
        errors.append("private_content_url_mismatch")
    false_flags = [
        "network_fetch_performed",
        "online_repo_clone_performed",
        "google_drive_storage_used",
        "deep_research_performed",
        "cuda_execution_performed",
        "cuda_source_modified",
        "benchmark_performed",
        "scored_experiments_executed",
    ]
    for flag in false_flags:
        if records["summary"].get(flag) is not False:
            errors.append(f"summary_guardrail_violation:{flag}")
    if records["summary"].get("new_cuda_kernels_added") != 0:
        errors.append("new_cuda_kernels_added_nonzero")
    counts = {
        "stage_id": "stage-5an",
        "content_pack_valid": not errors,
        "hosted_export_valid": not errors,
        "combined_webroot_valid": not errors,
        "content_pack_file_count": records["summary"].get("content_pack_file_count", 0),
        "hosted_content_file_count": records["summary"].get("hosted_content_file_count", 0),
        "included_bundle_count": records["summary"].get("included_bundle_count", 0),
        "included_source_count": records["summary"].get("included_source_count", 0),
        "included_claim_count": records["summary"].get("included_claim_count", 0),
        "included_content_record_count": records["summary"].get("included_content_record_count", 0),
        "safe_extracts_generated_count": records["summary"].get("safe_extracts_generated_count", 0),
        "deep_research_next_ready": records["summary"].get("deep_research_next_ready", False),
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


def _check_noindex(errors: list[str], path: Path, label: str) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    if NOINDEX not in text:
        errors.append(f"missing_noindex:{label}")


def _scan_metadata_files(errors: list[str], root: Path) -> None:
    if not root.exists():
        return
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".html", ".json", ".js", ".css", ".txt", ".md"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(root).as_posix()
        for pattern in ABSOLUTE_PATH_PATTERNS:
            if pattern.search(text):
                errors.append(f"local_absolute_path_leak:{rel}")
        for pattern in PRIVATE_ID_PATTERNS:
            if pattern.search(text):
                errors.append(f"private_identifier_leak:{rel}")
        if re.search(r"<script[^>]+src=[\"']https?://", text, re.IGNORECASE):
            errors.append(f"external_script_dependency:{rel}")
