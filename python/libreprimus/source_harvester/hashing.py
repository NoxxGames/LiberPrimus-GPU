"""Hash and inventory helpers for local source-harvester paths."""

from __future__ import annotations

import hashlib
import mimetypes
import zipfile
from pathlib import Path
from typing import Any

from .export import repo_relative, resolve, write_inventory
from .models import STAGE_ID


def sha256_bytes(data: bytes) -> str:
    """Return the SHA-256 hex digest for bytes."""

    return hashlib.sha256(data).hexdigest()


def hash_file(path: Path, *, source_id: str | None = None) -> dict[str, Any]:
    """Hash a single file without modifying it."""

    target = resolve(path)
    data = target.read_bytes()
    return {
        "record_type": "hash_inventory_record",
        "schema": "schemas/source-harvester/hash-inventory-record-v0.schema.json",
        "stage_id": STAGE_ID,
        "source_id": source_id,
        "path": repo_relative(target),
        "file_name": target.name,
        "size_bytes": len(data),
        "sha256": sha256_bytes(data),
        "mime_guess": mimetypes.guess_type(target.name)[0] or "application/octet-stream",
        "raw_file_committed": False,
        "generated_outputs_committed": False,
        "solve_claim": False,
    }


def hash_path(path: Path, *, source_id: str | None = None) -> list[dict[str, Any]]:
    """Hash a file or all files under a directory deterministically."""

    target = resolve(path)
    if target.is_file():
        return [hash_file(target, source_id=source_id)]
    if not target.is_dir():
        raise ValueError(f"path is neither file nor directory: {path}")
    return [hash_file(item, source_id=source_id) for item in sorted(target.rglob("*")) if item.is_file()]


def write_hash_path(path: Path, *, out: Path, source_id: str | None = None) -> list[dict[str, Any]]:
    """Hash a local path and write JSONL/CSV inventory."""

    records = hash_path(path, source_id=source_id)
    write_inventory(out, records)
    return records


def inventory_archive(
    *,
    path: Path,
    source_id: str,
    out: Path,
) -> list[dict[str, Any]]:
    """Inventory a local zip archive or directory without extracting to committed paths."""

    target = resolve(path)
    if target.is_dir():
        records = _inventory_dir(target, source_id=source_id)
    elif zipfile.is_zipfile(target):
        records = _inventory_zip(target, source_id=source_id)
    elif target.is_file():
        records = [hash_file(target, source_id=source_id)]
    else:
        raise ValueError(f"archive path does not exist: {path}")
    write_inventory(out, records)
    return records


def _inventory_dir(path: Path, *, source_id: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for item in sorted(path.rglob("*")):
        if not item.is_file():
            continue
        record = hash_file(item, source_id=source_id)
        record["record_type"] = "file_inventory_record"
        record["schema"] = "schemas/source-harvester/file-inventory-record-v0.schema.json"
        record["archive_member_path"] = item.relative_to(path).as_posix()
        records.append(record)
    return records


def _inventory_zip(path: Path, *, source_id: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with zipfile.ZipFile(path) as archive:
        for info in sorted(archive.infolist(), key=lambda item: item.filename):
            if info.is_dir():
                continue
            data = archive.read(info.filename)
            records.append(
                {
                    "record_type": "file_inventory_record",
                    "schema": "schemas/source-harvester/file-inventory-record-v0.schema.json",
                    "stage_id": STAGE_ID,
                    "source_id": source_id,
                    "path": repo_relative(path),
                    "archive_member_path": info.filename,
                    "file_name": Path(info.filename).name,
                    "size_bytes": len(data),
                    "sha256": sha256_bytes(data),
                    "mime_guess": mimetypes.guess_type(info.filename)[0]
                    or "application/octet-stream",
                    "raw_file_committed": False,
                    "archive_extracted": False,
                    "generated_outputs_committed": False,
                    "solve_claim": False,
                }
            )
    return records
