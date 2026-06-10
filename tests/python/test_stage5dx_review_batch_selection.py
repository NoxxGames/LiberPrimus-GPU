from __future__ import annotations

from pathlib import Path

from test_stage5dx_common import ensure_stage5dx_built, load_yaml


def test_stage5dx_selected_batch_has_exactly_twenty_existing_entries() -> None:
    ensure_stage5dx_built()
    result = load_yaml(
        "data/operator-console/source-browser/number-fact-review-batches/"
        "stage5dx-review-batch-002-visual-transform-result.yaml"
    )
    selected = result["selected_source_record_paths"]

    assert result["review_batch_id"] == "number_fact_review_batch_002_visual_transform"
    assert result["review_scope"] == "selected_20_source_records_only"
    assert len(selected) == 20
    assert all(Path(path).exists() for path in selected)


def test_stage5dx_entry_status_marks_review_only_rows() -> None:
    ensure_stage5dx_built()
    status = load_yaml(
        "data/operator-console/source-browser/number-fact-review-batches/"
        "stage5dx-review-batch-002-entry-status.yaml"
    )

    assert len(status["entries"]) == 20
    for entry in status["entries"]:
        assert entry["review_status"] == "reviewed_overlay_added"
        assert entry["entry_historical_source_lock_rewritten"] is False
        assert entry["usable_for_decision_now"] is False
        assert {"proof", "route_seed", "execution_seed", "solve_claim"} <= set(entry["not_allowed_as"])
