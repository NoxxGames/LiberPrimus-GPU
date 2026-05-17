"""Summary loading and derivation for deterministic image-analysis outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.paths import repo_root


def load_summary(results_dir: Path) -> dict[str, Any]:
    path = _resolve(results_dir) / "summary.json"
    if not path.is_file():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def summarize_for_research(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "image_count": summary.get("image_count", 0),
        "threshold_values": summary.get("threshold_values", []),
        "component_record_count": summary.get("component_record_count", 0),
        "symmetry_record_count": summary.get("symmetry_record_count", 0),
        "bitplane_record_count": summary.get("bitplane_record_count", 0),
        "feature_candidate_count": summary.get("feature_candidate_count", 0),
        "feature_counts": summary.get("feature_counts", {}),
        "top_symmetric_image_ids": summary.get("top_symmetric_image_ids", []),
        "top_asymmetric_image_ids": summary.get("top_asymmetric_image_ids", []),
        "top_sparse_dot_like_image_ids": summary.get("top_sparse_dot_like_image_ids", []),
    }


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path
