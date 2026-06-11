from __future__ import annotations

from test_stage5eb_common import ensure_stage5eb_built, load_yaml


def test_stage5eb_preserves_stage5ea_as_prior_validation_repair() -> None:
    ensure_stage5eb_built()

    record = load_yaml("data/project-state/stage5eb-stage5ea-preservation.yaml")
    summary = load_yaml("data/project-state/stage5eb-summary.yaml")

    assert record["stage5ea_status"] == "complete"
    assert record["stage5ea_issue"] == 162
    assert record["stage5ea_ci_status"] == "passed"
    assert record["stage5ea_parallel_worker_cap"] == 8
    assert record["number_fact_review_batch_3_deferred_to_stage5ec"] is True
    assert summary["stage5ea_recommended_stage5eb_number_fact_batch_3"] is True
    assert summary["operator_inserted_validation_finalization_repair_before_batch_3"] is True
    assert summary["number_fact_review_batch_3_performed_now"] is False
