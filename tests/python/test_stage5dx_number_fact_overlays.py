from __future__ import annotations

from test_stage5dx_common import ensure_stage5dx_built, load_yaml


def test_stage5dx_overlay_collection_has_expected_visual_transform_cards() -> None:
    ensure_stage5dx_built()
    collection = load_yaml(
        "data/operator-console/source-browser/number-fact-overlays/"
        "stage5dx-review-batch-002-visual-transform-overlays.yaml"
    )
    labels = {overlay["display_label"] for overlay in collection["overlays"]}

    assert collection["overlay_count"] == 23
    assert any("zero-based GP index sum 155" in label for label in labels)
    assert any("Disk sequence 56311" in label and "word52/WAY" in label for label in labels)
    assert any("Visual/negative-space cluster" in label for label in labels)


def test_stage5dx_review_batch_records_no_source_rewrite_or_backfill() -> None:
    ensure_stage5dx_built()
    result = load_yaml(
        "data/operator-console/source-browser/number-fact-review-batches/"
        "stage5dx-review-batch-002-visual-transform-result.yaml"
    )

    assert result["reviewed_entry_count"] == 20
    assert result["overlay_count"] == 23
    assert result["overlays_added_now"] is True
    assert result["historical_source_lock_records_rewritten"] is False
    assert result["number_fact_backfill_performed_now"] is False
