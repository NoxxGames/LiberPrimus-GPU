from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def test_stage3w_agents_records_current_state() -> None:
    agents = (REPO / "AGENTS.md").read_text(encoding="utf-8").lower()

    assert "stage 3v" in agents
    assert "stage 3w" in agents
    assert "state consolidation" in agents
    assert "canonical corpus: inactive" in agents
    assert "page boundaries: reviewable" in agents
    assert "cuda: deferred" in agents


def test_stage3w_results_schema_not_only_planned() -> None:
    results_schema = (REPO / "RESULTS_SCHEMA.md").read_text(encoding="utf-8").lower()

    assert "planned, not finalized" not in results_schema
    assert "no result schema" not in results_schema
    assert "result-store records" in results_schema
    assert "generated outputs" in results_schema


def test_stage3w_source_of_truth_doc_exists() -> None:
    text = (REPO / "docs/architecture/project-state-and-source-of-truth.md").read_text(
        encoding="utf-8"
    )

    assert "Primary operational truth" in text
    assert "Anti-Drift Policy" in text
    assert "Stage 3V is complete" in text


def test_stage3w_deep_research_reports_are_ignored() -> None:
    gitignore = (REPO / ".gitignore").read_text(encoding="utf-8")

    assert "deep-research-reports/**" in gitignore


def test_stage3w_status_and_roadmap_point_to_stage3x_next() -> None:
    status = (REPO / "STATUS.md").read_text(encoding="utf-8")
    roadmap = (REPO / "ROADMAP.md").read_text(encoding="utf-8")
    readme = (REPO / "README.md").read_text(encoding="utf-8")

    assert "Stage 3W state consolidation" in status
    assert "Stage 3X" in roadmap
    assert "Stage 3X CLI modularisation" in readme
