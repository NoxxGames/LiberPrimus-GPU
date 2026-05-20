"""Small export helpers for Stage 5A CUDA planning."""

from __future__ import annotations

from pathlib import Path

from libreprimus.benchmark_planning.export import resolve_repo_path
from libreprimus.cuda_planning.models import STAGE5A_OUTPUT_DIR, WARNINGS_JSONL


def write_empty_warnings(out_dir: Path = STAGE5A_OUTPUT_DIR) -> None:
    path = resolve_repo_path(out_dir) / WARNINGS_JSONL
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("", encoding="utf-8")
