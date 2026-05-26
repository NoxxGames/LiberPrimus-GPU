import subprocess
from pathlib import Path


def test_stage5ay_generated_outputs_and_codex_output_are_ignored() -> None:
    for path in [
        "experiments/results/token-block/stage5ay/preflight_design_report.json",
        "experiments/results/token-block/stage5ay/branch_budget_report.json",
        "codex-output/stage5ay-codex-completion.md",
    ]:
        result = subprocess.run(["git", "check-ignore", "-q", path], cwd=Path.cwd(), check=False)
        assert result.returncode == 0
