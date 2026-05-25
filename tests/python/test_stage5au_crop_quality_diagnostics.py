from pathlib import Path

import yaml


def test_stage5au_crop_quality_diagnostics_cover_every_case_challenge() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5au-crop-quality-diagnostics.yaml").read_text())
    assert payload["diagnostic_count"] == 203
    assert len(payload["records"]) == 203
    assert payload["quality_status_counts"] == {"usable_with_context": 123, "good_for_review": 80}
    assert payload["fallback_count"] == 0
    assert payload["unusable_count"] == 0
    assert all(record["manual_review_required"] for record in payload["records"])
