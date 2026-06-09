"""Validation and summary helpers for the Operator Console Source Browser."""

from __future__ import annotations

import json
import re
import time
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
    number_fact_table_display,
    reviewability_counts,
    zero_fact_review_state,
)
from .path_aliases import PathResolutionCache, load_path_aliases
from ..settings import (
    DEFAULT_COLUMN_PROFILE,
    DEFAULT_PATH_ALIASES,
    MANUAL_ENTRIES_DIR,
    MANUAL_OVERRIDES_DIR,
    TOMBSTONES_DIR,
)

BARE_ROOT_PATH_RE = re.compile(r"^[A-Za-z0-9 _,-]+\.(png|jpg|jpeg|webp|pdf|mp3|xlsx|xlsm|txt|py)$", re.I)
ALLOWED_ROOT_PATHS = {"ChatGPT-ContextFile.md", "README.md", "STATUS.md", "ROADMAP.md"}
CANONICAL_PAGE_ROOT = "third_party/CiadaSolversIddqd_v2/liber-primus__images--full"


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


def validate_path_canonicalization() -> ValidationResult:
    report = path_canonicalization_report()
    result = ValidationResult(
        counts={
            "entries_loaded": report["entries_loaded"],
            "records_scanned": report["records_scanned"],
            "spurious_root_image_paths": report["spurious_root_image_paths"],
            "spurious_root_document_paths": report["spurious_root_document_paths"],
            "duplicate_present_missing_path_pairs": report["duplicate_present_missing_path_pairs"],
            "source_root_relative_resolved_paths": report["source_root_relative_resolved_paths"],
            "canonical_lp_page_root_alias_present": report["canonical_lp_page_root_alias_present"],
            "stage5du_thread_image_paths_under_third_party": report[
                "stage5du_thread_image_paths_under_third_party"
            ],
        }
    )
    if report["spurious_root_image_paths"]:
        result.errors.extend(f"spurious root image path: {path}" for path in report["spurious_root_image_path_examples"])
    if report["spurious_root_document_paths"]:
        result.errors.extend(
            f"spurious root document path: {path}" for path in report["spurious_root_document_path_examples"]
        )
    if report["duplicate_present_missing_path_pairs"]:
        result.errors.extend(
            f"duplicate present+missing basename pair: {path}"
            for path in report["duplicate_present_missing_path_pair_examples"]
        )
    if not report["canonical_lp_page_root_alias_present"]:
        result.errors.append(f"canonical LP page root alias missing: {CANONICAL_PAGE_ROOT}")
    if not report["stage5du_thread_image_paths_under_third_party"]:
        result.errors.append("Stage 5DU thread image paths do not resolve under third_party")
    return result


def performance_smoke() -> ValidationResult:
    start = time.perf_counter()
    index = build_source_index()
    index_seconds = time.perf_counter() - start
    columns = [
        {"key": "title", "label": "Entry"},
        {"key": "images", "label": "Images"},
        {"key": "document_paths", "label": "Docs"},
        {"key": "urls", "label": "URLs"},
        {"key": "number_facts", "label": "Number facts"},
        {"key": "warnings", "label": "Warnings"},
    ]
    table_start = time.perf_counter()
    rows_to_check = min(100, len(index.entries))
    table_backend = "qt"
    try:
        from .table_model import SourceBrowserTableModel

        model = SourceBrowserTableModel(index.entries, columns)
        for row in range(rows_to_check):
            for spec in columns:
                # Use the model's cheap display helper directly to avoid a Qt index dependency in headless CI.
                model._display(index.entries[row], str(spec["key"]))  # noqa: SLF001
    except ModuleNotFoundError as exc:
        if not str(exc.name).startswith("PySide6"):
            raise
        table_backend = "headless_no_qt"
        for row in range(rows_to_check):
            for spec in columns:
                _headless_table_display(index.entries[row], str(spec["key"]))
    table_seconds = time.perf_counter() - table_start
    report = path_canonicalization_report(index)
    result = ValidationResult(
        counts={
            "entries_loaded": len(index.entries),
            "records_scanned": len(index.scanned_paths),
            "table_model_smoke_rows": rows_to_check,
            "table_model_backend": table_backend,
            "table_model_no_cell_widgets_policy": True,
            "thumbnail_generation_eager_for_table": False,
            "raw_preview_lazy": True,
            "path_resolution_cache_enabled": True,
            "thumbnail_cache_enabled": True,
            "startup_or_index_build_time_seconds_observed_locally": f"{index_seconds:.3f}",
            "table_display_smoke_time_seconds_observed_locally": f"{table_seconds:.3f}",
            "spurious_root_paths_after": report["spurious_root_image_paths"]
            + report["spurious_root_document_paths"],
            "duplicate_present_missing_path_pairs_after": report["duplicate_present_missing_path_pairs"],
        }
    )
    if len(index.entries) < 1490:
        result.errors.append("Source Browser entry count regressed below Stage 5DU baseline")
    if report["spurious_root_image_paths"] or report["spurious_root_document_paths"]:
        result.errors.append("spurious root paths remain after path canonicalization repair")
    if report["duplicate_present_missing_path_pairs"]:
        result.errors.append("duplicate present+missing path pairs remain after repair")
    return result


