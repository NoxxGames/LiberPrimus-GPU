from __future__ import annotations

from pathlib import Path

import pytest
import yaml


REPO = Path(__file__).resolve().parents[2]
WORKFLOW = REPO / ".github" / "workflows" / "ci.yml"


def _workflow_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def _workflow_yaml() -> dict[str, object]:
    payload = yaml.load(_workflow_text(), Loader=yaml.BaseLoader)
    assert isinstance(payload, dict)
    return payload


def _assert_readable_workflow_text(text: str) -> None:
    lines = text.splitlines()
    assert len(lines) > 25
    assert len(lines) > 1
    assert "name: CI on:" not in lines[0]
    assert max(len(line) for line in lines) < 180


def test_ci_workflow_exists() -> None:
    assert WORKFLOW.is_file()


def test_ci_workflow_is_readable_multiline_yaml() -> None:
    text = _workflow_text()
    _assert_readable_workflow_text(text)
    assert len(text.splitlines()) == WORKFLOW.read_text(encoding="utf-8").count("\n")


def test_minified_workflow_sample_is_rejected() -> None:
    sample = "name: CI on: push: branches: [main] pull_request: branches: [main]\n"
    with pytest.raises(AssertionError):
        _assert_readable_workflow_text(sample)


def test_ci_workflow_yaml_parses_and_has_expected_top_level_keys() -> None:
    payload = _workflow_yaml()
    assert payload["name"] == "CI"
    assert payload["permissions"] == {"contents": "read"}
    assert "concurrency" in payload
    assert "jobs" in payload


def test_ci_workflow_triggers_on_push_and_pull_request() -> None:
    triggers = _workflow_yaml()["on"]
    assert isinstance(triggers, dict)
    assert triggers["push"] == {"branches": ["main"]}
    assert triggers["pull_request"] == {"branches": ["main"]}


def test_ci_workflow_uses_python_312() -> None:
    jobs = _workflow_yaml()["jobs"]
    assert isinstance(jobs, dict)
    python_job = jobs["python-ci"]
    assert isinstance(python_job, dict)
    steps = python_job["steps"]
    assert isinstance(steps, list)
    assert any(isinstance(step, dict) and step.get("with", {}).get("python-version") == "3.12" for step in steps)


def test_ci_workflow_runs_ruff_and_pytest() -> None:
    text = _workflow_text()
    assert "python -m ruff check python/libreprimus tests/python" in text
    assert "python -m pytest -q tests/python" in text


def test_ci_workflow_validates_registry_and_manifests() -> None:
    text = _workflow_text()
    assert "verify-lock-hashes.sh" in text
    assert "transform-registry validate" in text
    assert "solved-baseline validate-manifest" in text
    assert "result-store validate-manifest" in text


def test_ci_workflow_jobs_are_present() -> None:
    jobs = _workflow_yaml()["jobs"]
    assert isinstance(jobs, dict)
    assert "python-ci" in jobs
    assert "cmake-cpu-smoke" in jobs


def test_ci_workflow_is_raw_data_free() -> None:
    text = _workflow_text().lower()
    assert "data/raw" not in text
    assert "liberprimus-research-report.md" not in text


def test_ci_workflow_has_no_generated_result_uploads() -> None:
    text = _workflow_text().lower()
    assert "upload-artifact" not in text
    assert "data/normalized" not in text


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
    assert "Stage 2D" in current_status
    assert "Stage 2E" in current_status
    assert "Stage 2F" in current_status
    assert "Stage 2G" in current_status
    assert "Stage 2H" in current_status
    assert "Stage 2I" in current_status
    assert "Stage 2J" in current_status
    assert "Stage 3A" in next_milestones
