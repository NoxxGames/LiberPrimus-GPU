"""Network and hash helpers for Stage 4K source-lock snapshots."""

from __future__ import annotations

from datetime import UTC, datetime
import hashlib
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from libreprimus.source_lock_snapshots.models import FetchResult

MAX_FETCH_BYTES = 1024 * 1024


def utc_now() -> str:
    """Return a stable UTC timestamp string for records."""

    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def hash_bytes(data: bytes) -> str:
    """Return the SHA-256 hex digest for bytes."""

    return hashlib.sha256(data).hexdigest()


def safe_cache_name(record_id: str, url: str) -> str:
    """Return a deterministic ignored-cache filename."""

    suffix = ".html" if ".fandom.com/" in url else ".txt"
    return f"{quote(record_id, safe='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_')}{suffix}"


def fetch_to_ignored_cache(
    *,
    url: str,
    cache_dir: Path,
    record_id: str,
    allow_network: bool,
    max_bytes: int = MAX_FETCH_BYTES,
) -> FetchResult:
    """Fetch a small public text/HTML source into the ignored cache when allowed."""

    if not allow_network:
        return FetchResult(retrieval_status="network_disabled")
    cache_dir.mkdir(parents=True, exist_ok=True)
    try:
        request = Request(url, headers={"User-Agent": "liberprimus-gpu-stage4k-source-lock/1.0"})
        with urlopen(request, timeout=20) as response:  # noqa: S310 - allowlisted public URLs only.
            data = response.read(max_bytes + 1)
            if len(data) > max_bytes:
                return FetchResult(
                    retrieval_status="fetch_failed",
                    http_status=getattr(response, "status", None),
                    content_type=response.headers.get("content-type"),
                    error="content_exceeds_stage4k_fetch_cap",
                )
            cache_path = cache_dir / safe_cache_name(record_id, url)
            cache_path.write_bytes(data)
            return FetchResult(
                retrieval_status="fetched",
                http_status=getattr(response, "status", None),
                content_type=response.headers.get("content-type"),
                content_length=len(data),
                content_sha256=hash_bytes(data),
                ignored_cache_path=cache_path.as_posix(),
                fetched=True,
            )
    except HTTPError as error:
        return FetchResult(
            retrieval_status="fetch_failed",
            http_status=error.code,
            content_type=error.headers.get("content-type") if error.headers else None,
            error=str(error),
        )
    except (OSError, URLError, TimeoutError) as error:
        return FetchResult(retrieval_status="fetch_failed", error=str(error))
