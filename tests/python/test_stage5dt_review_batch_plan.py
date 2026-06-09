from __future__ import annotations

from test_stage5dt_common import ensure_stage5dt_built, load_yaml


def test_review_batch_plan_is_stable_and_bounded() -> None:
    ensure_stage5dt_built()
    plan = load_yaml("data/operator-console/source-browser/number-fact-review-batches/stage5dt-batch-plan.yaml")
    assert plan["review_performed_now"] is False
    assert plan["batch_size_default"] == 20
    assert plan["total_batches"] >= 1
    assert all(1 <= batch["entry_count"] <= 20 for batch in plan["batches"])
    assert plan["batches"][0]["priority_reason"] == "first_stable_batch"
