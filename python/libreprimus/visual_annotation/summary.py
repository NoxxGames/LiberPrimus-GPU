"""Summary helpers for Stage 4C visual annotation records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.visual_annotation.loaders import load_yaml_payload


def summarize_visual_annotation(summary_path: Path) -> dict[str, Any]:
    """Load the committed Stage 4C annotation summary."""

    return load_yaml_payload(summary_path)
