"""Local page image source-lock scanning and validation."""

from __future__ import annotations

from datetime import UTC, datetime
import hashlib
import json
from pathlib import Path
from typing import Any

from libreprimus.image_analysis.basic_metadata import read_image_metadata
from libreprimus.image_analysis.primes import is_prime
from libreprimus.paths import repo_root

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}
SOURCE_ID = "local-liber-primus-pages-stage3k"


def resolve_repo_path(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def scan_local_images(
    *,
    source_dir: Path,
    lock_out: Path,
    artifact_out: Path,
    summary_out: Path | None = None,
    allow_missing: bool = False,
) -> dict[str, Any]:
    """Scan local images and write committed lock/artifact records plus optional summary."""
    resolved_source = resolve_repo_path(source_dir)
    resolved_lock = resolve_repo_path(lock_out)
    resolved_artifact = resolve_repo_path(artifact_out)
    resolved_summary = resolve_repo_path(summary_out) if summary_out is not None else None
    warnings: list[str] = []
    image_paths: list[Path] = []
    if resolved_source.is_dir():
        image_paths = sorted(
            path
            for path in resolved_source.rglob("*")
            if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
        )
    elif allow_missing:
        warnings.append("source_dir_missing_scan_skipped")
    else:
        raise FileNotFoundError(resolved_source)

    created_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    lock_records: list[dict[str, Any]] = []
    artifact_records: list[dict[str, Any]] = []
    total_bytes = 0
    prime_dimension_count = 0
    for path in image_paths:
        relative_path = _display_path(path)
        data = path.read_bytes()
        sha256 = hashlib.sha256(data).hexdigest()
        total_bytes += len(data)
        metadata = read_image_metadata(path)
        width_prime = is_prime(metadata.width)
        height_prime = is_prime(metadata.height)
        both_prime = width_prime and height_prime
        if both_prime:
            prime_dimension_count += 1
        image_id = f"liber-primus-page-image-{path.stem}"
        media_type = "image/jpeg" if path.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
        lock_records.append(
            {
                "record_type": "source_lock_record",
                "source_id": SOURCE_ID,
                "local_path": relative_path,
                "relative_path": relative_path,
                "file_name": path.name,
                "file_size_bytes": len(data),
                "sha256": sha256,
                "media_type": media_type,
                "created_at_utc": created_at,
                "source_class": "secondary_archive",
                "trusted_as_canonical": False,
                "review_status": "machine_checked",
                "notes": "Local third-party image lock; raw image remains ignored.",
            }
        )
        artifact_records.append(
            {
                "record_type": "image_artifact_record",
                "image_id": image_id,
                "source_id": SOURCE_ID,
                "relative_path": relative_path,
                "file_name": path.name,
                "file_size_bytes": len(data),
                "sha256": sha256,
                "image_format": metadata.image_format,
                "width": metadata.width,
                "height": metadata.height,
                "width_is_prime": width_prime,
                "height_is_prime": height_prime,
                "both_dimensions_prime": both_prime,
                "color_mode": metadata.color_mode,
                "trusted_as_canonical": False,
                "review_status": "machine_checked",
                "notes": "Deterministic image metadata only; no OCR or image-derived seed execution.",
            }
        )

    _write_jsonl(resolved_lock, lock_records)
    _write_jsonl(resolved_artifact, artifact_records)
    summary = {
        "record_type": "image_analysis_summary",
        "summary_id": "stage3k-local-liber-primus-page-image-scan",
        "generated_at_utc": created_at,
        "source_dir": str(source_dir).replace("\\", "/"),
        "image_count": len(image_paths),
        "lock_record_count": len(lock_records),
        "image_artifact_record_count": len(artifact_records),
        "total_bytes": total_bytes,
        "prime_dimension_count": prime_dimension_count,
        "warnings": warnings,
        "trusted_as_canonical": False,
        "notes": "Generated Stage 3K scan summary; output path remains ignored.",
    }
    if resolved_summary is not None:
        resolved_summary.parent.mkdir(parents=True, exist_ok=True)
        resolved_summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def validate_image_locks(
    *,
    locks: Path,
    artifacts: Path,
    allow_empty: bool = False,
) -> tuple[int, int, list[str]]:
    lock_records = _read_jsonl(resolve_repo_path(locks))
    artifact_records = _read_jsonl(resolve_repo_path(artifacts))
    errors: list[str] = []
    if not allow_empty and not lock_records:
        errors.append("lock records are empty")
    if len(lock_records) != len(artifact_records):
        errors.append("lock/artifact record counts differ")
    lock_hashes = {record.get("sha256") for record in lock_records}
    artifact_hashes = {record.get("sha256") for record in artifact_records}
    if lock_hashes != artifact_hashes:
        errors.append("lock/artifact hashes differ")
    for record in lock_records:
        if record.get("record_type") != "source_lock_record":
            errors.append(f"{record.get('file_name', '<unknown>')}: invalid lock record_type")
        if record.get("trusted_as_canonical") is not False:
            errors.append(f"{record.get('file_name', '<unknown>')}: lock must be noncanonical")
    for record in artifact_records:
        if record.get("record_type") != "image_artifact_record":
            errors.append(f"{record.get('file_name', '<unknown>')}: invalid artifact record_type")
        if record.get("trusted_as_canonical") is not False:
            errors.append(f"{record.get('file_name', '<unknown>')}: artifact must be noncanonical")
        width = int(record.get("width", 0))
        height = int(record.get("height", 0))
        if record.get("both_dimensions_prime") != (is_prime(width) and is_prime(height)):
            errors.append(f"{record.get('file_name', '<unknown>')}: prime dimension flag mismatch")
    return len(lock_records), len(artifact_records), errors


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records), encoding="utf-8")


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(repo_root()).as_posix()
    except ValueError:
        return path.as_posix()
