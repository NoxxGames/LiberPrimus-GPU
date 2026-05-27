from pathlib import Path

import yaml


def test_stage5bd_dry_run_policy_blocks_execution() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bd-dry-run-policy.yaml").read_text())

    assert payload["real_execution_authorised"] is False
    assert payload["dry_run_scope"] == "no_output_preflight_plan_validation"
    assert payload["real_token_block_byte_generation_allowed"] is False
    assert payload["real_variant_materialisation_allowed"] is False
    assert payload["hash_search_allowed"] is False
