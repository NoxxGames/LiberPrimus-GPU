from __future__ import annotations

from libreprimus.paths import repo_root


def _staged_plan_text() -> str:
    return (repo_root() / "docs/roadmap/staged-plan.md").read_text(encoding="utf-8").lower()


def test_stage3y_staged_plan_exists() -> None:
    assert (repo_root() / "docs/roadmap/staged-plan.md").is_file()


def test_stage3y_staged_plan_lists_stage3w_complete() -> None:
    text = _staged_plan_text()

    assert "stage 3w" in text
    assert "complete" in text


def test_stage3y_staged_plan_lists_stage3x_complete() -> None:
    text = _staged_plan_text()

    assert "stage 3x" in text
    assert "complete" in text


def test_stage3y_staged_plan_lists_stage3y_current() -> None:
    text = _staged_plan_text()

    assert "current stage" in text
    assert "stage 3y" in text


def test_stage3y_staged_plan_records_core_safety_state() -> None:
    text = _staged_plan_text()

    assert "cuda" in text and "deferred" in text
    assert "canonical corpus" in text and "inactive" in text
    assert "page boundaries" in text and "reviewable" in text
    assert "no solve claims" in text or "solve claims: none" in text


def test_stage3y_staged_plan_includes_deep_research_and_update_policy() -> None:
    text = _staged_plan_text()

    assert "deep research influence log" in text
    assert "update policy" in text
    assert "direction-change policy" in text
