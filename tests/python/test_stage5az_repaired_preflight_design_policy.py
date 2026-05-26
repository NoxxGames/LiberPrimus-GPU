from pathlib import Path

import yaml


def test_stage5az_repaired_policy_remains_design_only() -> None:
    payload = yaml.safe_load(
        Path("data/token-block/stage5az-repaired-preflight-design-policy.yaml").read_text(encoding="utf-8")
    )

    assert payload["policy_status"] == "design_only_repaired_for_family_id_uniqueness"
    assert payload["variant_byte_stream_generation_allowed_now"] is False
    assert payload["token_experiment_execution_allowed_now"] is False
    assert payload["duplicate_family_records_allowed"] is False
    assert payload["duplicate_taxonomy_membership_allowed"] is True
