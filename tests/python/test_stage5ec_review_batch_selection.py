from __future__ import annotations

from pathlib import Path

from test_stage5ec_common import ensure_stage5ec_built, load_yaml


def test_stage5ec_selected_batch_has_exactly_twenty_existing_entries() -> None:
    ensure_stage5ec_built()
    result = load_yaml(
        "data/operator-console/source-browser/number-fact-review-batches/"
        "stage5ec-review-batch-003-triangle-page32-token-music-result.yaml"
    )
    selected = result["selected_source_record_paths"]

    assert result["review_batch_id"] == "number_fact_review_batch_003_triangle_page32_token_music"
    assert result["review_scope"] == "selected_20_source_records_only"
    assert len(selected) == 20
    assert selected[0] == "data/historical-route/stage5dl-number-triangle-v1-source-lock.yaml"
    assert selected[-1] == "data/historical-route/stage5ds-token-block-vm-or-table-surface-candidate-v0.yaml"
    assert all(Path(path).exists() for path in selected)


def test_stage5ec_review_batch_records_overlay_only_policy() -> None:
    ensure_stage5ec_built()
    result = load_yaml(
        "data/operator-console/source-browser/number-fact-review-batches/"
        "stage5ec-review-batch-003-triangle-page32-token-music-result.yaml"
    )

    assert result["overlay_count"] == 25
    assert result["overlays_added_now"] is True
    assert result["historical_source_lock_records_rewritten"] is False
    assert result["source_lock_evidence_updated_now"] is False
    assert result["facts_added_directly_to_source_records"] is False
    assert result["facts_added_as_overlays"] is True
