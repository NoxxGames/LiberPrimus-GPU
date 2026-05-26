from __future__ import annotations

from pathlib import Path

from libreprimus.parallel_validation.pytest_runner import build_shards, discover_test_files, shard_plan_record


def test_pytest_sharding_is_deterministic_and_covers_once(tmp_path: Path) -> None:
    test_root = tmp_path / "tests"
    test_root.mkdir()
    for index in range(17):
        (test_root / f"test_{index:02d}.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")

    files = discover_test_files(test_root)
    first = build_shards(files, 16)
    second = build_shards(files, 16)
    assert first == second
    flattened = [path for shard in first for path in shard]
    assert sorted(flattened) == files
    assert len(flattened) == len(set(flattened))


def test_pytest_shard_plan_supports_sixteen_workers(tmp_path: Path) -> None:
    test_root = tmp_path / "tests"
    test_root.mkdir()
    for index in range(20):
        (test_root / f"test_{index:02d}.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")
    plan = shard_plan_record(test_root, 16)
    assert plan["requested_workers"] == 16
    assert plan["all_tests_covered_once"] is True
    assert plan["shard_count"] == 16
