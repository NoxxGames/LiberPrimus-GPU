from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _records(path: str) -> list[dict[str, Any]]:
    return list(yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"])


def test_stage5ad_doc_staleness_validation_is_clean_and_stage_aware() -> None:
    record = _records("data/cuda/stage5ad-bounded-p56-cuda-doc-staleness-validation.yaml")[0]

    assert record["latest_stage_context"] == "stage-5ad"
    assert record["doc_staleness_strict_check_passed"] is True
    assert record["stale_findings_after_repair"] == 0
    assert record["stage5ab_source_of_truth_consumed"] is True
    assert record["website_expansion_status"] == "deferred_future_unnumbered_project"
