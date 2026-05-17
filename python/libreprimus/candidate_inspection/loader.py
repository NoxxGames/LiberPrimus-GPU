"""Load ignored bounded candidate outputs for local inspection."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.paths import repo_root


def resolve_results_dir(results_dir: Path) -> Path:
    return results_dir if results_dir.is_absolute() else repo_root() / results_dir


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return payload


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        if not isinstance(payload, dict):
            raise ValueError(f"Expected JSONL object in {path}")
        records.append(payload)
    return records


def load_candidate_records(results_dir: Path) -> list[dict[str, Any]]:
    resolved = resolve_results_dir(results_dir)
    return load_jsonl(resolved / "candidate_records.jsonl")


def load_top_candidates(results_dir: Path) -> list[dict[str, Any]]:
    resolved = resolve_results_dir(results_dir)
    return load_jsonl(resolved / "top_candidates.jsonl")


def load_run_summary(results_dir: Path) -> dict[str, Any]:
    resolved = resolve_results_dir(results_dir)
    return load_json(resolved / "summary.json")


def load_stage_outputs(results_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    return load_candidate_records(results_dir), load_top_candidates(results_dir), load_run_summary(results_dir)
