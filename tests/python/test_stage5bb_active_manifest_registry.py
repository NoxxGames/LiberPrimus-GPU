from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


def test_stage5bb_active_manifest_registry_schema_and_paths() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bb-active-manifest-registry.yaml").read_text())
    schema = yaml.safe_load(Path("schemas/token-block/active-manifest-registry-v0.schema.json").read_text())

    Draft202012Validator(schema).validate(payload)
    roles = payload["active_manifest_roles"]
    assert roles["active_branch_manifest"]["path"] == "data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml"
    assert roles["active_bounded_variant_family_manifest"]["path"] == (
        "data/token-block/stage5az-repaired-bounded-variant-family-manifest.yaml"
    )
    assert roles["active_branch_eligibility_policy"]["required"] is True
    assert payload["stale_active_load_allowed"] is False
