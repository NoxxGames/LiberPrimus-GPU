from __future__ import annotations

import sys

from libreprimus.parallel_validation.models import ValidationCommand
from libreprimus.parallel_validation.subprocess_runner import run_command


def test_subprocess_runner_writes_separated_logs(tmp_path) -> None:
    command = ValidationCommand(
        command_id="log-test",
        display_name="log test",
        command=[sys.executable, "-c", "import sys; print('out'); print('err', file=sys.stderr)"],
        parallel_class="read_only_parallel_safe",
        requires_serial=False,
    )
    result = run_command(command, repo_root=tmp_path, log_dir=tmp_path / "logs")
    assert result.passed
    assert "out" in (tmp_path / "logs/log-test.stdout.log").read_text(encoding="utf-8")
    assert "err" in (tmp_path / "logs/log-test.stderr.log").read_text(encoding="utf-8")
