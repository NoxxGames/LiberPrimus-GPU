from pathlib import Path

import pytest

from libreprimus.result_store.models import (
    ExperimentArtifactRecord,
    ExperimentEventRecord,
    ExperimentRunRecord,
    ExperimentRunSummary,
)
from libreprimus.result_store.sqlite_sink import table_counts, write_sqlite_store


def sample_run(run_id: str = "run-1") -> ExperimentRunRecord:
    return ExperimentRunRecord(
        record_type="experiment_run_record",
        run_id=run_id,
        run_kind="solved_baseline",
        run_status="pass",
        manifest_id="manifest",
        manifest_sha256="a" * 64,
        registry_id="registry",
        registry_sha256="b" * 64,
        git_commit="abc",
        branch="main",
        created_at_utc="2026-05-16T00:00:00Z",
        completed_at_utc="2026-05-16T00:00:01Z",
        elapsed_ms=1.0,
        host={
            "os": "Windows",
            "platform": "Windows",
            "machine": "AMD64",
            "processor": "CPU",
            "python_version": "3.12.0",
        },
        tool_versions={},
        input_sources=[],
        profiles=[],
        corpus_candidate_id="rtkd-master-v0-candidate",
        canonical_corpus_active=False,
        page_boundaries_final=False,
        search_performed=False,
        scoring_used=False,
        cuda_used=False,
        gpu_required=False,
        random_seed=None,
        fixture_counts={"total": 1, "pass": 1, "fail": 0, "pending": 0, "skipped": 0},
        transform_counts={},
        output_artifacts=[],
        warnings=[],
        trusted_as_canonical=False,
        notes=[],
    )


def sample_event(run_id: str = "run-1") -> ExperimentEventRecord:
    return ExperimentEventRecord(
        record_type="experiment_event_record",
        run_id=run_id,
        event_index=0,
        timestamp_utc="2026-05-16T00:00:00Z",
        level="info",
        event_type="started",
        message="Started.",
        data={},
        trusted_as_canonical=False,
    )


def sample_artifact(run_id: str = "run-1") -> ExperimentArtifactRecord:
    return ExperimentArtifactRecord(
        record_type="experiment_artifact_record",
        run_id=run_id,
        artifact_id="artifact",
        artifact_kind="jsonl",
        path="experiments/results/result-store/stage2b/run_records.jsonl",
        sha256="c" * 64,
        size_bytes=1,
        committed=False,
        ignored_by_git=True,
        notes=[],
        trusted_as_canonical=False,
    )


def sample_summary() -> ExperimentRunSummary:
    return ExperimentRunSummary(
        record_type="experiment_run_summary",
        summary_id="summary",
        generated_at_utc="2026-05-16T00:00:00Z",
        run_count=1,
        pass_count=1,
        fail_count=0,
        partial_count=0,
        pending_count=0,
        skipped_count=0,
        error_count=0,
        run_kinds=["solved_baseline"],
        canonical_corpus_active_any=False,
        search_performed_any=False,
        scoring_used_any=False,
        cuda_used_any=False,
        generated_artifact_count=1,
        sqlite_database_path="results.sqlite3",
        jsonl_path="run_records.jsonl",
        warnings=[],
        trusted_as_canonical=False,
    )


def test_sqlite_sink_creates_required_tables_and_counts(tmp_path: Path) -> None:
    db = tmp_path / "results.sqlite3"

    write_sqlite_store(
        db,
        run_records=[sample_run()],
        event_records=[sample_event()],
        artifact_records=[sample_artifact()],
        summaries=[sample_summary()],
    )

    counts = table_counts(db)
    assert counts["schema_metadata"] >= 1
    assert counts["runs"] == 1
    assert counts["events"] == 1
    assert counts["artifacts"] == 1
    assert counts["summaries"] == 1


def test_sqlite_duplicate_run_fails_without_replace(tmp_path: Path) -> None:
    db = tmp_path / "results.sqlite3"
    write_sqlite_store(db, run_records=[sample_run()], event_records=[], artifact_records=[], summaries=[])

    with pytest.raises(ValueError):
        write_sqlite_store(db, run_records=[sample_run()], event_records=[], artifact_records=[], summaries=[])


def test_sqlite_duplicate_run_replaces_when_requested(tmp_path: Path) -> None:
    db = tmp_path / "results.sqlite3"
    write_sqlite_store(db, run_records=[sample_run()], event_records=[], artifact_records=[], summaries=[])
    write_sqlite_store(
        db,
        run_records=[sample_run()],
        event_records=[],
        artifact_records=[],
        summaries=[],
        replace=True,
    )

    assert table_counts(db)["runs"] == 1


def test_sqlite_required_false_flags_are_stored_false(tmp_path: Path) -> None:
    db = tmp_path / "results.sqlite3"
    write_sqlite_store(db, run_records=[sample_run()], event_records=[], artifact_records=[], summaries=[])

    import sqlite3

    with sqlite3.connect(db) as connection:
        row = connection.execute(
            "SELECT canonical_corpus_active, search_performed, scoring_used, cuda_used FROM runs"
        ).fetchone()
    assert row == (0, 0, 0, 0)
