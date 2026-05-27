from pathlib import Path

import yaml


def test_stage5bd_branch_family_counters_preserve_upper_bounds() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bd-branch-family-plan-counters.yaml").read_text())

    assert payload["variant_family_count"] == 10
    assert payload["variant_family_taxonomy_membership_count"] == 11
    assert payload["branch_upper_bound_product"] == 2720083094132915643088896
    assert payload["variant_byte_streams_generated"] is False
