from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_parallel_validation_cli_build_plan_works_with_temp_outputs(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "libreprimus.cli",
            "parallel-validation",
            "build-stage5ax-plan",
            "--out-plan",
            str(tmp_path / "plan.yaml"),
            "--out-command-registry",
            str(tmp_path / "registry.yaml"),
            "--out-run-policy",
            str(tmp_path / "policy.yaml"),
            "--out-safety-audit",
            str(tmp_path / "safety.yaml"),
            "--out-pytest-shard-plan",
            str(tmp_path / "shards.yaml"),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert "parallel_safe_command_count=" in result.stdout
    assert (tmp_path / "plan.yaml").is_file()


def test_parallel_validation_summary_cli_works_from_committed_summary() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "libreprimus.cli", "parallel-validation", "summary"],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert "recommended_next_stage_title=Stage 5AY" in result.stdout
