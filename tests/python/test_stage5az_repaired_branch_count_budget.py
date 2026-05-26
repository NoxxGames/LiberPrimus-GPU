from pathlib import Path

import yaml


def test_stage5az_branch_budget_is_unchanged() -> None:
    stage5ay = yaml.safe_load(
        Path("data/token-block/stage5ay-branch-count-budget.yaml").read_text(encoding="utf-8")
    )
    repaired = yaml.safe_load(
        Path("data/token-block/stage5az-repaired-branch-count-budget.yaml").read_text(encoding="utf-8")
    )

    assert repaired["branch_budget_changed"] is False
    assert repaired["branch_count_upper_bound_product"] == stage5ay["branch_count_upper_bound_product"]
    assert repaired["primary60_mappable_branch_upper_bound_product"] == stage5ay[
        "primary60_mappable_branch_upper_bound_product"
    ]
    assert repaired["full_cartesian_product_allowed"] is False
