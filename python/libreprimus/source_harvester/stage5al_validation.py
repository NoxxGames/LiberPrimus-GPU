"""Validation helpers for Stage 5AL website-ingest staging."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .export import read_yaml, resolve, write_json, write_yaml
from .models import STAGE5AL_FALSE_FLAGS, STAGE5AL_ID, STAGE5AL_REPORTS

ABSOLUTE_PATH_RE = re.compile(r"(^[A-Za-z]:[\\/]|^\\\\)")
REQUIRED_WEBSITE_FILES = [
    "research-index.yaml",
    "research-bundles.yaml",
    "source-cards.yaml",
    "content-index.yaml",
    "community-claims.yaml",
    "publication-gates.yaml",
    "deep-research-export.yaml",
    "missing-sources.yaml",
    "summary.yaml",
]
FORBIDDEN_CLAIM_FIELDS = {"claim_text", "claim_formula", "claimed_values", "source_message_locator", "source_image_refs"}


def validate_website_ingest_stage5al(
    *,
    website_ingest_dir: Path,
    publication_gates_path: Path,
    results_dir: Path,
    out: Path,
) -> tuple[dict[str, Any], list[str]]:
    """Validate the committed Stage 5AL website-ingest package."""

    errors: list[str] = []
    root = resolve(website_ingest_dir)
    for filename in REQUIRED_WEBSITE_FILES:
        if not (root / filename).exists():
            errors.append(f"missing_website_ingest_file:{filename}")
    index = _safe_yaml(errors, root / "research-index.yaml")
    bundles = _safe_yaml(errors, root / "research-bundles.yaml")
    sources = _safe_yaml(errors, root / "source-cards.yaml")
    content = _safe_yaml(errors, root / "content-index.yaml")
    claims = _safe_yaml(errors, root / "community-claims.yaml")
    gates = _safe_yaml(errors, root / "publication-gates.yaml")
    missing = _safe_yaml(errors, root / "missing-sources.yaml")
    summary = _safe_yaml(errors, root / "summary.yaml")
    policy = _safe_yaml(errors, publication_gates_path)

    _validate_records(errors, bundles.get("records", []), "bundle")
    _validate_records(errors, sources.get("records", []), "source")
    _validate_records(errors, content.get("records", []), "content")
    _validate_records(errors, claims.get("records", []), "claim")
    _validate_records(errors, missing.get("records", []), "missing")
    _validate_gates(errors, gates, policy)
    _validate_claims(errors, claims.get("records", []))
    _validate_summary(errors, index, summary, bundles, sources, content, claims, gates, missing)

    result_root = resolve(results_dir)
    for filename in [
        STAGE5AL_REPORTS["source_inventory"],
        STAGE5AL_REPORTS["research_index"],
        STAGE5AL_REPORTS["website_package"],
        STAGE5AL_REPORTS["publication_gates"],
        STAGE5AL_REPORTS["warnings"],
    ]:
        if not (result_root / filename).exists():
            errors.append(f"missing_generated_report:{filename}")

    counts = {
        "record_type": "stage5al_research_index_validation",
        "schema": "schemas/website-ingest/stage5al-summary-v0.schema.json",
        "stage_id": STAGE5AL_ID,
        "website_ingest_valid": not errors,
        "website_ingest_dir": website_ingest_dir.as_posix(),
        "bundle_count": len(bundles.get("records", [])),
        "source_card_count": len(sources.get("records", [])),
        "content_index_count": len(content.get("records", [])),
        "claim_record_count": len(claims.get("records", [])),
        "publication_gate_count": len(gates.get("records", [])),
        "missing_source_count": len(missing.get("records", [])),
        "public_website_ready_count": summary.get("public_website_ready_count", 0),
        "private_ids_published": False,
        "raw_bodies_published": False,
        "validation_error_count": len(errors),
        "errors": errors,
        "solve_claim": False,
    }
    write_yaml(out, counts)
    write_json(result_root / "research_index_validation.json", counts)
    return counts, errors


def validate_stage5al(
    *,
    website_ingest_summary_path: Path,
    website_data_contract_path: Path,
    deep_research_export_path: Path,
    deep_research_export_summary_path: Path,
    publication_gate_policy_path: Path,
    research_index_validation_path: Path,
    guardrail_path: Path,
    next_stage_decision_path: Path,
    summary_path: Path,
    website_ingest_dir: Path,
    results_dir: Path,
) -> tuple[dict[str, Any], list[str]]:
    """Validate Stage 5AL committed records and ignored generated reports."""

    errors: list[str] = []
    website = _safe_yaml(errors, website_ingest_summary_path)
    contract = _safe_yaml(errors, website_data_contract_path)
    export = _safe_yaml(errors, deep_research_export_path)
    export_summary = _safe_yaml(errors, deep_research_export_summary_path)
    gates = _safe_yaml(errors, publication_gate_policy_path)
    validation = _safe_yaml(errors, research_index_validation_path)
    guardrail = _safe_yaml(errors, guardrail_path)
    decision = _safe_yaml(errors, next_stage_decision_path)
    summary = _safe_yaml(errors, summary_path)

    if contract.get("website_data_contract_ready") is not True:
        errors.append("website_data_contract_not_ready")
    if validation.get("website_ingest_valid") is not True:
        errors.append("research_index_validation_not_ready")
    if export.get("deep_research_export_ready") is not True or export_summary.get("deep_research_export_ready") is not True:
        errors.append("deep_research_export_not_ready")
    if website.get("public_website_ready_count", 0) != 0 or summary.get("public_website_ready_count", 0) != 0:
        errors.append("public_website_ready_count_nonzero")
    if website.get("website_expansion_performed") is not False:
        errors.append("website_expansion_performed")
    if gates.get("publication_gate_count", 0) < 7:
        errors.append("publication_gate_records_missing")
    selected = [record for record in decision.get("records", []) if record.get("selected") is True]
    if len(selected) != 1:
        errors.append(f"selected_next_stage_count_mismatch:{len(selected)}")
    elif selected[0].get("deep_research_recommended_next") is not True:
        errors.append("deep_research_not_selected_next")
    for key, expected in STAGE5AL_FALSE_FLAGS.items():
        if key == "third_party_raw_tracked_new":
            continue
        if guardrail.get(key) is not expected:
            errors.append(f"guardrail_violation:{key}={guardrail.get(key)}")
        if key in summary and summary.get(key) is not expected:
            errors.append(f"summary_guardrail_violation:{key}={summary.get(key)}")
    if guardrail.get("new_cuda_kernels_added") != 0 or summary.get("new_cuda_kernels_added") != 0:
        errors.append("new_cuda_kernels_added_nonzero")
    validate_counts, validate_errors = validate_website_ingest_stage5al(
        website_ingest_dir=website_ingest_dir,
        publication_gates_path=publication_gate_policy_path,
        results_dir=results_dir,
        out=research_index_validation_path,
    )
    errors.extend(error for error in validate_errors if error not in errors)
    result_root = resolve(results_dir)
    for filename in [STAGE5AL_REPORTS["deep_research_export"], STAGE5AL_REPORTS["summary"], STAGE5AL_REPORTS["warnings"]]:
        if not (result_root / filename).exists():
            errors.append(f"missing_generated_report:{filename}")
    counts = {
        "website_ingest_valid": validate_counts.get("website_ingest_valid", False) and not errors,
        "website_shell_present": website.get("website_shell_present", False),
        "source_card_count": summary.get("source_card_count", 0),
        "content_index_count": summary.get("content_index_count", 0),
        "claim_record_count": summary.get("claim_record_count", 0),
        "publication_gate_count": summary.get("publication_gate_count", 0),
        "deep_research_export_ready": summary.get("deep_research_export_ready", False),
        "public_website_ready_count": summary.get("public_website_ready_count", 0),
        "private_only_count": summary.get("private_only_count", 0),
        "review_blocked_count": summary.get("review_blocked_count", 0),
        "network_fetch_performed": summary.get("network_fetch_performed", False),
        "online_repo_clone_performed": summary.get("online_repo_clone_performed", False),
        "google_drive_storage_used": summary.get("google_drive_storage_used", False),
        "validation_error_count": len(errors),
    }
    return counts, errors


def _validate_records(errors: list[str], records: list[dict[str, Any]], kind: str) -> None:
    for index, record in enumerate(records):
        prefix = f"{kind}:{index}"
        if record.get("solve_claim") is not False:
            errors.append(f"{prefix}:solve_claim")
        if record.get("website_publication_allowed") is not False and kind in {"bundle", "source", "content", "claim"}:
            errors.append(f"{prefix}:website_publication_allowed")
        if record.get("raw_content_publication_allowed") is not False and kind != "missing":
            errors.append(f"{prefix}:raw_content_publication_allowed")
        if record.get("generated_extract_publication_allowed") is not False and kind != "missing":
            errors.append(f"{prefix}:generated_extract_publication_allowed")
        for field in ("relative_path_or_ref", "source_refs"):
            if field in record and _contains_absolute_path(record[field]):
                errors.append(f"{prefix}:absolute_path:{field}")


def _validate_claims(errors: list[str], records: list[dict[str, Any]]) -> None:
    for record in records:
        claim_id = record.get("claim_id", "unknown")
        for field in FORBIDDEN_CLAIM_FIELDS:
            if field in record:
                errors.append(f"claim_forbidden_field:{claim_id}:{field}")
        if record.get("publication_status") != "blocked_private_or_sensitive":
            errors.append(f"claim_not_private_blocked:{claim_id}")
        if record.get("execution_ready") is not False:
            errors.append(f"claim_execution_ready:{claim_id}")


def _validate_gates(errors: list[str], gates: dict[str, Any], policy: dict[str, Any]) -> None:
    if gates.get("publication_gate_count") != policy.get("publication_gate_count"):
        errors.append("publication_gate_policy_mismatch")
    for record in gates.get("records", []):
        if record.get("website_publication_allowed") is not False:
            errors.append(f"gate_publication_allowed:{record.get('status')}")
        if record.get("raw_content_publication_allowed") is not False:
            errors.append(f"gate_raw_publication_allowed:{record.get('status')}")
        if record.get("private_ids_allowed") is not False:
            errors.append(f"gate_private_ids_allowed:{record.get('status')}")


def _validate_summary(
    errors: list[str],
    index: dict[str, Any],
    summary: dict[str, Any],
    bundles: dict[str, Any],
    sources: dict[str, Any],
    content: dict[str, Any],
    claims: dict[str, Any],
    gates: dict[str, Any],
    missing: dict[str, Any],
) -> None:
    expected = {
        "bundle_count": len(bundles.get("records", [])),
        "source_card_count": len(sources.get("records", [])),
        "content_index_count": len(content.get("records", [])),
        "claim_record_count": len(claims.get("records", [])),
        "publication_gate_count": len(gates.get("records", [])),
        "missing_source_count": len(missing.get("records", [])),
    }
    for key, value in expected.items():
        if summary.get(key) != value:
            errors.append(f"summary_count_mismatch:{key}:{summary.get(key)}!={value}")
        if key in index and index.get(key) != value:
            errors.append(f"index_count_mismatch:{key}:{index.get(key)}!={value}")


def _contains_absolute_path(value: Any) -> bool:
    if isinstance(value, str):
        return bool(ABSOLUTE_PATH_RE.search(value.replace("\\", "/")))
    if isinstance(value, list):
        return any(_contains_absolute_path(item) for item in value)
    if isinstance(value, dict):
        return any(_contains_absolute_path(item) for item in value.values())
    return False


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
