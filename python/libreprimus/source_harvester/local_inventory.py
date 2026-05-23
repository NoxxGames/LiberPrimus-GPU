"""Stage 5AG local third-party source inventory helpers."""

from __future__ import annotations

import gzip
import hashlib
import mimetypes
import subprocess
import tarfile
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from libreprimus.paths import repo_root

from .export import repo_relative, resolve, write_csv, write_json, write_jsonl, write_yaml
from .models import (
    DUPLICATE_HASHES_REPORT,
    FULL_ARCHIVE_INVENTORY_REPORT,
    FULL_FILE_INVENTORY_CSV_REPORT,
    FULL_FILE_INVENTORY_REPORT,
    FULL_HASH_INVENTORY_REPORT,
    STAGE5AG_ARCHIVE_SUMMARY_PATH,
    STAGE5AG_FILE_SUMMARY_PATH,
    STAGE5AG_HASH_SUMMARY_PATH,
    STAGE5AG_ID,
    STAGE5AG_OUTPUT_DIR,
    STAGE5AG_ROOT_INVENTORY_PATH,
    STAGE5AG_SOURCE_STAGE_ID,
)

ARCHIVE_EXTENSIONS = {".zip", ".tar", ".tgz", ".7z", ".rar", ".gz"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tif", ".tiff"}
PDF_EXTENSIONS = {".pdf"}
DOCX_EXTENSIONS = {".docx"}
TEXT_EXTENSIONS = {".txt", ".md", ".csv", ".json", ".yaml", ".yml", ".rtf", ".log"}
HTML_EXTENSIONS = {".html", ".htm", ".xhtml"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".ogg", ".mid", ".midi", ".m4a"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm", ".avi", ".mkv"}


def inventory_local_sources(
    *,
    source_root: Path,
    results_dir: Path = STAGE5AG_OUTPUT_DIR,
    out_root_inventory: Path = STAGE5AG_ROOT_INVENTORY_PATH,
    out_file_summary: Path = STAGE5AG_FILE_SUMMARY_PATH,
    out_archive_summary: Path = STAGE5AG_ARCHIVE_SUMMARY_PATH,
    out_hash_summary: Path = STAGE5AG_HASH_SUMMARY_PATH,
) -> dict[str, Any]:
    """Inventory local ignored source material without extracting or committing raw content."""

    root = resolve(source_root)
    output_dir = resolve(results_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    files = sorted((item for item in root.rglob("*") if item.is_file()), key=lambda item: _sort_key(item, root)) if root.exists() else []
    dirs = sorted((item for item in root.rglob("*") if item.is_dir()), key=lambda item: _sort_key(item, root)) if root.exists() else []

    file_records: list[dict[str, Any]] = []
    hash_records: list[dict[str, Any]] = []
    for file_path in files:
        digest = _sha256_file(file_path)
        file_record = _file_record(file_path, root=root, digest=digest)
        file_records.append(file_record)
        hash_records.append(
            {
                "record_type": "stage5ag_hash_inventory_record",
                "stage_id": STAGE5AG_ID,
                "source_stage_id": STAGE5AG_SOURCE_STAGE_ID,
                "path": file_record["path"],
                "sha256": digest,
                "size_bytes": file_record["size_bytes"],
                "hash_algorithm": "sha256",
                "raw_content_included": False,
                "raw_file_committed": False,
                "solve_claim": False,
            }
        )

    archive_records = [_archive_record(path, root=root, digest=record["sha256"]) for path, record in zip(files, hash_records) if path.suffix.lower() in ARCHIVE_EXTENSIONS]
    duplicates = _duplicate_hash_groups(hash_records)
    extension_counts = _counter_to_dict(Counter(record["extension"] for record in file_records))
    mime_counts = _counter_to_dict(Counter(record["mime_guess"] for record in file_records))
    category_counts = Counter(record["category"] for record in file_records)

    root_inventory = {
        "record_type": "stage5ag_local_source_root_inventory",
        "schema": "schemas/source-harvester/local-source-root-inventory-record-v0.schema.json",
        "stage_id": STAGE5AG_ID,
        "source_stage_id": STAGE5AG_SOURCE_STAGE_ID,
        "source_root": repo_relative(root),
        "root_exists": root.exists(),
        "root_is_ignored": _raw_content_under_root_is_ignored(source_root),
        "status": "inventoried" if root.exists() else "blocked_missing_source_root",
        "total_files": len(files),
        "total_dirs": len(dirs),
        "total_size_bytes": sum(record["size_bytes"] for record in file_records),
        "extension_counts": extension_counts,
        "mime_guess_counts": mime_counts,
        "archive_counts": _counter_to_dict(Counter(record["archive_type"] for record in archive_records)),
        "image_counts": category_counts.get("image", 0),
        "pdf_counts": category_counts.get("pdf", 0),
        "docx_counts": category_counts.get("docx", 0),
        "text_counts": category_counts.get("text", 0),
        "html_counts": category_counts.get("html", 0),
        "audio_counts": category_counts.get("audio", 0),
        "video_counts": category_counts.get("video", 0),
        "unsupported_archive_count": sum(1 for record in archive_records if not record["supported_for_listing"]),
        "largest_files": _largest_files(file_records),
        "top_level_entries": _top_level_entries(root),
        "untracked_raw_files_present": _untracked_raw_files_present(source_root),
        "tracked_raw_files_present": _tracked_raw_files_present(source_root),
        "staged_raw_files_present": _staged_raw_files_present(source_root),
        "metadata_only": True,
        "raw_content_included": False,
        "solve_claim": False,
    }
    file_summary = {
        "record_type": "stage5ag_local_source_file_inventory_summary",
        "schema": "schemas/source-harvester/local-source-file-inventory-summary-record-v0.schema.json",
        "stage_id": STAGE5AG_ID,
        "source_stage_id": STAGE5AG_SOURCE_STAGE_ID,
        "inventory_record_count": len(file_records),
        "full_inventory_generated_path": repo_relative(output_dir / FULL_FILE_INVENTORY_REPORT),
        "full_inventory_csv_generated_path": repo_relative(output_dir / FULL_FILE_INVENTORY_CSV_REPORT),
        "full_inventory_committed": False,
        "metadata_only": True,
        "raw_content_included": False,
        "category_counts": _counter_to_dict(category_counts),
        "extension_counts": extension_counts,
        "solve_claim": False,
    }
    archive_summary = {
        "record_type": "stage5ag_local_archive_inventory_summary",
        "schema": "schemas/source-harvester/local-archive-inventory-summary-record-v0.schema.json",
        "stage_id": STAGE5AG_ID,
        "source_stage_id": STAGE5AG_SOURCE_STAGE_ID,
        "archive_record_count": len(archive_records),
        "supported_archive_count": sum(1 for record in archive_records if record["supported_for_listing"]),
        "unsupported_archive_count": sum(1 for record in archive_records if not record["supported_for_listing"]),
        "local_archive_inventory_performed": bool(archive_records),
        "raw_extraction_performed": False,
        "raw_archive_content_committed": False,
        "records": archive_records,
        "solve_claim": False,
    }
    hash_summary = {
        "record_type": "stage5ag_local_source_hash_inventory_summary",
        "schema": "schemas/source-harvester/local-source-hash-inventory-summary-record-v0.schema.json",
        "stage_id": STAGE5AG_ID,
        "source_stage_id": STAGE5AG_SOURCE_STAGE_ID,
        "total_hashed_files": len(hash_records),
        "unique_hash_count": len({record["sha256"] for record in hash_records}),
        "duplicate_hash_groups": len(duplicates),
        "largest_duplicate_groups": duplicates[:10],
        "hash_algorithm": "sha256",
        "full_hash_inventory_generated_path": repo_relative(output_dir / FULL_HASH_INVENTORY_REPORT),
        "metadata_only": True,
        "raw_content_included": False,
        "solve_claim": False,
    }

    write_jsonl(output_dir / FULL_FILE_INVENTORY_REPORT, file_records)
    write_csv(output_dir / FULL_FILE_INVENTORY_CSV_REPORT, file_records)
    write_jsonl(output_dir / FULL_HASH_INVENTORY_REPORT, hash_records)
    write_jsonl(output_dir / FULL_ARCHIVE_INVENTORY_REPORT, archive_records)
    write_json(output_dir / DUPLICATE_HASHES_REPORT, duplicates)
    write_yaml(out_root_inventory, root_inventory)
    write_yaml(out_file_summary, file_summary)
    write_yaml(out_archive_summary, archive_summary)
    write_yaml(out_hash_summary, hash_summary)
    return {
        "root_inventory": root_inventory,
        "file_summary": file_summary,
        "archive_summary": archive_summary,
        "hash_summary": hash_summary,
        "file_records": file_records,
        "archive_records": archive_records,
        "hash_records": hash_records,
    }


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _file_record(path: Path, *, root: Path, digest: str) -> dict[str, Any]:
    extension = path.suffix.lower() or "[none]"
    category = _category_for_extension(extension)
    record: dict[str, Any] = {
        "record_type": "stage5ag_local_file_inventory_record",
        "stage_id": STAGE5AG_ID,
        "source_stage_id": STAGE5AG_SOURCE_STAGE_ID,
        "path": repo_relative(path),
        "source_root_relative_path": path.relative_to(root).as_posix(),
        "file_name": path.name,
        "extension": extension,
        "category": category,
        "size_bytes": path.stat().st_size,
        "sha256": digest,
        "mime_guess": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
        "metadata_only": True,
        "raw_content_included": False,
        "raw_file_committed": False,
        "solve_claim": False,
    }
    if category == "image":
        record.update(_image_metadata(path))
    return record


def _image_metadata(path: Path) -> dict[str, Any]:
    try:
        from PIL import Image
    except ImportError:
        return {"image_metadata_available": False}
    try:
        with Image.open(path) as image:
            return {
                "image_metadata_available": True,
                "image_format": image.format,
                "image_width": image.width,
                "image_height": image.height,
                "image_mode": image.mode,
            }
    except Exception:
        return {"image_metadata_available": False}


def _archive_record(path: Path, *, root: Path, digest: str) -> dict[str, Any]:
    extension = path.suffix.lower()
    base = {
        "record_type": "stage5ag_local_archive_inventory_record",
        "stage_id": STAGE5AG_ID,
        "source_stage_id": STAGE5AG_SOURCE_STAGE_ID,
        "source_id_candidate": _source_id_candidate_for_path(path),
        "path": repo_relative(path),
        "source_root_relative_path": path.relative_to(root).as_posix(),
        "sha256": digest,
        "size_bytes": path.stat().st_size,
        "archive_type": extension,
        "raw_extraction_performed": False,
        "raw_archive_content_committed": False,
        "solve_claim": False,
    }
    if extension == ".zip":
        try:
            with zipfile.ZipFile(path) as archive:
                infos = [info for info in archive.infolist() if not info.is_dir()]
            return {**base, **_archive_listing_summary([info.filename for info in infos], [info.file_size for info in infos]), "supported_for_listing": True, "inventory_status": "listed", "manual_action_required": False}
        except zipfile.BadZipFile:
            return {**base, **_empty_archive_listing(), "supported_for_listing": False, "inventory_status": "unsupported_or_corrupt_archive", "manual_action_required": True}
    if extension in {".tar", ".tgz"} or path.name.lower().endswith(".tar.gz"):
        try:
            with tarfile.open(path) as archive:
                members = [member for member in archive.getmembers() if member.isfile()]
            return {**base, **_archive_listing_summary([member.name for member in members], [member.size for member in members]), "supported_for_listing": True, "inventory_status": "listed", "manual_action_required": False}
        except tarfile.TarError:
            return {**base, **_empty_archive_listing(), "supported_for_listing": False, "inventory_status": "unsupported_or_corrupt_archive", "manual_action_required": True}
    if extension == ".gz":
        try:
            with gzip.open(path, "rb") as handle:
                handle.read(1)
            member_name = path.with_suffix("").name
            return {**base, **_archive_listing_summary([member_name], [0]), "supported_for_listing": True, "inventory_status": "single_gzip_member_not_extracted", "manual_action_required": False}
        except OSError:
            return {**base, **_empty_archive_listing(), "supported_for_listing": False, "inventory_status": "unsupported_or_corrupt_archive", "manual_action_required": True}
    return {**base, **_empty_archive_listing(), "supported_for_listing": False, "inventory_status": "unsupported_archive_type", "manual_action_required": True}


def _archive_listing_summary(names: list[str], sizes: list[int]) -> dict[str, Any]:
    top_levels = sorted({name.split("/", 1)[0] for name in names if name})
    extension_counts = Counter(Path(name).suffix.lower() or "[none]" for name in names)
    nested_archives = sum(1 for name in names if Path(name).suffix.lower() in ARCHIVE_EXTENSIONS)
    largest_members = sorted(
        ({"archive_member_path": name, "size_bytes": size} for name, size in zip(names, sizes)),
        key=lambda item: (-int(item["size_bytes"]), str(item["archive_member_path"])),
    )[:10]
    return {
        "member_count": len(names),
        "top_level_member_count": len(top_levels),
        "top_level_members": top_levels[:25],
        "extension_counts": _counter_to_dict(extension_counts),
        "nested_archive_count": nested_archives,
        "largest_members": largest_members,
    }


def _empty_archive_listing() -> dict[str, Any]:
    return {
        "member_count": 0,
        "top_level_member_count": 0,
        "top_level_members": [],
        "extension_counts": {},
        "nested_archive_count": 0,
        "largest_members": [],
    }


def _category_for_extension(extension: str) -> str:
    if extension in ARCHIVE_EXTENSIONS:
        return "archive"
    if extension in IMAGE_EXTENSIONS:
        return "image"
    if extension in PDF_EXTENSIONS:
        return "pdf"
    if extension in DOCX_EXTENSIONS:
        return "docx"
    if extension in HTML_EXTENSIONS:
        return "html"
    if extension in AUDIO_EXTENSIONS:
        return "audio"
    if extension in VIDEO_EXTENSIONS:
        return "video"
    if extension in TEXT_EXTENSIONS:
        return "text"
    return "other"


def _counter_to_dict(counter: Counter[str]) -> dict[str, int]:
    return {key: counter[key] for key in sorted(counter)}


def _largest_files(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"path": record["path"], "size_bytes": record["size_bytes"], "sha256": record["sha256"]}
        for record in sorted(records, key=lambda item: (-int(item["size_bytes"]), str(item["path"])))[:10]
    ]


def _top_level_entries(root: Path) -> list[dict[str, Any]]:
    if not root.exists():
        return []
    entries = []
    for item in sorted(root.iterdir(), key=lambda candidate: candidate.name.lower()):
        entries.append(
            {
                "path": repo_relative(item),
                "entry_name": item.name,
                "entry_type": "directory" if item.is_dir() else "file",
            }
        )
    return entries[:100]


def _duplicate_hash_groups(hash_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_hash: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in hash_records:
        by_hash[record["sha256"]].append(record)
    groups = []
    for digest, records in by_hash.items():
        if len(records) <= 1:
            continue
        groups.append(
            {
                "sha256": digest,
                "file_count": len(records),
                "paths": [record["path"] for record in sorted(records, key=lambda item: str(item["path"]))],
            }
        )
    return sorted(groups, key=lambda item: (-int(item["file_count"]), str(item["sha256"])))


def _source_id_candidate_for_path(path: Path) -> str | None:
    lower = path.as_posix().lower()
    if "diskcipherstuff" in lower:
        return "disk_cipher_theory_bundle_local"
    if "the-complete-cicada3301-archive" in lower:
        return "complete_cicada3301_archive"
    return None


def _raw_content_under_root_is_ignored(source_root: Path) -> bool:
    sentinel = (source_root / "__stage5ag_ignore_sentinel__.bin").as_posix()
    result = subprocess.run(["git", "check-ignore", "-q", sentinel], cwd=repo_root(), check=False)
    return result.returncode == 0


def _git_lines(*args: str) -> list[str]:
    result = subprocess.run(["git", *args], cwd=repo_root(), check=False, capture_output=True, text=True)
    if result.returncode not in {0, 1}:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _tracked_raw_files_present(source_root: Path) -> bool:
    allowed = {"readme.md", ".gitkeep"}
    prefix = source_root.as_posix().rstrip("/") + "/"
    return any(Path(line).name.lower() not in allowed for line in _git_lines("ls-files", prefix))


def _staged_raw_files_present(source_root: Path) -> bool:
    prefix = source_root.as_posix().rstrip("/") + "/"
    return any(line.startswith(prefix) for line in _git_lines("diff", "--cached", "--name-only"))


def _untracked_raw_files_present(source_root: Path) -> bool:
    prefix = source_root.as_posix().rstrip("/") + "/"
    return any(line.startswith("?? " + prefix) for line in _git_lines("status", "--short", prefix))


def _sort_key(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix().lower()
    except ValueError:
        return path.as_posix().lower()
