from __future__ import annotations

from pathlib import Path

from test_stage5ed_common import ensure_stage5ed_built, load_yaml


def test_stage5ed_selected_batch_has_exactly_twenty_existing_entries() -> None:
    ensure_stage5ed_built()
    result = load_yaml(
        "data/operator-console/source-browser/number-fact-review-batches/"
        "stage5ed-review-batch-004-disk-visual-method-result.yaml"
    )
    selected = result["selected_source_record_paths"]

    assert result["review_batch_id"] == "number_fact_review_batch_004_disk_visual_method"
    assert result["review_scope"] == "selected_20_source_records_only"
    assert len(selected) == 20
    assert selected[0] == "data/historical-route/stage5dn-disk-alberti-branch-cipher-candidate-v1.yaml"
    assert selected[-1] == "data/historical-route/stage5di-magic-square-matrix-route-context.yaml"
    assert all(Path(path).exists() for path in selected)


def test_stage5ed_review_batch_records_overlay_only_policy() -> None:
    ensure_stage5ed_built()
    result = load_yaml(
        "data/operator-console/source-browser/number-fact-review-batches/"
        "stage5ed-review-batch-004-disk-visual-method-result.yaml"
    )

    assert result["overlay_count"] == 25
    assert result["overlays_added_now"] is True
    assert result["historical_source_lock_records_rewritten"] is False
    assert result["source_lock_evidence_updated_now"] is False
    assert result["facts_added_directly_to_source_records"] is False
    assert result["facts_added_as_overlays"] is True