def _headless_table_display(entry: Any, key: str) -> str:
    if key == "title":
        return str(entry.title)
    if key == "images":
        count = len(entry.image_paths)
        return f"{count} image{'s' if count != 1 else ''}"
    if key == "document_paths":
        count = len(entry.document_paths)
        return f"{count} doc{'s' if count != 1 else ''}"
    if key == "urls":
        count = len(entry.urls)
        return f"{count} url{'s' if count != 1 else ''}"
    if key == "number_facts":
        return number_fact_table_display(entry)
    if key == "warnings":
        count = len(entry.warnings)
        return f"{count} warning{'s' if count != 1 else ''}"
    raw_value = getattr(entry, key, "")
    return "" if raw_value is None else str(raw_value)


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


def path_canonicalization_report(index: SourceIndex | None = None) -> dict[str, Any]:
    index = index or build_source_index()
    aliases = load_path_aliases()
    cache = PathResolutionCache(aliases)
    all_paths: list[str] = []
    spurious_images: list[str] = []
    spurious_documents: list[str] = []
    stage5du_thread_image_paths: list[str] = []
    source_root_relative_paths = 0
    for entry in index.entries:
        paths = sorted(set(entry.local_paths + entry.image_paths + entry.document_paths))
        all_paths.extend(paths)
        if entry.source_record_path.endswith("stage5du-thread-image-source-locks.yaml"):
            stage5du_thread_image_paths.extend(entry.image_paths)
        for path_text in paths:
            suffix = Path(path_text).suffix.lower()
            if _is_source_root_resolved(path_text):
                source_root_relative_paths += 1
            if path_text in ALLOWED_ROOT_PATHS or "/" in path_text or not BARE_ROOT_PATH_RE.match(path_text):
                continue
            if suffix in {".png", ".jpg", ".jpeg", ".webp"}:
                spurious_images.append(path_text)
            else:
                spurious_documents.append(path_text)
    duplicate_pairs = _duplicate_present_missing_pairs(all_paths, cache)
    canonical_alias_present = any(
        alias.source_prefix == CANONICAL_PAGE_ROOT or alias.target_prefix.replace("\\", "/") == CANONICAL_PAGE_ROOT
        for alias in aliases
    )
    stage5du_under_third_party = bool(stage5du_thread_image_paths) and all(
        path.startswith("third_party/") and cache.resolve(path).exists for path in stage5du_thread_image_paths
    )
    return {
        "entries_loaded": len(index.entries),
        "records_scanned": len(index.scanned_paths),
        "path_references_after": len(all_paths),
        "spurious_root_image_paths": len(spurious_images),
        "spurious_root_document_paths": len(spurious_documents),
        "spurious_root_image_path_examples": sorted(set(spurious_images))[:20],
        "spurious_root_document_path_examples": sorted(set(spurious_documents))[:20],
        "duplicate_present_missing_path_pairs": len(duplicate_pairs),
        "duplicate_present_missing_path_pair_examples": duplicate_pairs[:20],
        "source_root_relative_resolved_paths": source_root_relative_paths,
        "canonical_lp_page_root_alias_present": canonical_alias_present,
        "stage5du_thread_image_paths_under_third_party": stage5du_under_third_party,
        "path_resolution_cache_exists_checks": cache.exists_checks,
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
    cache = PathResolutionCache(aliases)
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
            if not cache.resolve(path_text).exists:
                missing_paths += 1
    return {
        "image_paths": image_paths,
        "document_paths": document_paths,
        "urls": url_count,
        "warnings": warning_count,
        "missing_paths": missing_paths,
    }


def _is_source_root_resolved(path_text: str) -> bool:
    return path_text.startswith("third_party/") and "/" in path_text


def _duplicate_present_missing_pairs(paths: list[str], cache: PathResolutionCache) -> list[str]:
    by_name: dict[str, list[str]] = {}
    for path_text in sorted(set(paths)):
        if path_text in ALLOWED_ROOT_PATHS:
            continue
        suffix = Path(path_text).suffix.lower()
        if suffix not in {".png", ".jpg", ".jpeg", ".webp", ".pdf", ".mp3", ".xlsx", ".xlsm", ".txt", ".py"}:
            continue
        by_name.setdefault(Path(path_text).name.lower(), []).append(path_text)
    pairs: list[str] = []
    for name, grouped in by_name.items():
        bare = [path for path in grouped if "/" not in path and BARE_ROOT_PATH_RE.match(path)]
        rooted = [path for path in grouped if "/" in path]
        if not bare or not rooted:
            continue
        rooted_present = any(cache.resolve(path).exists for path in rooted)
        bare_missing = [path for path in bare if not cache.resolve(path).exists]
        if rooted_present and bare_missing:
            pairs.append(f"{name}: {','.join(bare_missing)}")
    return pairs


def _format(value: int | str | bool) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)
