from pathlib import Path

import yaml


def test_stage5au_glyph_candidate_crops_are_deterministic_review_aids() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5au-crop-quality-diagnostics.yaml").read_text())
    first = payload["records"][0]
    assert payload["glyph_candidate_crop_count"] == 203
    assert first["challenge_id"] == "stage5at-token-case-001"
    assert first["glyph_candidate_bbox"] == {
        "x_min": 729,
        "y_min": 1232,
        "x_max": 958,
        "y_max": 1358,
        "width": 229,
        "height": 126,
    }
    assert first["glyph_candidate_status"] == "component_union"
    assert first["automatic_case_resolution_performed"] is False
