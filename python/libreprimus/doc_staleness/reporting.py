"""Stage 5AH report writing helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_json_report(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_warnings(path: Path, warnings: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps({"warning": warning}, sort_keys=True) + "\n" for warning in warnings),
        encoding="utf-8",
    )
