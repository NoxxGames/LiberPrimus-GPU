"""Provenance capture for generated result-store records."""

from __future__ import annotations

import hashlib
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from libreprimus.paths import repo_root

PROFILE_PATHS = [
    ("gematria-primus-v0", Path("data/profiles/gematria/gematria-primus-v0.json")),
    ("rtkd-separator-grammar-v0", Path("data/profiles/separators/rtkd-separator-grammar-v0.json")),
    ("glyph-variants-v0", Path("data/profiles/glyph-variants/glyph-variants-v0.json")),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_output(args: list[str]) -> str:
    try:
        result = subprocess.run(["git", *args], check=True, capture_output=True, text=True, cwd=repo_root())
    except (OSError, subprocess.CalledProcessError):
        return "unknown"
    return result.stdout.strip()


def git_commit() -> str:
    return _git_output(["rev-parse", "HEAD"])


def git_branch() -> str:
    return _git_output(["branch", "--show-current"]) or "unknown"


def host_metadata() -> dict[str, str]:
    return {
        "os": platform.system(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": sys.version.split()[0],
    }


def tool_versions() -> dict[str, Any]:
    return {
        "python": sys.version.split()[0],
        "libreprimus_result_store": "stage2b-v0",
    }


def profile_metadata() -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for profile_id, relative_path in PROFILE_PATHS:
        path = repo_root() / relative_path
        if path.is_file():
            records.append(
                {
                    "profile_id": profile_id,
                    "path": str(relative_path).replace("\\", "/"),
                    "sha256": sha256_file(path),
                }
            )
    return records


def source_metadata(summary: dict[str, Any], manifest_payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "source_id": str(summary.get("manifest_id", manifest_payload.get("input_manifest_path", ""))),
            "source_kind": "solved_baseline_manifest_run",
            "sha256": summary.get("manifest_sha256"),
        },
        {
            "source_id": str(manifest_payload.get("input_manifest_path", "")),
            "source_kind": "solved_baseline_manifest",
            "sha256": manifest_payload.get("input_manifest_sha256"),
        },
    ]
