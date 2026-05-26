from pathlib import Path

import yaml


def test_stage5bb_manifest_precedence_marks_superseded_inputs_inactive() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bb-manifest-precedence-policy.yaml").read_text())
    rules = {rule["rule_id"]: rule for rule in payload["rules"]}

    assert rules["stage5aw_supersedes_stage5av_branch_manifest"]["inactive_path"] == (
        "data/token-block/stage5av-token-variant-branch-manifest.yaml"
    )
    assert rules["stage5az_supersedes_stage5ay_variant_family_manifest"]["active_path"] == (
        "data/token-block/stage5az-repaired-bounded-variant-family-manifest.yaml"
    )
    assert payload["stale_active_load_allowed"] is False
    assert payload["execution_authorised_now"] is False
