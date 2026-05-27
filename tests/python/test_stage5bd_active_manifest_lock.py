from pathlib import Path

import yaml


def test_stage5bd_active_manifest_lock_preserves_repaired_inputs() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bd-active-manifest-lock.yaml").read_text())

    assert payload["active_branch_manifest"].endswith("stage5aw-repaired-token-variant-branch-manifest.yaml")
    assert payload["active_variant_family_manifest"].endswith(
        "stage5az-repaired-bounded-variant-family-manifest.yaml"
    )
    inactive = {record["manifest_key"]: record for record in payload["inactive_or_superseded_manifests"]}
    assert inactive["inactive_stage5av_branch_manifest"]["active_load_allowed"] is False
    assert inactive["inactive_stage5ay_bounded_variant_family_manifest"]["active_load_allowed"] is False
