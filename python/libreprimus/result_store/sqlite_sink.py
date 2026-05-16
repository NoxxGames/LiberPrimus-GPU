"""SQLite sink for generated experiment result-store records."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from libreprimus.result_store.schema_validation import validate_record

SQLITE_SCHEMA_ID = "sqlite-result-store-v0"

CREATE_TABLES = [
    """
    CREATE TABLE IF NOT EXISTS schema_metadata (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS runs (
        run_id TEXT PRIMARY KEY,
        run_kind TEXT NOT NULL,
        run_status TEXT NOT NULL,
        manifest_id TEXT NOT NULL,
        manifest_sha256 TEXT NOT NULL,
        registry_id TEXT NOT NULL,
        registry_sha256 TEXT NOT NULL,
        git_commit TEXT NOT NULL,
        created_at_utc TEXT NOT NULL,
        canonical_corpus_active INTEGER NOT NULL,
        search_performed INTEGER NOT NULL,
        scoring_used INTEGER NOT NULL,
        cuda_used INTEGER NOT NULL,
        payload TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS events (
        run_id TEXT NOT NULL,
        event_index INTEGER NOT NULL,
        timestamp_utc TEXT NOT NULL,
        level TEXT NOT NULL,
        event_type TEXT NOT NULL,
        payload TEXT NOT NULL,
        PRIMARY KEY (run_id, event_index),
        FOREIGN KEY (run_id) REFERENCES runs(run_id) ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS artifacts (
        run_id TEXT NOT NULL,
        artifact_id TEXT NOT NULL,
        artifact_kind TEXT NOT NULL,
        path TEXT NOT NULL,
        sha256 TEXT NOT NULL,
        committed INTEGER NOT NULL,
        ignored_by_git INTEGER NOT NULL,
        payload TEXT NOT NULL,
        PRIMARY KEY (run_id, artifact_id),
        FOREIGN KEY (run_id) REFERENCES runs(run_id) ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS summaries (
        summary_id TEXT PRIMARY KEY,
        generated_at_utc TEXT NOT NULL,
        run_count INTEGER NOT NULL,
        payload TEXT NOT NULL
    )
    """,
]


def connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys=ON")
    try:
        connection.execute("PRAGMA journal_mode=WAL")
    except sqlite3.DatabaseError:
        pass
    return connection


def initialize(connection: sqlite3.Connection) -> None:
    for statement in CREATE_TABLES:
        connection.execute(statement)
    connection.execute(
        "INSERT OR REPLACE INTO schema_metadata(key, value) VALUES (?, ?)",
        ("schema_id", SQLITE_SCHEMA_ID),
    )
    connection.commit()


def _payload(record: Any) -> dict[str, Any]:
    return validate_record(record)


def _dump(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, ensure_ascii=False)


def insert_run(connection: sqlite3.Connection, record: Any, *, replace: bool = False) -> None:
    payload = _payload(record)
    existing = connection.execute("SELECT 1 FROM runs WHERE run_id = ?", (payload["run_id"],)).fetchone()
    if existing and not replace:
        raise ValueError(f"Duplicate run_id in SQLite result store: {payload['run_id']}")
    if existing:
        connection.execute("DELETE FROM runs WHERE run_id = ?", (payload["run_id"],))
    connection.execute(
        """
        INSERT INTO runs(
            run_id, run_kind, run_status, manifest_id, manifest_sha256, registry_id,
            registry_sha256, git_commit, created_at_utc, canonical_corpus_active,
            search_performed, scoring_used, cuda_used, payload
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            payload["run_id"],
            payload["run_kind"],
            payload["run_status"],
            payload["manifest_id"],
            payload["manifest_sha256"],
            payload["registry_id"],
            payload["registry_sha256"],
            payload["git_commit"],
            payload["created_at_utc"],
            int(payload["canonical_corpus_active"]),
            int(payload["search_performed"]),
            int(payload["scoring_used"]),
            int(payload["cuda_used"]),
            _dump(payload),
        ),
    )


def insert_event(connection: sqlite3.Connection, record: Any) -> None:
    payload = _payload(record)
    connection.execute(
        """
        INSERT OR REPLACE INTO events(run_id, event_index, timestamp_utc, level, event_type, payload)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            payload["run_id"],
            payload["event_index"],
            payload["timestamp_utc"],
            payload["level"],
            payload["event_type"],
            _dump(payload),
        ),
    )


def insert_artifact(connection: sqlite3.Connection, record: Any) -> None:
    payload = _payload(record)
    connection.execute(
        """
        INSERT OR REPLACE INTO artifacts(
            run_id, artifact_id, artifact_kind, path, sha256, committed, ignored_by_git, payload
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            payload["run_id"],
            payload["artifact_id"],
            payload["artifact_kind"],
            payload["path"],
            payload["sha256"],
            int(payload["committed"]),
            int(payload["ignored_by_git"]),
            _dump(payload),
        ),
    )


def insert_summary(connection: sqlite3.Connection, record: Any, *, replace: bool = False) -> None:
    payload = _payload(record)
    if replace:
        connection.execute("DELETE FROM summaries WHERE summary_id = ?", (payload["summary_id"],))
    connection.execute(
        "INSERT INTO summaries(summary_id, generated_at_utc, run_count, payload) VALUES (?, ?, ?, ?)",
        (payload["summary_id"], payload["generated_at_utc"], payload["run_count"], _dump(payload)),
    )


def write_sqlite_store(
    path: Path,
    *,
    run_records: list[Any],
    event_records: list[Any],
    artifact_records: list[Any],
    summaries: list[Any],
    replace: bool = False,
) -> Path:
    with connect(path) as connection:
        initialize(connection)
        for run_record in run_records:
            insert_run(connection, run_record, replace=replace)
        for event_record in event_records:
            insert_event(connection, event_record)
        for artifact_record in artifact_records:
            insert_artifact(connection, artifact_record)
        for summary in summaries:
            insert_summary(connection, summary, replace=replace)
        connection.commit()
    return path


def table_counts(path: Path) -> dict[str, int]:
    with sqlite3.connect(path) as connection:
        return {
            table: int(connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
            for table in ["runs", "events", "artifacts", "summaries", "schema_metadata"]
        }
