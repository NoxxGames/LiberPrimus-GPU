from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _record(path: str) -> dict[str, Any]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"][0]


def test_doc_staleness_validation_consumes_stage5ab_records() -> None:
    record = _record("data/cuda/stage5ac-prime-minus-one-cuda-synthetic-doc-staleness-validation.yaml")
    assert record["source_stage_id"] == "stage-5ab"
    assert record["doc_staleness_source_of_truth"] == "data/project-state/stage5ab-doc-staleness-source-of-truth.yaml"
    assert record["operational_file_map"] == "data/project-state/operational-file-map.yaml"
    assert record["doc_staleness_strict_check_passed"] is True
    assert record["stale_findings_after_repair"] == 0
    assert record["next_stage_expected_prefix"] == "Stage 5AD"


def test_operational_docs_use_stage5au_latest_and_stage5av_next() -> None:
    status = Path("STATUS.md").read_text(encoding="utf-8")
    staged_plan = Path("docs/roadmap/staged-plan.md").read_text(encoding="utf-8")
    assert "Stage 5AU token case-review pack usability fix" in status
    assert "Next recommended prompt: Stage 5AV" in status
    assert "Latest completed stage: Stage 5AU" in staged_plan
    assert "Current planning focus: Stage 5AV" in staged_plan
