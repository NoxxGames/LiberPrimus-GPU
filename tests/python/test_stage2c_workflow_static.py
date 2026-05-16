from __future__ import annotations

from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
WORKFLOW = REPO / ".github" / "workflows" / "ci.yml"


def _workflow_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def test_ci_workflow_exists() -> None:
    assert WORKFLOW.is_file()


def test_ci_workflow_triggers_on_push_and_pull_request() -> None:
    text = _workflow_text()
    assert "push:" in text
    assert "pull_request:" in text
    assert "branches: [main]" in text


def test_ci_workflow_uses_python_312() -> None:
    assert 'python-version: "3.12"' in _workflow_text()


def test_ci_workflow_runs_ruff_and_pytest() -> None:
    text = _workflow_text()
    assert "python -m ruff check python/libreprimus tests/python" in text
    assert "python -m pytest -q tests/python" in text


def test_ci_workflow_validates_registry_and_manifests() -> None:
    text = _workflow_text()
    assert "transform-registry validate" in text
    assert "solved-baseline validate-manifest" in text
    assert "result-store validate-manifest" in text


def test_ci_workflow_does_not_enable_cuda_or_use_secrets_or_artifacts() -> None:
    text = _workflow_text().lower()
    assert "lpgpu_enable_cuda=on" not in text
    assert "setup-cuda" not in text
    assert "secrets." not in text
    assert "upload-artifact" not in text


def test_readme_top_status_is_not_stale() -> None:
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    current_status = readme.split("## Current status", maxsplit=1)[1].split("## Tutorials", maxsplit=1)[0]
    next_milestones = readme.split("## Next milestones", maxsplit=1)[1].split("## Stage 1B", maxsplit=1)[0]
    assert "Current status: Stage 1A" not in current_status
    assert "Stage 1A current status" not in current_status
    assert "Stage 1C next milestone" not in current_status
    assert "Stage 2A should build" not in next_milestones
    assert "Stage 2C" in current_status
    assert "Stage 2D" in next_milestones
