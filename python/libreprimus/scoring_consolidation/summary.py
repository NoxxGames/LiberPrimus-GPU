"""Summary helpers for Stage 4I scoring records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.paths import repo_root
from libreprimus.scoring_consolidation.models import (
    CALIBRATION_PROFILE_PATH,
    CALIBRATION_REPORT_PATH,
    COMPATIBILITY_MAP_PATH,
    CONFIDENCE_LABELS_PATH,
    DEFAULT_DATA_DIR,
    SCORER_RECORDS_PATH,
)


def load_summary(data_dir: Path = DEFAULT_DATA_DIR) -> dict[str, Any]:
    """Load committed scoring records and return report counts."""

    resolved = data_dir if data_dir.is_absolute() else repo_root() / data_dir
    scorers = _records(resolved / SCORER_RECORDS_PATH)
    labels = _records(resolved / CONFIDENCE_LABELS_PATH)
    mappings = _records(resolved / COMPATIBILITY_MAP_PATH)
    profiles = _records(resolved / CALIBRATION_PROFILE_PATH)
    reports = _records(resolved / CALIBRATION_REPORT_PATH)
    report = reports[0] if reports else {}
    return {
        "scorer_record_count": len(scorers),
        "confidence_label_count": len(labels),
        "compatibility_mapping_count": len(mappings),
        "calibration_profile_count": len(profiles),
        "positive_controls_available": bool(report.get("positive_controls_available")),
        "null_controls_available": bool(report.get("null_controls_available")),
        "negative_controls_available": bool(report.get("negative_controls_available")),
        "known_noisy_family_count": len(report.get("known_noisy_families", [])),
        "known_negative_or_deprioritised_family_count": len(report.get("known_negative_or_deprioritised_families", [])),
        "solve_claim": False,
        "cuda_used": False,
    }


def _records(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict) and isinstance(payload.get("records"), list):
        return [dict(item) for item in payload["records"] if isinstance(item, dict)]
    return []
