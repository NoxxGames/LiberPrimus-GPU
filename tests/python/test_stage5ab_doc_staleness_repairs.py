from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.doc_staleness.repairs import repair_summary_record
from libreprimus.doc_staleness.scanner import scan_repository


def test_stage5ab_current_operational_docs_have_no_staleness_findings() -> None:
    scan = scan_repository(source_of_truth_path=Path("data/project-state/stage5ah-doc-staleness-source-of-truth.yaml"))

    assert scan.finding_count == 0
    assert len(scan.scanned_paths) >= 24
    assert "README.md" in scan.scanned_paths


def test_stage5ab_readme_repaired_stale_examples() -> None:
    text = Path("README.md").read_text(encoding="utf-8")

    assert "Website expansion is deferred to Stage 6" not in text
    assert "Stage 5M" not in "\n".join(
        line for line in text.splitlines() if "Existing CUDA code" in line
    )
    assert "Stage 5AE corrected formula-parity reporting" in text
    assert "Stage 5AH" in text
    assert "Stage 5AI" in text


def test_stage5ab_repair_summary_helper_is_deterministic() -> None:
    record = repair_summary_record(before_count=16, after_count=0, repaired_paths=["b.md", "a.md"])

    assert record["before_finding_count"] == 16
    assert record["after_finding_count"] == 0
    assert record["repaired_paths"] == ["a.md", "b.md"]


def test_stage5ab_summary_records_no_cuda_or_solve_work() -> None:
    summary = yaml.safe_load(
        Path("data/project-state/stage5ab-doc-staleness-summary.yaml").read_text(encoding="utf-8")
    )

    assert summary["cuda_execution_performed"] is False
    assert summary["cuda_source_modified"] is False
    assert summary["new_cuda_kernels_added"] == 0
    assert summary["benchmark_performed"] is False
    assert summary["scored_experiments_executed"] is False
    assert summary["solve_claim"] is False


def test_stage5ab_tutorial_wiki_mirrors_are_synchronized() -> None:
    pairs = [
        ("tutorials/10-hardware-and-performance.md", "docs/wiki-source/10 Hardware And Performance.md"),
        ("tutorials/14-codex-assisted-development.md", "docs/wiki-source/14 Codex Assisted Development.md"),
        ("tutorials/15-troubleshooting.md", "docs/wiki-source/15 Troubleshooting.md"),
    ]
    for tutorial_path, wiki_path in pairs:
        tutorial = Path(tutorial_path).read_text(encoding="utf-8").strip()
        wiki = Path(wiki_path).read_text(encoding="utf-8")
        wiki_body = wiki.split("\n\n", 1)[1].strip()
        assert wiki_body == tutorial
