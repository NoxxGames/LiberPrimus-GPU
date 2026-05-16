"""Load generated Stage 2E dry-run summaries."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_summary(results_dir: Path) -> dict[str, Any]:
    path = results_dir / "summary.json"
    return json.loads(path.read_text(encoding="utf-8"))


def load_plan_records(results_dir: Path) -> list[dict[str, Any]]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(results_dir.glob("*-dry-run-plan.json"))
    ]
