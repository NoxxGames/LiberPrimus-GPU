from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


def test_stage5az_integrity_audit_schema_validates() -> None:
    payload = yaml.safe_load(
        Path("data/token-block/stage5az-preflight-manifest-integrity-audit.yaml").read_text(encoding="utf-8")
    )
    schema = yaml.safe_load(
        Path("schemas/token-block/preflight-manifest-integrity-audit-v0.schema.json").read_text(encoding="utf-8")
    )

    Draft202012Validator(schema).validate(payload)
    assert payload["duplicate_family_ids_before_repair"] == ["unresolved_as_current_only"]
    assert payload["token_experiments_executed"] is False
