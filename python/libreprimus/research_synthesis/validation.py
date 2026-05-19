"""Validation for Stage 3Y research-synthesis records."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.paths import repo_root
from libreprimus.research_synthesis.loader import load_all_record_sets, resolve_repo_path
from libreprimus.research_synthesis.models import (
    ALLOWED_METHOD_STATUSES,
    DEFAULT_DATA_DIR,
    DEFAULT_STAGED_PLAN,
    RECORD_SET_SPECS,
    REQUIRED_METHOD_FAMILIES,
)


def validate_research_synthesis(
    data_dir: Path = DEFAULT_DATA_DIR,
    staged_plan: Path = DEFAULT_STAGED_PLAN,
) -> tuple[dict[str, Any], list[str]]:
    """Validate research-synthesis records and staged-plan guardrails."""

    errors: list[str] = []
    summary: dict[str, Any] = {
        "data_dir": str(data_dir),
        "staged_plan": str(staged_plan),
        "record_counts": {},
        "method_status_counts": {},
    }

    staged_plan_path = resolve_repo_path(staged_plan)
    if not staged_plan_path.is_file():
        errors.append(f"staged_plan_missing: {staged_plan_path}")
    else:
        staged_text = staged_plan_path.read_text(encoding="utf-8").lower()
        _require_text(errors, staged_text, ("stage 3w", "complete"), "staged_plan_stage3w_complete")
        _require_text(errors, staged_text, ("stage 3x", "complete"), "staged_plan_stage3x_complete")
        _require_text(errors, staged_text, ("stage 3y", "complete"), "staged_plan_stage3y_complete")
        _require_text(errors, staged_text, ("stage 3z",), "staged_plan_stage3z_present")
        _require_text(
            errors,
            staged_text,
            ("stage 4a", "discord research-bundle", "deep research"),
            "staged_plan_stage4a_discord_research_bundle",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 4b", "source-lock", "visual observation"),
            "staged_plan_stage4b_source_lock_visual_observation",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 4c", "cuneiform", "dot"),
            "staged_plan_stage4c_cuneiform_dot",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 4d", "bounded numeric verifier"),
            "staged_plan_stage4d_bounded_numeric_verifier",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 4e", "cookie exact-candidate refresh"),
            "staged_plan_stage4e_cookie_exact_candidate_refresh_next",
        )
        _require_text(errors, staged_text, ("cuda", "deferred"), "staged_plan_cuda_deferred")
        _require_text(errors, staged_text, ("canonical corpus", "inactive"), "staged_plan_canonical_inactive")
        _require_text(errors, staged_text, ("page boundaries", "reviewable"), "staged_plan_boundaries_reviewable")
        _require_text(errors, staged_text, ("update policy",), "staged_plan_update_policy")

    records_by_key: dict[str, list[dict[str, Any]]] = {}
    try:
        records_by_key = load_all_record_sets(data_dir)
    except (FileNotFoundError, ValueError) as error:
        errors.append(str(error))
        return summary, errors

    for spec in RECORD_SET_SPECS:
        records = records_by_key.get(spec.key, [])
        summary["record_counts"][spec.key] = len(records)
        schema_path = repo_root() / spec.schema_path
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            errors.append(f"schema_missing: {schema_path}")
            continue
        validator = Draft202012Validator(schema)
        for index, record in enumerate(records):
            if record.get("record_type") != spec.record_type:
                errors.append(f"{spec.filename}[{index}] record_type mismatch")
            for validation_error in validator.iter_errors(record):
                path = ".".join(str(part) for part in validation_error.path)
                errors.append(f"{spec.filename}[{index}] {path}: {validation_error.message}")

    method_records = records_by_key.get("method_families", [])
    method_ids = {str(record.get("method_family_id")) for record in method_records}
    missing_methods = REQUIRED_METHOD_FAMILIES - method_ids
    if missing_methods:
        errors.append(f"missing_method_families: {sorted(missing_methods)}")

    status_counter = Counter(str(record.get("status")) for record in method_records)
    summary["method_status_counts"] = dict(sorted(status_counter.items()))
    for record in method_records:
        method_id = str(record.get("method_family_id"))
        status = str(record.get("status"))
        if status not in ALLOWED_METHOD_STATUSES:
            errors.append(f"invalid_method_status: {method_id}={status}")
        if not record.get("reopen_conditions"):
            errors.append(f"missing_reopen_conditions: {method_id}")
        if not record.get("stop_conditions"):
            errors.append(f"missing_stop_conditions: {method_id}")
        if record.get("solve_claim") is not False:
            errors.append(f"solve_claim_not_false: {method_id}")

    retirement_records = records_by_key.get("method_retirements", [])
    for record in retirement_records:
        method_id = str(record.get("method_family_id"))
        if method_id not in method_ids:
            errors.append(f"retirement_references_missing_method: {method_id}")
        if not record.get("reopen_conditions"):
            errors.append(f"retirement_missing_reopen_conditions: {method_id}")

    direction_changes = records_by_key.get("direction_changes", [])
    stage4a_change = _find_record(direction_changes, "change_id", "stage3z-stage4-discord-bundle-priority")
    if stage4a_change is None:
        errors.append("stage3z_stage4_discord_bundle_priority_missing")
    else:
        new_direction = str(stage4a_change.get("new_direction", "")).lower()
        affected_docs = " ".join(str(item) for item in stage4a_change.get("affected_docs", [])).lower()
        if "discord research-bundle" not in new_direction or "deep research" not in new_direction:
            errors.append("stage3z_stage4_direction_missing_discord_deep_research")
        if "docs/roadmap/staged-plan.md" not in affected_docs or "roadmap.md" not in affected_docs:
            errors.append("stage3z_stage4_direction_missing_affected_docs")
    stage4b_change = _find_record(direction_changes, "change_id", "stage4b-source-lock-visual-intake-priority")
    if stage4b_change is None:
        errors.append("stage4b_source_lock_visual_intake_priority_missing")
    else:
        new_direction = str(stage4b_change.get("new_direction", "")).lower()
        if "source" not in new_direction or "visual" not in new_direction or "annotation" not in new_direction:
            errors.append("stage4b_direction_missing_source_visual_annotation")

    influence_records = records_by_key.get("deep_research_influences", [])
    if _find_record(influence_records, "report_id", "stage4a-discord-research-bundle-review") is None:
        errors.append("stage4a_discord_research_bundle_review_influence_missing")

    cuneiform_dot = _find_method(method_records, "cuneiform_dot_annotation_pack")
    if cuneiform_dot is None:
        errors.append("cuneiform_dot_annotation_pack_missing")
    else:
        stop_text = " ".join(str(item).lower() for item in cuneiform_dot.get("stop_conditions", []))
        if "seed" not in stop_text or "unreviewed" not in stop_text:
            errors.append("cuneiform_dot_annotation_pack_missing_seed_guardrail")

    bounded_numeric = _find_method(method_records, "bounded_numeric_verifier_pack")
    if bounded_numeric is None:
        errors.append("bounded_numeric_verifier_pack_missing")
    else:
        stop_text = " ".join(str(item).lower() for item in bounded_numeric.get("stop_conditions", []))
        if "no-fudge" not in stop_text or "broaden" not in stop_text:
            errors.append("bounded_numeric_verifier_pack_missing_no_fudge_guardrail")

    cuda = _find_method(method_records, "cuda_gpu_acceleration")
    if cuda is None or cuda.get("status") != "deferred":
        errors.append("cuda_gpu_acceleration_not_deferred")

    cookie = _find_method(method_records, "cookie_hash_sha256_packs")
    if cookie is None:
        errors.append("cookie_hash_sha256_packs_missing")
    else:
        stop_text = " ".join(str(item).lower() for item in cookie.get("stop_conditions", []))
        if "broad" not in stop_text or "new source" not in stop_text:
            errors.append("cookie_hash_sha256_pack_missing_no_broadening_guardrail")

    for key, records in records_by_key.items():
        for record in records:
            if record.get("solve_claim") is True:
                errors.append(f"{key}:{record.get('record_type')} solve_claim=true")
            if record.get("raw_outputs_committed") is True:
                errors.append(f"{key}:{record.get('record_type')} raw_outputs_committed=true")
            if record.get("generated_outputs_committed") is True:
                errors.append(f"{key}:{record.get('record_type')} generated_outputs_committed=true")

    summary["valid"] = not errors
    return summary, errors


def _require_text(errors: list[str], text: str, terms: tuple[str, ...], check_id: str) -> None:
    if not all(term in text for term in terms):
        errors.append(check_id)


def _find_method(records: list[dict[str, Any]], method_family_id: str) -> dict[str, Any] | None:
    for record in records:
        if record.get("method_family_id") == method_family_id:
            return record
    return None


def _find_record(records: list[dict[str, Any]], key: str, value: str) -> dict[str, Any] | None:
    for record in records:
        if record.get(key) == value:
            return record
    return None
