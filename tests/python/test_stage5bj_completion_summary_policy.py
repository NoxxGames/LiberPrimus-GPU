import subprocess

from test_stage5bj_crosswalk_closure import ROOT, load_yaml


def test_completion_summary_paths_are_local_only_and_ignored() -> None:
    summary = load_yaml("data/project-state/stage5bj-summary.yaml")
    paths = summary["completion_summary_local_paths"]

    assert "codex_output/stage5bj-completion-summary.md" in paths
    assert "codex-output/stage5bj-completion-summary.md" in paths
    for path in paths:
        result = subprocess.run(
            ["git", "check-ignore", "-q", path],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, path


def test_generated_stage5bj_outputs_are_ignored() -> None:
    for path in [
        "experiments/results/historical-route/stage5bj/summary.json",
        "experiments/results/historical-route/stage5bj/extracted-surfaces/stage5bj-lock-2014-1033-512-hex.hex",
    ]:
        result = subprocess.run(
            ["git", "check-ignore", "-q", path],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, path
