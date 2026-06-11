from __future__ import annotations

from pathlib import Path

from libreprimus.parallel_validation.pytest_runner import build_shards, pytest_file_weight
from test_stage5ea_common import ensure_stage5ea_built, load_yaml


def test_pytest_shard_policy_preserves_eight_worker_cap_and_weights() -> None:
    ensure_stage5ea_built()

    record = load_yaml("data/project-state/stage5ea-pytest-shard-policy-repair.yaml")
    files = [
        Path("tests/python/test_stage5ea_cli.py"),
        Path("tests/python/test_stage5ea_source_browser_performance.py"),
        Path("tests/python/test_small_a.py"),
        Path("tests/python/test_small_b.py"),
    ]
    shards = build_shards(files, 2)

    assert record["worker_cap"] == 8
    assert record["old_16_worker_default_reintroduced"] is False
    assert record["historical_slow_tests_are_weighted_or_serial_isolated"] is True
    assert pytest_file_weight(Path("tests/python/test_stage5ea_cli.py")) == 4
    assert len(shards) == 2
