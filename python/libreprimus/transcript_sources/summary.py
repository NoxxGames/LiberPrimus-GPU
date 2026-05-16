"""Summary loaders for transcript sources."""

from __future__ import annotations

from pathlib import Path

from libreprimus.transcript_sources.models import (
    Scream314ReferenceSummary,
    TranscriptSourceSummary,
)
from libreprimus.transcript_sources.rtkd_master import parse_rtkd_master
from libreprimus.transcript_sources.scream314_reference import parse_scream314_reference


def load_summary(source: str, path: Path) -> TranscriptSourceSummary | Scream314ReferenceSummary:
    """Load one transcript-source summary by source selector."""
    if source == "rtkd-master":
        _, summary = parse_rtkd_master(path)
        return summary
    if source == "scream314":
        _, summary = parse_scream314_reference(path)
        return summary
    raise ValueError(f"Unsupported transcript source: {source}")
