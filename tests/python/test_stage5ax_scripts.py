from __future__ import annotations

from pathlib import Path


def test_parallel_validation_scripts_are_opt_in_and_use_cli() -> None:
    for relative in [
        "scripts/ci/run-parallel-validation.ps1",
        "scripts/ci/run-fast-validation.ps1",
        "scripts/ci/run-parallel-validation.sh",
        "scripts/ci/run-fast-validation.sh",
    ]:
        text = Path(relative).read_text(encoding="utf-8")
        assert "parallel-validation" in text
        assert "git add ." not in text
        assert "git push" not in text
