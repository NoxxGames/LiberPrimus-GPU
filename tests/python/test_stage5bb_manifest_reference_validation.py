from pathlib import Path

import yaml


def test_stage5bb_manifest_reference_validation_blocks_inactive_active_loads() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bb-manifest-reference-validation.yaml").read_text())

    assert payload["all_manifest_references_resolve"] is True
    assert payload["inactive_manifest_used_as_active_count"] == 0
    assert payload["stage5av_branch_manifest_active"] is False
    assert payload["stage5ay_variant_family_manifest_active"] is False
    assert payload["stage5aw_branch_manifest_active"] is True
    assert payload["stage5az_variant_family_manifest_active"] is True
