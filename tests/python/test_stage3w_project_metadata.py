from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def test_stage3w_pyproject_description_is_current() -> None:
    pyproject = (REPO / "pyproject.toml").read_text(encoding="utf-8").lower()

    assert "stage 0a scaffold" not in pyproject
    assert "bounded cpu experiments" in pyproject
    assert "deferred cuda" in pyproject


def test_stage3w_docker_readme_is_not_stage0a_placeholder() -> None:
    docker_readme = (REPO / "docker/README.md").read_text(encoding="utf-8").lower()

    assert "stage 0a restrictions" not in docker_readme
    assert "no docker image is required for stage 0a" not in docker_readme
    assert "not the primary supported path" in docker_readme


def test_stage3w_ci_scripts_run_state_drift() -> None:
    ps1 = (REPO / "scripts/ci/run-consistency-checks.ps1").read_text(encoding="utf-8")
    sh = (REPO / "scripts/ci/run-consistency-checks.sh").read_text(encoding="utf-8")

    assert "consistency check-state-drift" in ps1
    assert "consistency check-state-drift" in sh


def test_stage3w_github_actions_use_node24_compatible_action_majors() -> None:
    workflow = (REPO / ".github/workflows/ci.yml").read_text(encoding="utf-8")

    assert "actions/checkout@v5" in workflow
    assert "actions/setup-python@v6" in workflow
