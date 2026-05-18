"""Summary helpers for Stage 3R Discord lead promotion."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.discord_lead_promotion.export import read_json, read_yaml
from libreprimus.paths import repo_root


def load_summary(audit_summary: Path, manifest_dir: Path | None = None) -> dict[str, Any]:
    resolved = _resolve(audit_summary)
    if resolved.is_file():
        summary = read_yaml(resolved)
    else:
        generated = repo_root() / "experiments/results/discord-lead-promotion/stage3r/promotion_summary.json"
        if generated.is_file():
            summary = read_json(generated)
        else:
            raise FileNotFoundError(resolved)
    if manifest_dir is not None:
        resolved_manifest_dir = _resolve(manifest_dir)
        summary["manifest_files_present"] = len(list(resolved_manifest_dir.glob("EXP-3R-*.yaml")))
    return summary


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path
