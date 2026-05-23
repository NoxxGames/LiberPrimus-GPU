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


def test_stage5ai_committed_records_validate_against_schemas() -> None:
    pairs = [
        ("schemas/source-harvester/curated-bundle-extraction-policy-v0.schema.json", "data/source-harvester/stage5ai-curated-bundle-extraction-policy.yaml"),
        ("schemas/source-harvester/curated-source-card-summary-v0.schema.json", "data/source-harvester/stage5ai-curated-source-card-summary.yaml"),
        ("schemas/source-harvester/curated-content-index-summary-v0.schema.json", "data/source-harvester/stage5ai-curated-content-index-summary.yaml"),
        ("schemas/source-harvester/website-ingest-bundle-index-v0.schema.json", "data/source-harvester/stage5ai-website-ingest-format.yaml"),
        ("schemas/source-harvester/deep-research-pack-format-v0.schema.json", "data/source-harvester/stage5ai-deep-research-pack-format.yaml"),
        ("schemas/source-harvester/unclassified-source-classification-v0.schema.json", "data/source-harvester/stage5ai-unclassified-source-classification.yaml"),
        ("schemas/source-harvester/missing-source-plan-v0.schema.json", "data/source-harvester/stage5ai-missing-source-plan.yaml"),
        ("schemas/source-harvester/stage5ai-curated-research-bundle-summary-v0.schema.json", "data/source-harvester/stage5ai-curated-research-bundle-summary.yaml"),
    ]
    for schema_path, record_path in pairs:
        _validator(schema_path).validate(_yaml(record_path))


def test_stage5ai_schemas_reject_forbidden_flags() -> None:
    summary = _yaml("data/source-harvester/stage5ai-curated-research-bundle-summary.yaml")
    validator = _validator("schemas/source-harvester/stage5ai-curated-research-bundle-summary-v0.schema.json")
    with pytest.raises(ValidationError):
        validator.validate({**summary, "solve_claim": True})
    with pytest.raises(ValidationError):
        validator.validate({**summary, "cuda_execution_performed": True})
    with pytest.raises(ValidationError):
        validator.validate({**summary, "generated_bundle_bodies_committed": True})
