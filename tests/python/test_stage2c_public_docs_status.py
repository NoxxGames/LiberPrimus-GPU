from __future__ import annotations

from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
README = REPO / "README.md"
STATUS = REPO / "STATUS.md"
ROADMAP = REPO / "ROADMAP.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section(text: str, heading: str, next_heading: str) -> str:
    return text.split(heading, maxsplit=1)[1].split(next_heading, maxsplit=1)[0]


def test_public_docs_exist_and_are_multiline() -> None:
    for path, minimum in [(README, 50), (STATUS, 20), (ROADMAP, 20)]:
        assert path.is_file()
        assert len(_text(path).splitlines()) > minimum


def test_readme_current_status_is_current() -> None:
    readme = _text(README)
    current_status = _section(readme, "## Current status", "## CI status")
    assert "Stage 2A:" in current_status
    assert "complete" in current_status.lower()
    assert "Stage 2B:" in current_status
    assert "Stage 2C:" in current_status
    assert "10" in current_status and "Known solved baselines" in current_status
    assert "Canonical corpus: inactive" in current_status
    assert "Search/scoring/CUDA campaigns: not started" in current_status
    assert "Stage 2D" in current_status
    assert "Stage 2E" in current_status
    assert "Stage 2F" in current_status


def test_readme_top_level_status_is_not_stale() -> None:
    readme = _text(README)
    public_intro = readme.split("## Tutorials", maxsplit=1)[0]
    assert "Stage 2A should build" not in public_intro
    assert "Next milestone: Stage 2B" not in public_intro
    assert "Next milestones: Stage 2B" not in public_intro
    assert "Stage 2B is the next milestone" not in public_intro


def test_status_and_roadmap_are_current() -> None:
    status = _text(STATUS)
    roadmap = _text(ROADMAP)
    assert "Stage 2B added the experiment result-store foundation" in status
    assert "Stage 2C added GitHub Actions CI" in status
    assert "Stage 2D" in status
    assert "Stage 2E" in status
    assert "## Stage 2D - CI-gated schema and docs hardening" in roadmap
    assert "## Stage 2E - CPU experiment manifest scaffold and dry-run planner" in roadmap
    assert "## Stage 2F - Synthetic and solved-fixture CPU execution harness design" in roadmap
    assert "Stage 2A should build" not in roadmap
    assert "Stage 2B is the next milestone" not in roadmap
