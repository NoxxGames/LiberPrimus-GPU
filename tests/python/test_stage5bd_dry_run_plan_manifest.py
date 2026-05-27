from pathlib import Path

import yaml


def test_stage5bd_dry_run_plan_manifest_is_metadata_only() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bd-dry-run-plan-manifest.yaml").read_text())

    assert payload["dry_run_plan_created"] is True
    assert payload["plan_inputs_are_metadata_only"] is True
    assert payload["real_byte_streams_generated"] is False
    assert payload["full_plan_family_cross_product_enumerated"] is False
    assert payload["representative_plan_id_count"] == 10
