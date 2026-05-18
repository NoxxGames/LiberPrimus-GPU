from __future__ import annotations

from libreprimus.paths import repo_root


def test_stage3y_agents_mentions_staged_plan_update_policy() -> None:
    text = (repo_root() / "AGENTS.md").read_text(encoding="utf-8").lower()

    assert "docs/roadmap/staged-plan.md" in text
    assert ".md" in text and ".txt" in text
    assert "method family" in text


def test_stage3y_document_freshness_policy_exists() -> None:
    text = (repo_root() / "docs/architecture/project-document-freshness-policy.md").read_text(
        encoding="utf-8"
    ).lower()

    assert "stage status" in text
    assert "roadmap" in text
    assert "docs/roadmap/staged-plan.md" in text


def test_stage3y_roadmap_links_staged_plan() -> None:
    text = (repo_root() / "ROADMAP.md").read_text(encoding="utf-8")

    assert "docs/roadmap/staged-plan.md" in text
