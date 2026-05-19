"""Load and validate CPU batch manifests."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import yaml

from libreprimus.cpu_batch.models import CpuBatchManifest
from libreprimus.cpu_batch.validation import validate_manifest_payload
from libreprimus.history.source_records import resolve_repo_path


def manifest_sha256(path: Path) -> str:
    """Return the SHA-256 digest for a manifest file."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_manifest(path: Path) -> CpuBatchManifest:
    """Load a CPU batch manifest and validate its policy guardrails."""

    resolved = resolve_repo_path(path)
    payload = yaml.safe_load(resolved.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"CPU batch manifest must be a mapping: {resolved}")
    errors = validate_manifest_payload(payload)
    if errors:
        raise ValueError("; ".join(errors))
    return CpuBatchManifest(payload=dict(payload), path=resolved, manifest_sha256=manifest_sha256(resolved))


def load_manifest_payload(path: Path) -> dict[str, Any]:
    """Load only the YAML payload for tests and validation commands."""

    return load_manifest(path).payload
