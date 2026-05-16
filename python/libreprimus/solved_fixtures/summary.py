"""Load solved-fixture reproduction summaries."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_summary(results_dir: Path) -> dict[str, Any]:
    return json.loads((results_dir / "summary.json").read_text(encoding="utf-8"))
