"""Validation helpers for visual numeric and cookie/hash observation records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.history.source_records import resolve_repo_path

CONFIDENCE_VALUES = {"high", "medium", "low", "review_required", "rejected"}
REVIEW_STATUSES = {
    "unreviewed",
    "machine_checked",
    "human_review_required",
    "accepted_as_observation",
    "rejected",
}


def load_records(path: Path) -> list[dict[str, Any]]:
    resolved = resolve_repo_path(path)
    payload = yaml.safe_load(resolved.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("records"), list):
        raise ValueError(f"Record file must contain a records list: {resolved}")
    records = payload["records"]
    if not all(isinstance(record, dict) for record in records):
        raise ValueError(f"Every record must be a mapping: {resolved}")
    return records


def validate_visual_records(path: Path) -> tuple[int, list[str]]:
    records = load_records(path)
    errors: list[str] = []
    seen: set[str] = set()
    for record in records:
        observation_id = str(record.get("observation_id", ""))
        if observation_id in seen:
            errors.append(f"{observation_id}: duplicate observation_id")
        seen.add(observation_id)
        if record.get("record_type") != "visual_numeric_observation":
            errors.append(f"{observation_id}: invalid record_type")
        if record.get("confidence") not in CONFIDENCE_VALUES:
            errors.append(f"{observation_id}: invalid confidence")
        if record.get("review_status") not in REVIEW_STATUSES:
            errors.append(f"{observation_id}: invalid review_status")
        if record.get("trusted_as_canonical") is not False:
            errors.append(f"{observation_id}: trusted_as_canonical must be false")
        if record.get("usable_as_experiment_seed") is not False:
            errors.append(f"{observation_id}: usable_as_experiment_seed must be false")
        readings = record.get("candidate_readings")
        if not isinstance(readings, list) or not readings:
            errors.append(f"{observation_id}: candidate_readings must be non-empty")
        elif not all(isinstance(reading, dict) and reading.get("confidence") in CONFIDENCE_VALUES for reading in readings):
            errors.append(f"{observation_id}: invalid candidate reading")
    return len(records), errors


def validate_cookie_records(path: Path) -> tuple[int, list[str]]:
    records = load_records(path)
    errors: list[str] = []
    seen: set[str] = set()
    for record in records:
        cookie_id = str(record.get("cookie_id", ""))
        if cookie_id in seen:
            errors.append(f"{cookie_id}: duplicate cookie_id")
        seen.add(cookie_id)
        value = str(record.get("cookie_value", ""))
        if record.get("record_type") != "cookie_hash_record":
            errors.append(f"{cookie_id}: invalid record_type")
        if record.get("trusted_as_canonical") is not False:
            errors.append(f"{cookie_id}: trusted_as_canonical must be false")
        if record.get("preimage_status") not in {"unknown", "not_attempted", "rejected"}:
            errors.append(f"{cookie_id}: preimage_status must not claim a preimage")
        if record.get("value_format") != "hex64" or len(value) != 64 or any(ch not in "0123456789abcdefABCDEF" for ch in value):
            errors.append(f"{cookie_id}: cookie value must be hex64")
    return len(records), errors


def summarize_observations(
    *,
    visual: Path,
    cookies: Path,
    sources: Path,
) -> dict[str, int]:
    from libreprimus.history.source_records import load_yaml_records

    visual_records = load_records(visual)
    cookie_records = load_records(cookies)
    source_records = load_yaml_records(sources)
    seed_disabled_count = sum(
        1 for record in visual_records if record.get("usable_as_experiment_seed") is False
    )
    return {
        "source_record_count": len(source_records),
        "visual_observation_count": len(visual_records),
        "cookie_hash_record_count": len(cookie_records),
        "visual_seed_disabled_count": seed_disabled_count,
    }
