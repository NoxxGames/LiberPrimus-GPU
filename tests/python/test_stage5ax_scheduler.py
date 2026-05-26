from __future__ import annotations

import sys

import pytest

from libreprimus.parallel_validation.models import ValidationCommand
from libreprimus.parallel_validation.scheduler import assert_parallel_safe, cap_workers


def test_parallel_safe_command_accepts_scheduler() -> None:
    command = ValidationCommand(
        command_id="safe",
        display_name="safe",
        command=[sys.executable, "-c", "print('ok')"],
        parallel_class="read_only_parallel_safe",
        requires_serial=False,
    )
    assert_parallel_safe(command)


def test_serial_command_rejected_by_scheduler() -> None:
    command = ValidationCommand(
        command_id="serial",
        display_name="serial",
        command=["git", "status"],
        parallel_class="serial_git_mutating",
        requires_serial=True,
    )
    with pytest.raises(ValueError):
        assert_parallel_safe(command)


def test_worker_cap_uses_policy_and_cpu_limit() -> None:
    assert cap_workers(32, 16, 64) == 16
    assert cap_workers(16, 16, 4) == 4
    assert cap_workers(None, 16, None) == 1
