"""Validation for Stage 4J observation-review records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.observation_review.loaders import load_yaml_records
from libreprimus.observation_review.models import REVIEW_STATES
from libreprimus.observation_review.path_sanitisation import check_paths_summary
from libreprimus.observation_review.promotion_gates import promotion_blocked_reasons


def validate_observation_review_records(
    *,
    policy: Path,
    decisions: Path,
    promotions: Path,
    quarantine: Path,
    summary: Path,
) -> tuple[dict[str, int], list[str]]:
    """Validate committed Stage 4J observation-review record files."""

    errors: list[str] = []
    policy_records = load_yaml_records(policy)
    decision_records = load_yaml_records(decisions)
    promotion_records = load_yaml_records(promotions)
    quarantine_records = load_yaml_records(quarantine)
    summary_records = load_yaml_records(summary)
    counts = {
        "policy_records": len(policy_records),
        "decision_records": len(decision_records),
        "promotion_records": len(promotion_records),
        "quarantine_records": len(quarantine_records),
        "summary_records": len(summary_records),
    }
    if len(policy_records) != 1:
        errors.append("policy_record_missing")
    if len(summary_records) != 1:
        errors.append("summary_record_missing")
    if not decision_records:
        errors.append("decision_records_missing")
    _validate_common_flags([*policy_records, *decision_records, *promotion_records, *quarantine_records, *summary_records], errors)
    for record in decision_records:
        _validate_decision(record, errors)
    decisions_by_id = {str(record.get("review_decision_id")): record for record in decision_records}
    for record in promotion_records:
        _validate_promotion(record, decisions_by_id, errors)
    for record in quarantine_records:
        if not record.get("why_dangerous"):
            errors.append(f"quarantine_missing_why_dangerous:{record.get('observation_id')}")
        if record.get("allowed_control_use") is not True:
            errors.append(f"quarantine_control_use_not_true:{record.get('observation_id')}")
    if summary_records:
        summary_record = summary_records[0]
        if int(summary_record.get("decisions_created") or -1) != len(decision_records):
            errors.append("summary_decision_count_mismatch")
        if int(summary_record.get("promoted_to_manifest_count") or 0) != 0:
            errors.append("unexpected_manifest_promotion")
    return counts, errors


def validate_path_sanitisation(root: Path) -> tuple[dict[str, int | bool], list[str]]:
    """Validate committed operational docs/records for local path leaks and stale text."""

    summary = check_paths_summary(root)
    errors: list[str] = []
    for finding in summary["findings"]:
        errors.append(f"{finding['kind']}:{finding['path']}:{finding['line']}")
    counts: dict[str, int | bool] = {
        "absolute_local_path_findings": int(summary["absolute_local_path_finding_count"]),
        "stale_operational_text_findings": int(summary["stale_operational_text_finding_count"]),
        "path_sanitisation_passed": bool(summary["path_sanitisation_passed"]),
    }
    return counts, errors


def _validate_common_flags(records: list[dict[str, Any]], errors: list[str]) -> None:
    for record in records:
        label = str(record.get("review_decision_id") or record.get("observation_id") or record.get("policy_id") or record.get("record_type"))
        if record.get("solve_claim") is not False:
            errors.append(f"solve_claim_not_false:{label}")
        if record.get("trusted_as_canonical") is not False:
            errors.append(f"trusted_as_canonical_not_false:{label}")
        if record.get("cuda_used") is True:
            errors.append(f"cuda_used_true:{label}")


def _validate_decision(record: dict[str, Any], errors: list[str]) -> None:
    label = str(record.get("review_decision_id"))
    if record.get("review_state") not in REVIEW_STATES:
        errors.append(f"invalid_review_state:{label}")
    if record.get("usable_as_experiment_seed") is not False:
        errors.append(f"decision_seed_not_false:{label}")
    if record.get("observation_type") == "visual_cuneiform_candidate" and record.get("accepted_reading"):
        errors.append(f"cuneiform_accepted_without_human_review:{label}")
    if record.get("observation_type") == "visual_dot_pattern_candidate" and record.get("ambiguous") is False:
        errors.append(f"dot_ambiguity_forced:{label}")
    if record.get("observation_type") == "discord_derived_lead" and record.get("public_source_corroboration") is not True:
        if "discord_missing_public_source_corroboration" not in record.get("promotion_blocked_reasons", []):
            errors.append(f"discord_missing_block:{label}")


def _validate_promotion(
    record: dict[str, Any],
    decisions_by_id: dict[str, dict[str, Any]],
    errors: list[str],
) -> None:
    review_decision_id = str(record.get("review_decision_id"))
    observation_id = str(record.get("observation_id"))
    decision = decisions_by_id.get(review_decision_id)
    if decision is None:
        errors.append(f"promotion_missing_decision:{observation_id}")
        return
    expected = promotion_blocked_reasons(decision)
    if record.get("blocked_reasons") != expected:
        errors.append(f"promotion_reasons_mismatch:{observation_id}")
    if record.get("promotion_status") != "blocked":
        errors.append(f"promotion_unexpectedly_unblocked:{observation_id}")
    if record.get("usable_as_experiment_seed") is not False:
        errors.append(f"promotion_seed_not_false:{observation_id}")
