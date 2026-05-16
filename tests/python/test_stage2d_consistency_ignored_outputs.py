from __future__ import annotations

from libreprimus.consistency.check_ignored_outputs import check_ignored_output_consistency


def test_ignored_output_policy_passes() -> None:
    assert not [result for result in check_ignored_output_consistency() if result.is_failure]


def test_data_raw_is_ignored() -> None:
    results = check_ignored_output_consistency()

    assert any(
        result.check_name == "path_ignored" and "data/raw" in str(result.path)
        for result in results
    )


def test_generated_outputs_are_ignored() -> None:
    results = check_ignored_output_consistency()

    assert any("data/normalized" in str(result.path) for result in results if result.check_name == "path_ignored")
    assert any("experiments/results" in str(result.path) for result in results if result.check_name == "path_ignored")


def test_sqlite_db_is_ignored() -> None:
    results = check_ignored_output_consistency()

    assert any("sqlite3" in str(result.path) for result in results if result.check_name == "path_ignored")


def test_committed_inputs_are_trackable() -> None:
    results = check_ignored_output_consistency()
    trackable_paths = [str(result.path) for result in results if result.check_name == "path_trackable"]

    assert any("data/profiles" in path for path in trackable_paths)
    assert any("schemas/results" in path for path in trackable_paths)
    assert any("data/fixtures" in path for path in trackable_paths)
    assert any("experiments/manifests" in path for path in trackable_paths)
