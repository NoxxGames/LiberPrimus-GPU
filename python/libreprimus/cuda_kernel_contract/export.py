"""Export helpers for Stage 5E CUDA kernel contract records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.benchmark_planning.export import write_json, write_jsonl, write_yaml
from libreprimus.cuda_kernel_contract.models import WARNINGS_REPORT


def write_records_yaml(path: Path, records: list[dict[str, Any]]) -> None:
    write_yaml(path, {"records": records})


def write_record_yaml(path: Path, record: dict[str, Any]) -> None:
    write_yaml(path, record)


def write_report(path: Path, payload: Any) -> None:
    write_json(path, payload)


def write_warnings(out_dir: Path, warnings: list[dict[str, Any]]) -> None:
    write_jsonl(out_dir / WARNINGS_REPORT, warnings)
