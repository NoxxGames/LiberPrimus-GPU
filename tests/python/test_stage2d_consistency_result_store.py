from __future__ import annotations

import json
from pathlib import Path

from libreprimus.consistency.check_result_store import check_result_store_consistency
from libreprimus.result_store.import_solved_baseline import import_solved_baseline
from test_stage2b_import_solved_baseline_synthetic import write_synthetic_solved_baseline


def test_stage2b_manifest_passes() -> None:
    failures = [
        result
        for result in check_result_store_consistency()
        if result.check_name == "manifest_valid" and result.is_failure
    ]

    assert failures == []


def test_absent_generated_outputs_skip_with_warning(tmp_path: Path) -> None:
    manifest, _, _ = write_synthetic_solved_baseline(tmp_path)
    results = check_result_store_consistency(
        manifest,
        results_dir=tmp_path / "missing",
        sqlite_path=tmp_path / "missing" / "results.sqlite3",
        allow_missing_generated=True,
    )

    assert any(result.check_name == "generated_outputs_optional" and result.is_warning for result in results)


def test_synthetic_generated_output_validates(tmp_path: Path) -> None:
    manifest, solved_dir, out_dir = write_synthetic_solved_baseline(tmp_path)
    import_solved_baseline(manifest, solved_baseline_results=solved_dir, out_dir=out_dir)

    results = check_result_store_consistency(
        manifest,
        results_dir=out_dir,
        sqlite_path=out_dir / "results.sqlite3",
    )

    assert not [result for result in results if result.is_failure]


def test_synthetic_generated_output_false_flags_are_checked(tmp_path: Path) -> None:
    manifest, solved_dir, out_dir = write_synthetic_solved_baseline(tmp_path)
    import_solved_baseline(manifest, solved_baseline_results=solved_dir, out_dir=out_dir)
    run_path = out_dir / "run_records.jsonl"
    run = json.loads(run_path.read_text(encoding="utf-8").splitlines()[0])
    run["search_performed"] = True
    run_path.write_text(json.dumps(run) + "\n", encoding="utf-8")

    results = check_result_store_consistency(
        manifest,
        results_dir=out_dir,
        sqlite_path=out_dir / "results.sqlite3",
    )

    assert any(result.check_name == "generated_outputs_valid" for result in results if result.is_failure)


def test_sqlite_path_ignored() -> None:
    results = check_result_store_consistency()

    assert any(result.check_name == "sqlite_path_ignored" and not result.is_failure for result in results)
