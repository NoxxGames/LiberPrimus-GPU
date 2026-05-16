"""Export helpers for consistency check summaries."""

from __future__ import annotations

import json
from pathlib import Path

from libreprimus.consistency.models import ConsistencyCheckSuiteResult


def write_summary(path: Path, suite: ConsistencyCheckSuiteResult) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(suite.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path
