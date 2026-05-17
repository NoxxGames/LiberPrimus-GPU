from __future__ import annotations

from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
README = REPO / "README.md"


def _readme() -> str:
    return README.read_text(encoding="utf-8")


def _section(text: str, heading: str, next_heading: str) -> str:
    return text.split(heading, maxsplit=1)[1].split(next_heading, maxsplit=1)[0]


def test_readme_boundary_section_replaces_stage0a_non_goals() -> None:
    readme = _readme()
    lines = readme.splitlines()

    assert "## Non-goals" not in lines
    assert "## Non-goals for Stage 0A" not in lines
    assert "## Current boundaries and deferred work" in lines
    assert "These are not permanent project exclusions" in readme
    assert "CUDA/search/scoring are deferred, not permanently excluded." in readme


def test_readme_boundary_subsections_are_explicit() -> None:
    section = _section(_readme(), "## Current boundaries and deferred work", "## Architecture summary")

    assert "### Permanent safety rules" in section
    assert "### Current boundaries" in section
    assert "### Deferred future work" in section
    assert "### Already implemented since Stage 0A" in section


def test_readme_rejects_stale_stage0a_boundary_phrases() -> None:
    readme = _readme()

    assert "No real corpus data is imported, transformed, or normalized." not in readme
    assert "No final Gematria rune table is frozen." not in readme


def test_readme_preserves_current_safety_and_boundary_language() -> None:
    readme = _readme()
    section = _section(readme, "## Current boundaries and deferred work", "## Architecture summary")

    assert "No generated output is a solve by itself." in section
    assert "No Liber Primus page is claimed solved" in section
    assert "still unsolved must not receive a solve claim" in section
    assert "Canonical corpus: inactive." in section
    assert "Unsolved-page search campaigns: not started." in section
    assert "Scoring campaigns: not started." in section
    assert "CUDA experiment campaigns: not started." in section
    assert "Search/scoring/CUDA campaigns: not started." in readme
    assert "Stage 2E: CPU exploratory experiment manifest scaffold and dry-run planner complete." in readme
    assert "Stage 2F: bounded CPU execution harness for synthetic and solved-fixture-only runs complete." in readme
    assert "Stage 2G: exploratory experiment proposal and human-approval workflow complete." in readme
    assert "Stage 2H: approval-gated execution path for approved synthetic/solved controls complete." in readme
    assert "Stage 2I first real bounded CPU exploratory experiment approval packet" in readme


def test_readme_does_not_imply_deferred_work_is_permanently_excluded() -> None:
    section = _section(_readme(), "## Current boundaries and deferred work", "## Architecture summary")
    lower_section = section.lower()

    assert "will never implement cuda" not in lower_section
    assert "will never implement search" not in lower_section
    assert "will never implement scoring" not in lower_section
    assert "Deferred future work" in section
    assert "CUDA/search/scoring are deferred, not permanently excluded." in section
    assert "CUDA kernels after CPU references and parity tests exist." in section


def test_remote_readme_verifier_scripts_exist_and_do_not_require_gh() -> None:
    ps1 = REPO / "scripts" / "ci" / "verify-remote-readme-status.ps1"
    sh = REPO / "scripts" / "ci" / "verify-remote-readme-status.sh"

    assert ps1.is_file()
    assert sh.is_file()
    assert "git show" in ps1.read_text(encoding="utf-8")
    assert "git show" in sh.read_text(encoding="utf-8")
    assert "gh " not in ps1.read_text(encoding="utf-8")
    assert "gh " not in sh.read_text(encoding="utf-8")


def test_readme_remains_multiline_markdown() -> None:
    assert len(_readme().splitlines()) > 50
