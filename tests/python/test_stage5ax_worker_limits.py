from __future__ import annotations

from libreprimus.parallel_validation.plan import default_max_workers
from libreprimus.parallel_validation.pytest_runner import recommended_pytest_workers


def test_default_workers_never_exceed_sixteen() -> None:
    assert 1 <= default_max_workers() <= 16


def test_pytest_workers_are_capped() -> None:
    assert recommended_pytest_workers(64, 16) <= 16
