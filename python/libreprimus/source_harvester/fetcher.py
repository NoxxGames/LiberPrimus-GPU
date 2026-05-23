"""Opt-in network fetch support for user-run source harvesting."""

from __future__ import annotations

import json
import time
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .export import write_jsonl
from .hashing import hash_file
from .manifest import manifest_records
from .models import DOWNLOAD_CAPTURE_MODES, FAILURES_REPORT
from .policy import require_safe_output_root


def fetch_source(
    *,
    manifest_path: Path,
    source_id: str,
    out_root: Path,
    allow_network: bool = False,
    allow_downloads: bool = False,
    rate_limit_seconds: float = 3.0,
) -> dict[str, Any]:
    """Fetch one source when explicitly allowed by a user-run CLI invocation."""

    if not allow_network:
        raise ValueError("network fetch requires --allow-network")
    if rate_limit_seconds <= 0:
        raise ValueError("rate_limit_seconds must be positive")
    require_safe_output_root(out_root)
    records = {record["source_id"]: record for record in manifest_records(manifest_path)}
    if source_id not in records:
        raise ValueError(f"unknown source_id: {source_id}")
    record = records[source_id]
    if not record.get("allow_network_fetch"):
        raise ValueError(f"source does not allow direct network fetch: {source_id}")
    if _requires_download(record) and not allow_downloads:
        raise ValueError("download-like capture modes require --allow-downloads")
    url = record.get("url")
    if not url:
        raise ValueError(f"source has no URL for network fetch: {source_id}")

    time.sleep(rate_limit_seconds)
    request = urllib.request.Request(url, headers={"User-Agent": "LiberPrimusGPU-SourceHarvester/0.1"})
    target_root = out_root if out_root.is_absolute() else Path.cwd() / out_root
    raw_dir = target_root / source_id / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    parsed = urlparse(url)
    suffix = Path(parsed.path).suffix or ".bin"
    raw_path = raw_dir / f"{source_id}{suffix}"
    try:
        with urllib.request.urlopen(request, timeout=30) as response:  # noqa: S310 - opt-in CLI.
            raw_path.write_bytes(response.read())
            status = getattr(response, "status", None)
            content_type = response.headers.get("content-type")
    except Exception as exc:
        failure = {
            "source_id": source_id,
            "url": url,
            "failure_type": "fetch_failed",
            "error": str(exc),
            "retrieved_at": datetime.now(UTC).isoformat(),
        }
        write_jsonl(target_root / FAILURES_REPORT, [failure])
        raise
    hash_record = hash_file(raw_path, source_id=source_id)
    metadata = {
        "source_id": source_id,
        "url": url,
        "retrieved_at": datetime.now(UTC).isoformat(),
        "http_status": status,
        "content_type": content_type,
        "local_raw_path": raw_path.as_posix(),
        "sha256": hash_record["sha256"],
        "size_bytes": hash_record["size_bytes"],
        "raw_file_committed": False,
        "solve_claim": False,
    }
    (target_root / source_id / "fetch_metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return metadata


def _requires_download(record: dict[str, Any]) -> bool:
    return bool(set(record.get("recommended_capture_modes", [])).intersection(DOWNLOAD_CAPTURE_MODES))
