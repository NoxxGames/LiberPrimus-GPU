from pathlib import Path

import yaml


def test_stage5ay_preflight_policy_is_design_only() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5ay-preflight-design-policy.yaml").read_text(encoding="utf-8"))

    assert payload["policy_status"] == "design_only"
    assert payload["variant_byte_stream_generation_allowed_now"] is False
    assert payload["token_experiment_execution_allowed_now"] is False
    assert payload["family_taxonomy"]["case_branch_family"]
