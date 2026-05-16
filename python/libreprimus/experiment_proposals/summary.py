"""Load generated Stage 2G proposal review packet summaries."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_summary(results_dir: Path) -> dict[str, Any]:
    return json.loads((results_dir / "summary.json").read_text(encoding="utf-8"))


def load_review_packets(results_dir: Path) -> list[dict[str, Any]]:
    packets: list[dict[str, Any]] = []
    for path in sorted(results_dir.glob("*-review-packet.json")):
        packets.append(json.loads(path.read_text(encoding="utf-8")))
    return packets

