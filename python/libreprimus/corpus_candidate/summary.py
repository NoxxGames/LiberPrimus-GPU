"""Summary loading for generated corpus candidates."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_summary(candidate_dir: Path) -> dict[str, Any]:
    return json.loads((candidate_dir / "summary.json").read_text(encoding="utf-8"))
