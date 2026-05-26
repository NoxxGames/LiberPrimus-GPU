from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


def test_stage5az_taxonomy_policy_allows_membership_not_duplicate_records() -> None:
    payload = yaml.safe_load(
        Path("data/token-block/stage5az-family-taxonomy-membership-policy.yaml").read_text(encoding="utf-8")
    )
    schema = yaml.safe_load(
        Path("schemas/token-block/family-taxonomy-membership-policy-v0.schema.json").read_text(encoding="utf-8")
    )

    Draft202012Validator(schema).validate(payload)
    assert payload["duplicate_taxonomy_membership_allowed"] is True
    assert payload["duplicate_family_records_allowed"] is False
    assert payload["unresolved_as_current_only_memberships"] == ["baseline_family", "unresolved_policy_family"]
