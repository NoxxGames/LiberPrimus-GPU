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
    assert "Broad search/scoring/CUDA campaigns: not started" in current_status
    assert "Stage 2D" in current_status
    assert "Stage 2E" in current_status
    assert "Stage 2F" in current_status
    assert "Stage 2G" in current_status
    assert "Stage 2H" in current_status
    assert "Stage 2I" in current_status
    assert "Stage 2J" in current_status
    assert "Stage 3A" in current_status
    assert "Stage 3B" in current_status
    assert "Stage 3C" in current_status
    assert "Stage 3D" in current_status
    assert "Stage 3E" in current_status
    assert "Stage 3F" in current_status


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
    assert "Stage 2F" in status
    assert "Stage 2G" in status
    assert "Stage 2H" in status
    assert "Stage 2I" in status
    assert "Stage 2J" in status
    assert "Stage 3A" in status
    assert "Stage 3B" in status
    assert "Stage 3C" in status
    assert "Stage 3D" in status
    assert "Stage 3E" in status
    assert "Stage 3F" in status
    assert "## Stage 2D - CI-gated schema and docs hardening" in roadmap
    assert "## Stage 2E - CPU experiment manifest scaffold and dry-run planner" in roadmap
    assert "## Stage 2F - Synthetic and solved-fixture CPU execution harness design" in roadmap
    assert "## Stage 2G - First bounded CPU exploratory experiment proposal" in roadmap
    assert "## Stage 2H - Approval-gated execution path" in roadmap
    assert "## Stage 2I - First real bounded CPU exploratory approval packet" in roadmap
    assert "## Stage 2J - Standing bounded auto-run policy" in roadmap
    assert "## Stage 3A - Minimal real bounded CPU execution/scoring scaffold" in roadmap
    assert "## Stage 3B - Inspect bounded leads and refine next queue item" in roadmap
    assert "## Stage 3C - Scoring calibration and null controls" in roadmap
    assert "## Stage 3D - Small Vigenere known-motif key-list preview" in roadmap
    assert "## Stage 3E - Method prioritization backlog" in roadmap
    assert "## Stage 3F - Evidence-key Vigenere pack executor" in roadmap
    assert "## Stage 3G - p56-local prime-minus-one offset sweep" in roadmap
    assert "Stage 2A should build" not in roadmap
    assert "Stage 2B is the next milestone" not in roadmap
