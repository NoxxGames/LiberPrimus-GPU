"""Validation and summary helpers for the Operator Console Source Browser."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from .context_file import context_file_status
from .loaders import SourceIndex, build_source_index, load_record_file
from .manual_entries import validate_no_huge_raw_blob
from .number_facts import (
    REVIEW_STATES,
    load_enrichment_overlays,
    normalize_entry_number_facts,
    reviewability_counts,
    zero_fact_review_state,
)
from .path_aliases import load_path_aliases, resolve_with_aliases
from ..settings import (
    DEFAULT_COLUMN_PROFILE,
    DEFAULT_PATH_ALIASES,
    MANUAL_ENTRIES_DIR,
    MANUAL_OVERRIDES_DIR,
    TOMBSTONES_DIR,
)


@dataclass
class ValidationResult:
    counts: dict[str, int | str | bool] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_cli_text(self) -> str:
        lines = [f"{key}={_format(value)}" for key, value in self.counts.items()]
        lines.append(f"warning_count={len(self.warnings)}")
        lines.append(f"validation_error_count={len(self.errors)}")
        for warning in self.warnings:
            lines.append(f"warning={warning}")
        for error in self.errors:
            lines.append(f"error={error}")
        return "\n".join(lines)


def validate_source_index() -> ValidationResult:
    index = build_source_index()
    result = ValidationResult(
        counts={
            "records_scanned": len(index.scanned_paths),
            "entries_loaded": len(index.entries),
            "manual_entries": _count_files(MANUAL_ENTRIES_DIR),
            "overrides": _count_files(MANUAL_OVERRIDES_DIR),
            "tombstones": _count_files(TOMBSTONES_DIR),
        }
    )
    result.errors.extend(index.parse_errors)
    seen: set[str] = set()
    duplicate_count = 0
    for entry in index.entries:
        if entry.entry_id in seen:
            duplicate_count += 1
            result.errors.append(f"duplicate entry_id: {entry.entry_id}")
        seen.add(entry.entry_id)
    path_stats = _path_stats(index)
    result.counts.update(
        {
            "duplicate_entry_ids": duplicate_count,
            "image_paths": path_stats["image_paths"],
            "document_paths": path_stats["document_paths"],
            "urls": path_stats["urls"],
            "warnings": path_stats["warnings"],
            "missing_paths": path_stats["missing_paths"],
            "schema_errors": 0,
        }
    )
    result.errors.extend(_validate_config_schema(DEFAULT_PATH_ALIASES))
    result.errors.extend(_validate_config_schema(DEFAULT_COLUMN_PROFILE))
    result.counts["schema_errors"] = sum(1 for error in result.errors if "schema" in error.lower())
    return result


def validate_manual_records() -> ValidationResult:
    index = build_source_index()
    entry_ids = {entry.entry_id for entry in index.entries}
    result = ValidationResult(counts={"manual_entries": 0, "overrides": 0, "tombstones": 0})
    for path in sorted(MANUAL_ENTRIES_DIR.glob("*.yaml")):
        if path.name == ".gitkeep":
            continue
        result.counts["manual_entries"] = int(result.counts["manual_entries"]) + 1
        payload = _load_yaml(path, result)
        if payload is None:
            continue
        result.errors.extend(_validate_payload_schema(path, payload))
        result.errors.extend(f"{path.as_posix()}: {error}" for error in validate_no_huge_raw_blob(payload))
    for path in sorted(MANUAL_OVERRIDES_DIR.glob("*.yaml")):
        if path.name == ".gitkeep":
            continue
        result.counts["overrides"] = int(result.counts["overrides"]) + 1
        payload = _load_yaml(path, result)
        if payload is None:
            continue
        result.errors.extend(_validate_payload_schema(path, payload))
        target = str(payload.get("target_entry_id") or "")
        if target and target not in entry_ids:
            result.errors.append(f"{path.as_posix()}: override target does not exist: {target}")
    for path in sorted(TOMBSTONES_DIR.glob("*.yaml")):
        if path.name == ".gitkeep":
            continue
        result.counts["tombstones"] = int(result.counts["tombstones"]) + 1
        payload = _load_yaml(path, result)
        if payload is None:
            continue
        result.errors.extend(_validate_payload_schema(path, payload))
        target = str(payload.get("target_entry_id") or "")
        if target and target not in entry_ids:
            result.errors.append(f"{path.as_posix()}: tombstone target does not exist: {target}")
    result.counts["schema_errors"] = sum(1 for error in result.errors if "schema" in error.lower())
    return result


def source_browser_summary(index: SourceIndex | None = None) -> dict[str, Any]:
    index = index or build_source_index()
    categories = sorted({entry.category for entry in index.entries})
    path_stats = _path_stats(index)
    return {
        "records_scanned": len(index.scanned_paths),
        "entries_loaded": len(index.entries),
        "manual_entries": sum(1 for entry in index.entries if entry.record_type == "source_browser_manual_entry"),
        "overrides": _count_files(MANUAL_OVERRIDES_DIR),
        "tombstones": _count_files(TOMBSTONES_DIR),
        "image_paths": path_stats["image_paths"],
        "document_paths": path_stats["document_paths"],
        "urls": path_stats["urls"],
        "warnings": path_stats["warnings"],
        "missing_paths": path_stats["missing_paths"],
        "categories": categories,
        "chatgpt_context": context_file_status(),
    }


def validate_number_fact_cards() -> ValidationResult:
    index = build_source_index()
    counts = reviewability_counts(index.entries)
    result = ValidationResult(
        counts={
            "entries_loaded": len(index.entries),
            "fact_cards_extracted": counts["total_number_fact_cards_extracted"],
            "vague_fact_cards": counts["vague_fact_card_count"],
            "zero_fact_not_reviewed_entries": counts[
                "entries_with_zero_extracted_number_facts_not_reviewed"
            ],
            "overlay_count": len(load_enrichment_overlays()),
        }
    )
    for entry in index.entries:
        if not entry.number_facts:
            state = zero_fact_review_state(entry)
            if state not in REVIEW_STATES:
                result.errors.append(f"{entry.source_record_path}: invalid zero-fact state {state}")
            continue
        for card in normalize_entry_number_facts(entry):
            if card.review_state not in REVIEW_STATES:
                result.errors.append(f"{card.source_record_path}: invalid review state {card.review_state}")
            if card.usable_for_decision_now:
                result.errors.append(f"{card.source_record_path}: fact card is decision-usable now")
            if "solve_claim" not in card.not_allowed_as:
                result.errors.append(f"{card.source_record_path}: fact card missing solve_claim guardrail")
    return result


def number_fact_reviewability_summary(index: SourceIndex | None = None) -> dict[str, Any]:
    index = index or build_source_index()
    counts = reviewability_counts(index.entries)
    return {
        "entries_loaded": len(index.entries),
        "fact_cards_extracted": counts["total_number_fact_cards_extracted"],
        "entries_with_vague_number_facts": counts["entries_with_vague_number_facts"],
        "zero_fact_not_reviewed_entries": counts[
            "entries_with_zero_extracted_number_facts_not_reviewed"
        ],
        "entries_with_rich_fact_cards": counts["entries_with_rich_fact_cards"],
        "overlay_count": len(load_enrichment_overlays()),
    }


def _validate_config_schema(path: Path) -> list[str]:
    if not path.exists():
        return [f"{path.as_posix()}: config file missing"]
    payload = load_record_file(path)
    return _validate_payload_schema(path, payload)


def _validate_payload_schema(path: Path, payload: dict[str, Any]) -> list[str]:
    schema_path = payload.get("schema")
    if not isinstance(schema_path, str):
        return [f"{path.as_posix()}: schema path missing"]
    schema_file = Path(schema_path)
    if not schema_file.exists():
        return [f"{path.as_posix()}: schema file missing: {schema_path}"]
    validator = Draft202012Validator(json.loads(schema_file.read_text(encoding="utf-8")))
    return [f"{path.as_posix()}: schema error: {error.message}" for error in validator.iter_errors(payload)]


def _load_yaml(path: Path, result: ValidationResult) -> dict[str, Any] | None:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        result.errors.append(f"{path.as_posix()}: YAML parse failed: {exc}")
        return None
    if not isinstance(payload, dict):
        result.errors.append(f"{path.as_posix()}: record is not a mapping")
        return None
    return payload


def _count_files(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for file_path in path.glob("*.yaml") if file_path.name != ".gitkeep")


def _path_stats(index: SourceIndex) -> dict[str, int]:
    aliases = load_path_aliases()
    missing_paths = 0
    image_paths = 0
    document_paths = 0
    url_count = 0
    warning_count = 0
    for entry in index.entries:
        image_paths += len(entry.image_paths)
        document_paths += len(entry.document_paths)
        url_count += len(entry.urls)
        warning_count += len(entry.warnings)
        for path_text in set(entry.local_paths + entry.image_paths + entry.document_paths):
            if path_text.startswith(("http://", "https://")):
                continue
            if not resolve_with_aliases(path_text, aliases).exists():
                missing_paths += 1
    return {
        "image_paths": image_paths,
        "document_paths": document_paths,
        "urls": url_count,
        "warnings": warning_count,
        "missing_paths": missing_paths,
    }


def _format(value: int | str | bool) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)
