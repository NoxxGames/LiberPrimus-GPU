"""Summaries for Stage 3Y research-synthesis records."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from libreprimus.research_synthesis.loader import load_all_record_sets
from libreprimus.research_synthesis.models import DEFAULT_DATA_DIR


def build_summary(data_dir: Path = DEFAULT_DATA_DIR) -> dict[str, Any]:
    """Build a compact summary of research-synthesis records."""

    records = load_all_record_sets(data_dir)
    method_statuses = Counter(
        str(record.get("status")) for record in records.get("method_families", [])
    )
    retirement_statuses = Counter(
        str(record.get("retired_status")) for record in records.get("method_retirements", [])
    )
    return {
        "data_dir": str(data_dir),
        "stage_summary_count": len(records.get("stage_summaries", [])),
        "method_family_count": len(records.get("method_families", [])),
        "retirement_count": len(records.get("method_retirements", [])),
        "deep_research_influence_count": len(records.get("deep_research_influences", [])),
        "direction_change_count": len(records.get("direction_changes", [])),
        "method_status_counts": dict(sorted(method_statuses.items())),
        "retirement_status_counts": dict(sorted(retirement_statuses.items())),
    }
