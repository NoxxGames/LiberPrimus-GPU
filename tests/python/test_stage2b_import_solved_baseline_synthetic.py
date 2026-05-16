import json
import sqlite3
from pathlib import Path

import yaml

from libreprimus.result_store.import_solved_baseline import import_solved_baseline
from libreprimus.result_store.jsonl_sink import read_jsonl
from libreprimus.result_store.provenance import sha256_file
from libreprimus.result_store.summary import load_summary
from libreprimus.result_store.validation import validate_result_store


def write_synthetic_solved_baseline(tmp_path: Path) -> tuple[Path, Path, Path]:
    solved_dir = tmp_path / "solved"
    solved_dir.mkdir()
    summary = {
        "record_type": "solved_baseline_manifest_run_summary",
        "manifest_id": "synthetic-stage2a",
        "manifest_sha256": "a" * 64,
        "registry_id": "cpu-reference-transforms-v0",
        "registry_sha256": "b" * 64,
        "fixture_count": 4,
        "pass_count": 4,
        "fail_count": 0,
        "pending_count": 0,
        "skipped_count": 0,
        "direct_translation_pass_count": 1,
        "atbash_family_pass_count": 1,
        "vigenere_pass_count": 1,
        "prime_stream_pass_count": 1,
        "search_performed_any": False,
        "cuda_used_any": False,
        "scoring_used_any": False,
        "elapsed_ms": 1.25,
        "warnings": [],
    }
    records = [
        {
            "record_type": "solved_baseline_manifest_run_record",
            "fixture_id": "fixture",
            "match_status": "pass",
        }
    ]
    (solved_dir / "summary.json").write_text(json.dumps(summary), encoding="utf-8")
    (solved_dir / "manifest_run_records.jsonl").write_text(
        "\n".join(json.dumps(record) for record in records) + "\n",
        encoding="utf-8",
    )
    (solved_dir / "warnings.jsonl").write_text("", encoding="utf-8")
    input_manifest = tmp_path / "stage2a.yaml"
    input_manifest.write_text(
        yaml.safe_dump({"manifest_id": "synthetic-stage2a", "corpus_candidate_id": "synthetic-candidate"}),
        encoding="utf-8",
    )
    result_manifest = tmp_path / "result-store.yaml"
    result_manifest.write_text(
        yaml.safe_dump(
            {
                "record_type": "experiment_result_store_manifest",
                "manifest_id": "synthetic-result-store",
                "manifest_version": "result-store-v0",
                "description": "Synthetic import.",
                "input_manifest_path": str(input_manifest),
                "input_manifest_sha256": sha256_file(input_manifest),
                "output_dir": str(tmp_path / "out"),
                "jsonl_output_path": str(tmp_path / "out" / "run_records.jsonl"),
                "sqlite_output_path": str(tmp_path / "out" / "results.sqlite3"),
                "import_sources": [
                    str(solved_dir / "summary.json"),
                    str(solved_dir / "manifest_run_records.jsonl"),
                    str(solved_dir / "warnings.jsonl"),
                ],
                "canonical_corpus_active": False,
                "page_boundaries_final": False,
                "search_enabled": False,
                "scoring_enabled": False,
                "cuda_enabled": False,
                "expected_run_kind": "solved_baseline",
                "notes": [],
            }
        ),
        encoding="utf-8",
    )
    return result_manifest, solved_dir, tmp_path / "out"


def test_import_synthetic_solved_baseline_outputs_jsonl_sqlite_and_summary(tmp_path: Path) -> None:
    manifest, solved_dir, out_dir = write_synthetic_solved_baseline(tmp_path)

    result = import_solved_baseline(manifest, solved_baseline_results=solved_dir, out_dir=out_dir)

    assert result["summary"].pass_count == 1
    assert (out_dir / "run_records.jsonl").is_file()
    assert (out_dir / "artifact_records.jsonl").is_file()
    assert (out_dir / "event_records.jsonl").is_file()
    assert (out_dir / "summary.json").is_file()
    assert (out_dir / "results.sqlite3").is_file()
    assert validate_result_store(out_dir, out_dir / "results.sqlite3") == []


def test_import_counts_and_false_flags_match_input(tmp_path: Path) -> None:
    manifest, solved_dir, out_dir = write_synthetic_solved_baseline(tmp_path)
    import_solved_baseline(manifest, solved_baseline_results=solved_dir, out_dir=out_dir)

    run = read_jsonl(out_dir / "run_records.jsonl")[0]
    artifacts = read_jsonl(out_dir / "artifact_records.jsonl")
    summary = load_summary(out_dir)

    assert run["fixture_counts"] == {"total": 4, "pass": 4, "fail": 0, "pending": 0, "skipped": 0}
    assert run["search_performed"] is False
    assert run["cuda_used"] is False
    assert run["scoring_used"] is False
    assert all(artifact["committed"] is False and artifact["ignored_by_git"] is True for artifact in artifacts)
    assert summary["run_count"] == 1
    with sqlite3.connect(out_dir / "results.sqlite3") as connection:
        assert connection.execute("SELECT COUNT(*) FROM runs").fetchone()[0] == 1
