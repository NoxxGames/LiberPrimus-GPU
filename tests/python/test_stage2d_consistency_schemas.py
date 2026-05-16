from __future__ import annotations

import json
from pathlib import Path

from libreprimus.consistency.check_schemas import check_schema_consistency


def _write_schema(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def test_current_schemas_pass() -> None:
    assert not [result for result in check_schema_consistency() if result.is_failure]


def test_duplicate_schema_id_fails(tmp_path: Path) -> None:
    payload = {"$id": "duplicate", "title": "Duplicate", "type": "object"}
    _write_schema(tmp_path / "one.schema.json", payload)
    _write_schema(tmp_path / "two.schema.json", payload)
    doc = tmp_path / "RESULTS_SCHEMA.md"
    doc.write_text("experiment-run-record-v0 experiment-run-summary-v0 solved-page-fixture solved-baseline-run-manifest-v0")

    failures = check_schema_consistency(tmp_path, results_schema_doc=doc)

    assert any(result.check_name == "schema_metadata_unique" for result in failures if result.is_failure)


def test_missing_expected_schema_fails(tmp_path: Path) -> None:
    _write_schema(tmp_path / "only.schema.json", {"type": "object"})
    doc = tmp_path / "RESULTS_SCHEMA.md"
    doc.write_text("experiment-run-record-v0 experiment-run-summary-v0 solved-page-fixture solved-baseline-run-manifest-v0")

    failures = check_schema_consistency(tmp_path, results_schema_doc=doc)

    assert any(result.check_name == "expected_schema_exists" for result in failures if result.is_failure)


def test_trusted_as_canonical_true_allowance_fails(tmp_path: Path) -> None:
    _write_schema(
        tmp_path / "results/experiment-run-record-v0.schema.json",
        {
            "type": "object",
            "properties": {
                "record_type": {"const": "experiment_run_record"},
                "trusted_as_canonical": {"const": True},
            },
        },
    )
    doc = tmp_path / "RESULTS_SCHEMA.md"
    doc.write_text("experiment-run-record-v0 experiment-run-summary-v0 solved-page-fixture solved-baseline-run-manifest-v0")

    failures = check_schema_consistency(tmp_path, results_schema_doc=doc)

    assert any(result.check_name == "trusted_as_canonical_false" for result in failures if result.is_failure)
