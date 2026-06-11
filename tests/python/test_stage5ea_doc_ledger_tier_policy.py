from __future__ import annotations

from test_stage5ea_common import ensure_stage5ea_built, load_yaml


def test_doc_ledger_tiers_separate_current_docs_from_history() -> None:
    ensure_stage5ea_built()

    record = load_yaml("data/project-state/stage5ea-doc-ledger-tier-policy.yaml")

    assert record["tier_a_must_track_current_and_next_stage"] is True
    assert "data/project-state/current-stage-state.yaml" in record["tier_a_paths"]
    assert record["tier_b_may_preserve_historical_stage_references"] is True
    assert record["tier_c_historical_logs_are_append_only"] is True
