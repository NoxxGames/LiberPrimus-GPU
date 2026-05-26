from pathlib import Path

import yaml


def test_stage5bb_branch_counter_summary_matches_stage5az_budget() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bb-branch-counter-summary.yaml").read_text())

    assert payload["branch_counter_mode"] == "metadata_only"
    assert payload["branch_upper_bound_product"] == 2720083094132915643088896
    assert payload["primary60_mappable_branch_upper_bound_product"] == 4194304
    assert payload["full_cartesian_product_enumerated"] is False
    assert payload["variant_byte_streams_generated"] is False
