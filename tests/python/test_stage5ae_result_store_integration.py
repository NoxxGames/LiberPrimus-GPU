from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ae_result_store_integration_is_compact_metadata_only() -> None:
    record = yaml.safe_load(Path("data/cuda/stage5ae-corrected-bounded-p56-result-store-integration.yaml").read_text())["records"][0]
    assert record["result_store_contract"] == "stage4p_unified_result_surface"
    assert record["integration_status"] == "compact_summary_only"
    assert record["generated_result_body_committed"] is False
    assert record["generated_body_publication_allowed"] is False
