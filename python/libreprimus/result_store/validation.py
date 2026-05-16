"""Validation helpers for generated result stores."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from libreprimus.paths import repo_root
from libreprimus.result_store.import_solved_baseline import load_result_store_manifest
from libreprimus.result_store.jsonl_sink import read_jsonl
from libreprimus.result_store.provenance import sha256_file
from libreprimus.result_store.schema_validation import validate_record
from libreprimus.result_store.sqlite_sink import table_counts

REQUIRED_SQLITE_TABLES = {"schema_metadata", "runs", "events", "artifacts", "summaries"}


def validate_result_store_manifest_file(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        manifest = load_result_store_manifest(path)
    except (OSError, ValueError) as exc:
        return [str(exc)]
    input_manifest = repo_root() / manifest.input_manifest_path
    if not input_manifest.is_file():
        errors.append(f"Input manifest missing: {input_manifest}")
    elif sha256_file(input_manifest) != manifest.input_manifest_sha256:
        errors.append("Input manifest SHA-256 mismatch.")
    return errors


def _validate_jsonl(path: Path) -> tuple[list[dict], list[str]]:
    records = read_jsonl(path)
    errors: list[str] = []
    for index, record in enumerate(records):
        try:
            validate_record(record)
        except Exception as exc:  # noqa: BLE001 - validation errors are collected for CLI display.
            errors.append(f"{path.name}:{index}: {exc}")
    return records, errors


def _validate_summary(path: Path) -> tuple[dict, list[str]]:
    if not path.is_file():
        return {}, [f"Missing summary file: {path}"]
    summary = json.loads(path.read_text(encoding="utf-8"))
    try:
        validate_record(summary)
    except Exception as exc:  # noqa: BLE001
        return summary, [f"summary.json: {exc}"]
    return summary, []


def _sqlite_tables(path: Path) -> set[str]:
    with sqlite3.connect(path) as connection:
        rows = connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    return {str(row[0]) for row in rows}


def validate_result_store(results_dir: Path, sqlite_path: Path) -> list[str]:
    errors: list[str] = []
    run_records, run_errors = _validate_jsonl(results_dir / "run_records.jsonl")
    event_records, event_errors = _validate_jsonl(results_dir / "event_records.jsonl")
    artifact_records, artifact_errors = _validate_jsonl(results_dir / "artifact_records.jsonl")
    summary, summary_errors = _validate_summary(results_dir / "summary.json")
    errors.extend(run_errors + event_errors + artifact_errors + summary_errors)
    for record in run_records:
        if record.get("canonical_corpus_active") is not False:
            errors.append(f"{record.get('run_id')}: canonical_corpus_active must be false.")
        if record.get("search_performed") is not False:
            errors.append(f"{record.get('run_id')}: search_performed must be false.")
        if record.get("scoring_used") is not False:
            errors.append(f"{record.get('run_id')}: scoring_used must be false.")
        if record.get("cuda_used") is not False:
            errors.append(f"{record.get('run_id')}: cuda_used must be false.")
    for record in artifact_records:
        if record.get("committed") is not False:
            errors.append(f"{record.get('artifact_id')}: committed must be false.")
        if record.get("ignored_by_git") is not True:
            errors.append(f"{record.get('artifact_id')}: ignored_by_git must be true.")
    if not sqlite_path.is_file():
        errors.append(f"Missing SQLite database: {sqlite_path}")
        return errors
    tables = _sqlite_tables(sqlite_path)
    missing_tables = REQUIRED_SQLITE_TABLES - tables
    if missing_tables:
        errors.append(f"SQLite missing tables: {sorted(missing_tables)}")
    counts = table_counts(sqlite_path)
    if counts.get("runs") != len(run_records):
        errors.append("SQLite run count does not match JSONL run count.")
    if counts.get("events") != len(event_records):
        errors.append("SQLite event count does not match JSONL event count.")
    if counts.get("artifacts") != len(artifact_records):
        errors.append("SQLite artifact count does not match JSONL artifact count.")
    with sqlite3.connect(sqlite_path) as connection:
        unsafe = connection.execute(
            "SELECT COUNT(*) FROM runs WHERE canonical_corpus_active != 0 OR search_performed != 0 "
            "OR scoring_used != 0 OR cuda_used != 0"
        ).fetchone()[0]
    if int(unsafe):
        errors.append("SQLite contains a run with unsafe canonical/search/scoring/CUDA flags.")
    if summary and summary.get("run_count") != len(run_records):
        errors.append("Summary run count does not match JSONL run count.")
    return errors
