from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ae_doc_staleness_record_requires_strict_check() -> None:
    record = yaml.safe_load(Path("data/cuda/stage5ae-corrected-bounded-p56-doc-staleness-validation.yaml").read_text())["records"][0]
    assert record["strict_doc_staleness_check_expected"] is True
    assert record["stale_stage5ad_pass_language_allowed"] is False
    assert record["doc_staleness_validation_status"] == "strict_check_required_and_passed_locally"
