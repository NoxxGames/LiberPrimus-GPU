from __future__ import annotations

from pathlib import Path

from test_stage5dw_common import ensure_stage5dw_built, load_yaml


def test_stage5dw_selected_batch_has_exactly_twenty_existing_entries() -> None:
    ensure_stage5dw_built()
    selection = load_yaml("data/project-state/stage5dw-review-batch-001-selection.yaml")
    selected = selection["selected_source_record_paths"]

    assert selection["stage5dt_stable_batch_plan_preserved"] is True
    assert selection["stage5dt_stable_batch_001_not_mutated"] is True
    assert selection["stage5dw_batch_selection_policy"] == "assistant_operator_high_signal_evidence_batch"
    assert len(selected) == 20
    assert all(Path(path).exists() for path in selected)


def test_stage5dw_batch_result_records_overlay_counts_without_source_rewrite() -> None:
    ensure_stage5dw_built()
    result = load_yaml(
        "data/operator-console/source-browser/number-fact-review-batches/"
        "stage5dw-review-batch-001-high-signal-result.yaml"
    )

    assert result["reviewed_entry_count"] == 20
    assert result["overlays_added_count"] == 37
    assert result["overlay_only_cards_required_count"] > 0
    assert result["facts_added_directly_to_source_records"] is False
    assert result["historical_source_lock_records_rewritten"] is False
