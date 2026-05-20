"""Export helpers for Stage 5C CUDA build/device records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import resolve_repo_path, write_json, write_yaml
from libreprimus.cuda_build.models import STAGE5C_OUTPUT_DIR, WARNINGS_JSONL


def write_record_set(path: Path, records: list[dict[str, Any]]) -> None:
    """Write a committed YAML record set."""

    write_yaml(path, {"records": records})


def write_report(out_dir: Path, filename: str, payload: Any) -> None:
    """Write an ignored generated JSON report."""

    write_json(resolve_repo_path(out_dir) / filename, payload)


def write_empty_warnings(out_dir: Path = STAGE5C_OUTPUT_DIR) -> None:
    """Ensure the ignored warnings file exists."""

    path = resolve_repo_path(out_dir) / WARNINGS_JSONL
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("", encoding="utf-8")
