from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
import yaml
from jsonschema import Draft202012Validator, ValidationError


def _yaml(path: str) -> dict[str, Any]:
    payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _validator(path: str) -> Draft202012Validator:
    return Draft202012Validator(json.loads(Path(path).read_text(encoding="utf-8")))


def test_stage5ak_committed_records_validate_against_schemas() -> None:
    pairs = [
        (
            "schemas/source-harvester/community-facts-local-inventory-record-v0.schema.json",
            "data/source-harvester/stage5ak-community-facts-local-inventory.yaml",
        ),
        (
            "schemas/source-harvester/community-facts-source-card-summary-v0.schema.json",
            "data/source-harvester/stage5ak-community-facts-source-card-summary.yaml",
        ),
        (
            "schemas/source-harvester/community-facts-content-index-summary-v0.schema.json",
            "data/source-harvester/stage5ak-community-facts-content-index-summary.yaml",
        ),
        (
            "schemas/source-harvester/community-facts-attachment-index-v0.schema.json",
            "data/source-harvester/stage5ak-community-facts-attachment-index.yaml",
        ),
        (
            "schemas/source-harvester/community-facts-clue-category-v0.schema.json",
            "data/source-harvester/stage5ak-community-facts-clue-categories.yaml",
        ),
        (
            "schemas/source-harvester/community-claim-policy-v0.schema.json",
            "data/source-harvester/stage5ak-community-claim-policy.yaml",
        ),
        (
            "schemas/source-harvester/community-facts-claim-record-v0.schema.json",
            "data/source-harvester/stage5ak-community-facts-claim-records.yaml",
        ),
        (
            "schemas/source-harvester/community-facts-correction-log-v0.schema.json",
            "data/source-harvester/stage5ak-community-facts-correction-log.yaml",
        ),
        (
            "schemas/source-harvester/community-facts-arithmetic-preflight-v0.schema.json",
            "data/source-harvester/stage5ak-community-facts-arithmetic-preflight.yaml",
        ),
        (
            "schemas/source-harvester/stage5ak-summary-v0.schema.json",
            "data/source-harvester/stage5ak-summary.yaml",
        ),
    ]
    for schema_path, record_path in pairs:
        _validator(schema_path).validate(_yaml(record_path))


def test_stage5ak_schemas_reject_forbidden_flags() -> None:
    summary = _yaml("data/source-harvester/stage5ak-summary.yaml")
    summary_validator = _validator("schemas/source-harvester/stage5ak-summary-v0.schema.json")
    with pytest.raises(ValidationError):
        summary_validator.validate({**summary, "solve_claim": True})
    with pytest.raises(ValidationError):
        summary_validator.validate({**summary, "raw_images_committed": True})
    with pytest.raises(ValidationError):
        summary_validator.validate({**summary, "generated_bundle_bodies_committed": True})

    claims = _yaml("data/source-harvester/stage5ak-community-facts-claim-records.yaml")
    claims_validator = _validator("schemas/source-harvester/community-facts-claim-record-v0.schema.json")
    with pytest.raises(ValidationError):
        claims_validator.validate({**claims, "execution_ready_count": 1})

    arithmetic = _yaml("data/source-harvester/stage5ak-community-facts-arithmetic-preflight.yaml")
    arithmetic_validator = _validator("schemas/source-harvester/community-facts-arithmetic-preflight-v0.schema.json")
    with pytest.raises(ValidationError):
        arithmetic_validator.validate({**arithmetic, "scan_or_search_performed": True})
