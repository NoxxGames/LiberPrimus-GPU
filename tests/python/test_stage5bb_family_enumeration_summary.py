from pathlib import Path

import yaml


def test_stage5bb_family_enumeration_summary_is_unique_metadata_only() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bb-family-enumeration-summary.yaml").read_text())

    assert payload["family_enumeration_mode"] == "metadata_only"
    assert payload["unique_variant_family_count"] == 10
    assert payload["taxonomy_membership_count"] == 11
    assert payload["duplicate_active_family_id_count"] == 0
    assert payload["real_variant_branches_enumerated"] is False
    assert payload["variant_outputs_generated"] is False
