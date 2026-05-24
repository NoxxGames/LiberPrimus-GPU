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


def test_stage5aj_committed_records_validate_against_schemas() -> None:
    pairs = [
        ("schemas/source-harvester/usefulfiles-local-inventory-record-v0.schema.json", "data/source-harvester/stage5aj-usefulfiles-local-inventory.yaml"),
        ("schemas/source-harvester/usefulfiles-source-manifest-extension-v0.schema.json", "data/source-harvester/stage5aj-usefulfiles-source-manifest-extension.yaml"),
        ("schemas/source-harvester/xlsx-extraction-summary-v0.schema.json", "data/source-harvester/stage5aj-xlsx-extraction-summary.yaml"),
        ("schemas/source-harvester/important-links-source-index-v0.schema.json", "data/source-harvester/stage5aj-important-links-source-index.yaml"),
        ("schemas/source-harvester/extraction-fidelity-policy-v0.schema.json", "data/source-harvester/stage5aj-extraction-fidelity-policy.yaml"),
        ("schemas/source-harvester/redaction-policy-v0.schema.json", "data/source-harvester/stage5aj-redaction-policy.yaml"),
        ("schemas/source-harvester/scraper-capture-policy-v0.schema.json", "data/source-harvester/stage5aj-scraper-capture-policy.yaml"),
        ("schemas/source-harvester/deep-research-pack-update-summary-v0.schema.json", "data/source-harvester/stage5aj-deep-research-pack-update-summary.yaml"),
        ("schemas/source-harvester/stage5aj-summary-v0.schema.json", "data/source-harvester/stage5aj-summary.yaml"),
    ]
    for schema_path, record_path in pairs:
        _validator(schema_path).validate(_yaml(record_path))


def test_stage5aj_summary_schema_rejects_forbidden_flags() -> None:
    summary = _yaml("data/source-harvester/stage5aj-summary.yaml")
    validator = _validator("schemas/source-harvester/stage5aj-summary-v0.schema.json")
    with pytest.raises(ValidationError):
        validator.validate({**summary, "solve_claim": True})
    with pytest.raises(ValidationError):
        validator.validate({**summary, "cuda_execution_performed": True})
    with pytest.raises(ValidationError):
        validator.validate({**summary, "raw_xlsx_committed": True})
    with pytest.raises(ValidationError):
        validator.validate({**summary, "generated_bundle_bodies_committed": True})
