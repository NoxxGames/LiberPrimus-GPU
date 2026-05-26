from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


def test_stage5az_repaired_variant_family_manifest_has_unique_ids() -> None:
    payload = yaml.safe_load(
        Path("data/token-block/stage5az-repaired-bounded-variant-family-manifest.yaml").read_text(
            encoding="utf-8"
        )
    )
    schema = yaml.safe_load(
        Path("schemas/token-block/repaired-bounded-variant-family-manifest-v0.schema.json").read_text(
            encoding="utf-8"
        )
    )

    Draft202012Validator(schema).validate(payload)
    ids = [record["family_id"] for record in payload["families"]]
    assert len(ids) == len(set(ids))
    assert ids.count("unresolved_as_current_only") == 1
    unresolved = next(record for record in payload["families"] if record["family_id"] == "unresolved_as_current_only")
    assert unresolved["taxonomy_memberships"] == ["baseline_family", "unresolved_policy_family"]
    assert payload["unique_family_count"] == 10
    assert payload["taxonomy_membership_count"] == 11
