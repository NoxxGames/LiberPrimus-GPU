"""Pure status-display helpers for Source Browser records."""

from __future__ import annotations

STATUS_UNSPECIFIED_LABEL = "unspecified"
STATUS_UNSPECIFIED_TOOLTIP = (
    "No source_status/status/ready_state/review_state field was present in the source record."
)
STATUS_LEGEND = (
    "Status values are read from source_status/status/ready_state/review_state. "
    "'unspecified' means no status field was present, not incomplete."
)


def display_status(source_status: str | None) -> str:
    return source_status or STATUS_UNSPECIFIED_LABEL
