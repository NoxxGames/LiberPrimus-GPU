from pathlib import Path

import yaml


def test_stage5ay_branch_budget_blocks_full_cartesian_product() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5ay-branch-count-budget.yaml").read_text(encoding="utf-8"))

    assert payload["branch_count_upper_bound_product"] == 2720083094132915643088896
    assert payload["branch_count_upper_bound_log10"] == 24.434582
    assert payload["primary60_mappable_branch_upper_bound_product"] == 4194304
    assert payload["primary60_mappable_branch_upper_bound_log10"] == 6.62266
    assert payload["full_cartesian_product_allowed"] is False
