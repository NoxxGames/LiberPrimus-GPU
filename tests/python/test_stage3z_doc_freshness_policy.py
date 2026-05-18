from __future__ import annotations

import os
import subprocess

from libreprimus.paths import repo_root


def test_stage3z_agents_requires_markdown_text_updates() -> None:
    text = (repo_root() / "AGENTS.md").read_text(encoding="utf-8").lower()

    assert ".md" in text
    assert ".txt" in text
    assert "staged-plan" in text


def test_stage3z_agents_requires_staged_plan_for_direction_changes() -> None:
    text = (repo_root() / "AGENTS.md").read_text(encoding="utf-8").lower()

    assert "direction change" in text
    assert "data/research/project-direction-change-records-v0.yaml" in text


def test_stage3z_tutorials_readme_links_onboarding_docs() -> None:
    text = (repo_root() / "tutorials/README.md").read_text(encoding="utf-8").lower()

    assert "../docs/onboarding/start-here.md" in text
    assert "../docs/onboarding/source-of-truth-map.md" in text


def test_stage3z_wiki_source_contains_onboarding_links() -> None:
    text = (repo_root() / "docs/wiki-source/Home.md").read_text(encoding="utf-8").lower()

    assert "project overview" in text
    assert "tutorial" in text


def test_stage3z_wiki_source_validation_passes() -> None:
    script = (
        "scripts/github/validate-wiki-source.ps1"
        if os.name == "nt"
        else "scripts/github/validate-wiki-source.sh"
    )
    command = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", script]
    if os.name != "nt":
        command = ["bash", script]

    result = subprocess.run(
        command,
        cwd=repo_root(),
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "wiki_source_valid=true" in result.stdout
