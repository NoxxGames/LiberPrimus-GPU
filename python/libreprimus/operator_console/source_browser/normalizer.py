"""Normalize committed and manual records into Source Browser entries."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .entries import SourceBrowserEntry
from ..settings import DOCUMENT_EXTENSIONS, IMAGE_EXTENSIONS

URL_RE = re.compile(r"https?://[^\s)>\"]+")
SHA_RE = re.compile(r"^[0-9a-fA-F]{32,128}$")


def normalize_record(source_record_path: Path, raw_record: dict[str, Any]) -> SourceBrowserEntry:
    record_type = _string_or_none(raw_record.get("record_type"))
    stage_id = _string_or_none(raw_record.get("stage_id"))
    candidate_family_id = _first_string(
        raw_record,
        (
            "candidate_family_id",
            "candidate_id",
            "candidate_record_id",
            "candidate_key",
            "record_id",
            "source_id",
            "entry_id",
        ),
    )
    source_type = _first_string(raw_record, ("source_type", "source_context", "source_kind"))
    source_status = _first_string(raw_record, ("source_status", "status", "ready_state", "review_state"))
    trust_tier = _first_string(raw_record, ("trust_tier", "trust_classification", "trust_level"))
    confidence = _first_string(
        raw_record,
        ("confidence", "confidence_label", "confidence_level", "evidence_strength"),
    )
    title = _title(raw_record, source_record_path, record_type, candidate_family_id)
    summary = _summary(raw_record, title)
    local_paths = sorted(_collect_paths(raw_record))
    image_paths = sorted(path for path in local_paths if Path(path).suffix.lower() in IMAGE_EXTENSIONS)
    document_paths = sorted(
        path for path in local_paths if Path(path).suffix.lower() in DOCUMENT_EXTENSIONS
    )
    urls = sorted(_collect_urls(raw_record))
    warnings = sorted(_collect_warning_strings(raw_record))
    hashes = _collect_hashes(raw_record)
    number_facts = _collect_number_facts(raw_record)
    links_to = sorted(_collect_links(raw_record))
    entry_type = _entry_type(raw_record, record_type, source_record_path)
    category = _category(
        record_type=record_type,
        entry_type=entry_type,
        title=title,
        source_record_path=source_record_path,
        source_type=source_type,
        candidate_family_id=candidate_family_id,
        image_paths=image_paths,
        document_paths=document_paths,
        urls=urls,
        number_facts=number_facts,
        warnings=warnings,
    )
    entry_id = _entry_id(raw_record, record_type, candidate_family_id, source_record_path)
    return SourceBrowserEntry(
        entry_id=entry_id,
        entry_type=entry_type,
        category=category,
        title=title,
        summary=summary,
        stage_id=stage_id,
        record_type=record_type,
        candidate_family_id=candidate_family_id,
        source_type=source_type,
        source_status=source_status,
        trust_tier=trust_tier,
        confidence=confidence,
        selected_now=_first_bool(raw_record, ("selected_now", "pivot_target_selected_now")),
        solve_claim=_first_bool(raw_record, ("solve_claim",)),
        execution_allowed=_first_bool(raw_record, ("execution_allowed", "execution_authorized_now")),
        source_lock_only=_first_bool(raw_record, ("source_lock_only",)),
        local_paths=local_paths,
        image_paths=image_paths,
        document_paths=document_paths,
        urls=urls,
        hashes=hashes,
        number_facts=number_facts,
        links_to=links_to,
        warnings=warnings,
        notes=_first_string(raw_record, ("notes", "operator_notes", "review_notes")),
        created_at=_first_string(raw_record, ("created_at", "created")),
        modified_at=_first_string(raw_record, ("modified_at", "updated_at", "modified")),
        source_record_path=source_record_path.as_posix(),
        schema_path=_string_or_none(raw_record.get("schema")),
        raw_record=raw_record,
    )


def context_entry(path: Path) -> SourceBrowserEntry:
    exists = path.exists()
    raw = {
        "record_type": "chatgpt_context_file",
        "stage_id": None,
        "path": path.as_posix(),
        "status": "present" if exists else "missing",
        "solve_claim": False,
        "execution_allowed": False,
    }
    return SourceBrowserEntry(
        entry_id="chatgpt-context-file",
        entry_type="chatgpt_context",
        category="ChatGPT context",
        title="ChatGPT-ContextFile.md",
        summary="Assistant context handoff file for concise project facts and stage state.",
        stage_id=None,
        record_type="chatgpt_context_file",
        candidate_family_id=None,
        source_type="operator_context_file",
        source_status="present" if exists else "missing",
        trust_tier=None,
        confidence=None,
        selected_now=False,
        solve_claim=False,
        execution_allowed=False,
        source_lock_only=False,
        local_paths=[path.as_posix()],
        image_paths=[],
        document_paths=[path.as_posix()],
        urls=[],
        hashes={},
        number_facts=[],
        links_to=[],
        warnings=[] if exists else ["ChatGPT context file is missing"],
        notes=None,
        created_at=None,
        modified_at=None,
        source_record_path=path.as_posix(),
        schema_path=None,
        raw_record=raw,
    )


def _entry_id(
    raw_record: dict[str, Any],
    record_type: str | None,
    candidate_family_id: str | None,
    source_record_path: Path,
) -> str:
    if raw_record.get("record_type") == "source_browser_manual_entry":
        explicit = _string_or_none(raw_record.get("entry_id"))
        if explicit:
            return explicit
    base = "|".join(
        [
            record_type or "record",
            candidate_family_id or _first_string(raw_record, ("source_id", "record_id")) or "",
            source_record_path.as_posix(),
        ]
    )
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", base.lower()).strip("-")[:80]
    suffix = hashlib.sha256(base.encode("utf-8")).hexdigest()[:12]
    return f"{slug}-{suffix}" if slug else f"source-entry-{suffix}"


def _entry_type(raw_record: dict[str, Any], record_type: str | None, source_record_path: Path) -> str:
    if record_type == "source_browser_manual_entry":
        return _first_string(raw_record, ("entry_type",)) or "manual_entry"
    if "source-lock" in source_record_path.as_posix() or "source_lock" in (record_type or ""):
        return "source_lock"
    if "candidate" in (record_type or "") or "candidate" in source_record_path.as_posix():
        return "candidate_record"
    if "summary" in (record_type or ""):
        return "summary"
    return record_type or "metadata_record"


def _title(
    raw_record: dict[str, Any],
    source_record_path: Path,
    record_type: str | None,
    candidate_family_id: str | None,
) -> str:
    for key in ("title", "stage_title", "display_title", "name", "entry_title"):
        value = _string_or_none(raw_record.get(key))
        if value:
            return value
    if candidate_family_id:
        return candidate_family_id.replace("_", " ")
    if record_type:
        return record_type.replace("_", " ")
    return source_record_path.stem.replace("-", " ")


def _summary(raw_record: dict[str, Any], fallback: str) -> str:
    for key in ("summary", "description", "notes", "purpose", "stage_title"):
        value = _string_or_none(raw_record.get(key))
        if value:
            return value[:500]
    return fallback


def _category(
    *,
    record_type: str | None,
    entry_type: str,
    title: str,
    source_record_path: Path,
    source_type: str | None,
    candidate_family_id: str | None,
    image_paths: list[str],
    document_paths: list[str],
    urls: list[str],
    number_facts: list[dict[str, Any]],
    warnings: list[str],
) -> str:
    haystack = " ".join(
        filter(
            None,
            [record_type, entry_type, title, source_type, candidate_family_id, source_record_path.as_posix()],
        )
    ).lower()
    if "manual" in entry_type:
        return "Manual entries"
    if "mayfly" in haystack:
        return "Mayfly"
    if "dot" in haystack:
        return "Dots"
    if "cover" in haystack:
        return "Cover geometry"
    if "diskcipher" in haystack or "disk-cipher" in haystack:
        return "DiskCipher"
    if "triangle" in haystack:
        return "Triangle"
    if "page32" in haystack or "page-32" in haystack:
        return "Page32"
    if "blake" in haystack:
        return "Blake"
    if "music" in haystack or "mp3" in haystack:
        return "Music"
    if "hash" in haystack or "preimage" in haystack:
        return "Hash contracts"
    if "quote" in haystack or "crib" in haystack:
        return "Quote / crib candidates"
    if warnings:
        return "Warnings"
    if "source-lock" in haystack or "source_lock" in haystack:
        return "Source-locks"
    if "candidate" in haystack:
        return "Candidate families"
    if number_facts or "number" in haystack or "numeric" in haystack:
        return "Number facts"
    if image_paths:
        return "Images"
    if document_paths:
        return "Documents"
    if urls:
        return "References"
    if "fixture" in haystack or "solved" in haystack:
        return "Solved precedents"
    return "References"


def _first_string(raw_record: dict[str, Any], keys: Iterable[str]) -> str | None:
    for key in keys:
        value = _string_or_none(raw_record.get(key))
        if value:
            return value
    return None


def _first_bool(raw_record: dict[str, Any], keys: Iterable[str]) -> bool | None:
    for key in keys:
        value = raw_record.get(key)
        if isinstance(value, bool):
            return value
    return None


def _string_or_none(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    if isinstance(value, int | float):
        return str(value)
    return None


def _walk(value: Any) -> Iterable[Any]:
    yield value
    if isinstance(value, dict):
        for item in value.values():
            yield from _walk(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk(item)


def _collect_paths(raw_record: dict[str, Any]) -> set[str]:
    paths: set[str] = set()
    for value in _walk(raw_record):
        if not isinstance(value, str):
            continue
        text = value.strip()
        if not text or URL_RE.search(text):
            continue
        suffix = Path(text).suffix.lower()
        if (
            text == "ChatGPT-ContextFile.md"
            or text.startswith(("data/", "docs/", "third_party/", "experiments/manifests/"))
            or suffix in IMAGE_EXTENSIONS
            or suffix in DOCUMENT_EXTENSIONS
        ):
            paths.add(text.replace("\\", "/"))
    return paths


def _collect_urls(raw_record: dict[str, Any]) -> set[str]:
    urls: set[str] = set()
    for value in _walk(raw_record):
        if isinstance(value, str):
            urls.update(match.group(0).rstrip(".,") for match in URL_RE.finditer(value))
    return urls


def _collect_hashes(raw_record: dict[str, Any]) -> dict[str, str]:
    hashes: dict[str, str] = {}

    def visit(value: Any, prefix: str = "") -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                key_text = f"{prefix}.{key}" if prefix else str(key)
                if isinstance(item, str) and ("sha" in str(key).lower() or "hash" in str(key).lower()):
                    if SHA_RE.match(item):
                        hashes[key_text] = item.lower()
                visit(item, key_text)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                visit(item, f"{prefix}[{index}]")

    visit(raw_record)
    return hashes


def _collect_warning_strings(raw_record: dict[str, Any]) -> set[str]:
    warnings: set[str] = set()

    def visit(value: Any, key_hint: str = "") -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                visit(item, str(key).lower())
        elif isinstance(value, list):
            for item in value:
                visit(item, key_hint)
        elif isinstance(value, str) and (
            "warning" in key_hint
            or "blocker" in key_hint
            or "gap" in key_hint
            or "missing" in value.lower()
        ):
            warnings.add(value[:300])

    visit(raw_record)
    return warnings


def _collect_links(raw_record: dict[str, Any]) -> set[str]:
    links: set[str] = set()

    def visit(value: Any, key_hint: str = "") -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                visit(item, str(key).lower())
        elif isinstance(value, list):
            for item in value:
                visit(item, key_hint)
        elif isinstance(value, str) and ("link" in key_hint or "reference" in key_hint):
            if not URL_RE.search(value):
                links.add(value[:300])

    visit(raw_record)
    return links


def _collect_number_facts(raw_record: dict[str, Any]) -> list[dict[str, Any]]:
    facts: list[dict[str, Any]] = []

    def visit(value: Any, key_hint: str = "") -> None:
        if len(facts) >= 20:
            return
        if isinstance(value, dict):
            keys = {str(key).lower() for key in value}
            if keys & {"fact_id", "expression", "result", "claimed_value", "numeric_value", "value"} and (
                "number" in key_hint or "fact" in key_hint or "numeric" in key_hint or "claim" in key_hint
            ):
                facts.append({str(key): item for key, item in value.items() if _is_compact_value(item)})
                return
            for key, item in value.items():
                visit(item, str(key).lower())
        elif isinstance(value, list):
            for item in value:
                visit(item, key_hint)

    visit(raw_record)
    return facts


def _is_compact_value(value: Any) -> bool:
    return value is None or isinstance(value, str | int | float | bool)


def url_label(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc or url[:40]
