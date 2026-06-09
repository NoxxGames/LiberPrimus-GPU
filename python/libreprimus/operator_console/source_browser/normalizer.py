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
ROOT_ALLOWLIST = {"ChatGPT-ContextFile.md", "README.md", "STATUS.md", "ROADMAP.md"}
PATH_BEARING_KEYS = {
    "path",
    "paths",
    "local_path",
    "local_paths",
    "relative_path",
    "relative_paths",
    "source_path",
    "source_paths",
    "source_file",
    "source_files",
    "source_root",
    "source_roots",
    "image_path",
    "image_paths",
    "image_relative_path",
    "document_path",
    "document_paths",
    "pdf_path",
    "audio_path",
    "attachment_path",
    "thread_folder",
    "canonical_page_root",
    "root_path",
    "file_path",
    "source_record_path",
    "schema_path",
}
SOURCE_ROOT_KEYS = {
    "source_root",
    "source_roots",
    "thread_folder",
    "canonical_page_root",
    "root_path",
    "base_path",
}
SOURCE_ROOT_RELATIVE_KEYS = {
    "source_images",
    "source_files",
    "source_documents",
    "image_files",
    "document_files",
    "expected_files",
    "observed_files",
    "files",
    "records",
    "image_locks",
    "pdf_locks",
    "audio_locks",
}
SOURCE_ROOT_RELATIVE_CHILD_KEYS = {"file_name", "image_name", "document_name", "pdf_name", "audio_name"}
LABEL_ONLY_KEYS = {
    "file_name",
    "title",
    "display_title",
    "name",
    "entry_title",
    "source_id",
    "candidate_family_id",
    "claim_id",
    "phrase",
    "text",
    "summary",
    "description",
    "notes",
    "relation",
    "expected_duplicate_note",
    "expected_files_about",
}


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
    entry = SourceBrowserEntry(
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
    entry.search_text = _search_text(entry)
    return entry


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
        search_text="chatgpt context file chatgpt-contextfile.md assistant context handoff",
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


def _collect_paths(raw_record: dict[str, Any]) -> set[str]:
    paths: set[str] = set()
    _collect_paths_from_value(raw_record, paths, source_roots=(), key_path=())
    return _suppress_bare_duplicate_paths(paths)


def _collect_paths_from_value(
    value: Any,
    paths: set[str],
    *,
    source_roots: tuple[str, ...],
    key_path: tuple[str, ...],
) -> None:
    if isinstance(value, dict):
        local_roots = _source_roots_from_mapping(value, source_roots)
        relative_path_present = _has_path_value(value.get("relative_path")) or _has_path_value(
            value.get("image_relative_path")
        )
        for key, item in value.items():
            key_text = str(key)
            key_lower = key_text.lower()
            child_path = (*key_path, key_lower)
            if key_lower in SOURCE_ROOT_KEYS:
                continue
            if key_lower in PATH_BEARING_KEYS:
                _collect_path_value(item, paths, source_roots=local_roots, key=key_lower)
                continue
            if key_lower in SOURCE_ROOT_RELATIVE_KEYS:
                _collect_source_root_relative_value(item, paths, source_roots=local_roots, key_path=child_path)
                continue
            if (
                key_lower in SOURCE_ROOT_RELATIVE_CHILD_KEYS
                and not relative_path_present
                and _parent_allows_filename_resolution(key_path)
            ):
                _collect_source_root_relative_value(item, paths, source_roots=local_roots, key_path=child_path)
                continue
            if key_lower in LABEL_ONLY_KEYS:
                continue
            _collect_paths_from_value(item, paths, source_roots=local_roots, key_path=child_path)
    elif isinstance(value, list):
        for item in value:
            _collect_paths_from_value(item, paths, source_roots=source_roots, key_path=key_path)


def _source_roots_from_mapping(value: dict[str, Any], inherited: tuple[str, ...]) -> tuple[str, ...]:
    roots = list(inherited)
    for key in SOURCE_ROOT_KEYS:
        item = value.get(key)
        if isinstance(item, str):
            _append_source_root(item, roots)
        elif isinstance(item, list):
            for nested in item:
                if isinstance(nested, str):
                    _append_source_root(nested, roots)
    return tuple(dict.fromkeys(roots))


def _append_source_root(text: str, roots: list[str]) -> None:
    normalized = _normalize_path_text(text)
    if normalized and _looks_like_path(normalized) and normalized not in roots:
        roots.append(normalized)


def _collect_path_value(value: Any, paths: set[str], *, source_roots: tuple[str, ...], key: str) -> None:
    if isinstance(value, str):
        _add_path(paths, value, source_roots=source_roots, force_source_root=key in SOURCE_ROOT_RELATIVE_KEYS)
    elif isinstance(value, list):
        for item in value:
            _collect_path_value(item, paths, source_roots=source_roots, key=key)
    elif isinstance(value, dict):
        _collect_paths_from_value(value, paths, source_roots=source_roots, key_path=(key,))


def _collect_source_root_relative_value(
    value: Any,
    paths: set[str],
    *,
    source_roots: tuple[str, ...],
    key_path: tuple[str, ...],
) -> None:
    if isinstance(value, str):
        _add_path(paths, value, source_roots=source_roots, force_source_root=True)
    elif isinstance(value, list):
        for item in value:
            _collect_source_root_relative_value(item, paths, source_roots=source_roots, key_path=key_path)
    elif isinstance(value, dict):
        _collect_paths_from_value(value, paths, source_roots=source_roots, key_path=key_path)


def _add_path(
    paths: set[str],
    text: str,
    *,
    source_roots: tuple[str, ...],
    force_source_root: bool = False,
) -> None:
    normalized = _normalize_path_text(text)
    if not normalized or URL_RE.search(normalized):
        return
    if _is_bare_filename(normalized):
        if normalized in ROOT_ALLOWLIST:
            paths.add(normalized)
            return
        if source_roots and (force_source_root or _has_path_suffix(normalized)):
            for root in source_roots:
                paths.add(f"{root.rstrip('/')}/{normalized}")
            return
        return
    if _looks_like_path(normalized):
        paths.add(normalized)


def _normalize_path_text(text: str) -> str:
    return text.strip().replace("\\", "/")


def _looks_like_path(text: str) -> bool:
    suffix = Path(text).suffix.lower()
    return (
        text in ROOT_ALLOWLIST
        or text.startswith(("data/", "docs/", "third_party/", "experiments/manifests/", "schemas/"))
        or "/" in text
        or suffix in IMAGE_EXTENSIONS
        or suffix in DOCUMENT_EXTENSIONS
    )


def _has_path_suffix(text: str) -> bool:
    return Path(text).suffix.lower() in IMAGE_EXTENSIONS | DOCUMENT_EXTENSIONS


def _is_bare_filename(text: str) -> bool:
    return "/" not in text and "\\" not in text and bool(Path(text).suffix)


def _has_path_value(value: Any) -> bool:
    if isinstance(value, str):
        return bool(_normalize_path_text(value))
    if isinstance(value, list):
        return any(_has_path_value(item) for item in value)
    return False


def _parent_allows_filename_resolution(key_path: tuple[str, ...]) -> bool:
    return any(key in SOURCE_ROOT_RELATIVE_KEYS for key in key_path)


def _suppress_bare_duplicate_paths(paths: set[str]) -> set[str]:
    basenames_with_rooted_path = {
        Path(path).name.lower()
        for path in paths
        if not _is_bare_filename(path) and Path(path).suffix.lower() in IMAGE_EXTENSIONS | DOCUMENT_EXTENSIONS
    }
    return {
        path
        for path in paths
        if not (
            _is_bare_filename(path)
            and Path(path).name.lower() in basenames_with_rooted_path
            and path not in ROOT_ALLOWLIST
        )
    }


def _walk(value: Any) -> Iterable[Any]:
    yield value
    if isinstance(value, dict):
        for item in value.values():
            yield from _walk(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk(item)


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


def _search_text(entry: SourceBrowserEntry) -> str:
    parts = [
        entry.title,
        entry.summary,
        entry.notes or "",
        entry.record_type or "",
        entry.candidate_family_id or "",
        entry.stage_id or "",
        entry.source_record_path,
        " ".join(entry.local_paths),
        " ".join(entry.urls),
        " ".join(entry.warnings),
        " ".join(str(fact) for fact in entry.number_facts),
    ]
    return " ".join(parts).lower()


def _is_compact_value(value: Any) -> bool:
    return value is None or isinstance(value, str | int | float | bool)


def url_label(url: str) -> str:
    parsed = urlparse(url)
    return parsed.netloc or url[:40]
