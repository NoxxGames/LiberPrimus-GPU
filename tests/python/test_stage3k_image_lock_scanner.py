from __future__ import annotations

import json
from pathlib import Path

from libreprimus.history.image_locks import scan_local_images, validate_image_locks
from libreprimus.image_analysis.primes import is_prime

REPO = Path(__file__).resolve().parents[2]
LOCKS = REPO / "data/locks/third-party/liber-primus-pages/liber-primus-page-image-locks-v0.jsonl"
ARTIFACTS = REPO / "data/observations/visual/liber-primus-page-image-artifacts-v0.jsonl"


def _png_bytes(width: int, height: int) -> bytes:
    return (
        b"\x89PNG\r\n\x1a\n"
        + b"\x00\x00\x00\r"
        + b"IHDR"
        + width.to_bytes(4, "big")
        + height.to_bytes(4, "big")
        + b"\x08\x02\x00\x00\x00"
        + b"\x00\x00\x00\x00"
    )


def test_synthetic_image_scan_records_dimensions_and_hash(tmp_path: Path) -> None:
    source = tmp_path / "images"
    source.mkdir()
    (source / "sample.png").write_bytes(_png_bytes(509, 503))
    locks = tmp_path / "locks.jsonl"
    artifacts = tmp_path / "artifacts.jsonl"
    summary = tmp_path / "summary.json"

    payload = scan_local_images(
        source_dir=source,
        lock_out=locks,
        artifact_out=artifacts,
        summary_out=summary,
    )

    artifact = json.loads(artifacts.read_text(encoding="utf-8").splitlines()[0])
    assert payload["image_count"] == 1
    assert artifact["width"] == 509
    assert artifact["height"] == 503
    assert artifact["both_dimensions_prime"] is True
    assert len(artifact["sha256"]) == 64


def test_prime_dimension_helper() -> None:
    assert is_prime(509)
    assert is_prime(503)
    assert not is_prime(510)


def test_image_scanner_handles_missing_dir_with_allow_missing(tmp_path: Path) -> None:
    payload = scan_local_images(
        source_dir=tmp_path / "missing",
        lock_out=tmp_path / "locks.jsonl",
        artifact_out=tmp_path / "artifacts.jsonl",
        summary_out=tmp_path / "summary.json",
        allow_missing=True,
    )

    assert payload["image_count"] == 0
    assert payload["warnings"] == ["source_dir_missing_scan_skipped"]


def test_committed_image_lock_records_validate_if_present() -> None:
    lock_count, artifact_count, errors = validate_image_locks(
        locks=LOCKS,
        artifacts=ARTIFACTS,
        allow_empty=True,
    )

    assert errors == []
    assert lock_count == artifact_count
