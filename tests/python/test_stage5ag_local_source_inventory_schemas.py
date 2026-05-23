from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
import yaml
from jsonschema import Draft202012Validator, ValidationError


def _yaml(path: str) -> Any:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def _records(path: str) -> list[dict[str, Any]]:
    payload = _yaml(path)
    return [dict(record) for record in payload.get("records", [])]


def _validator(path: str) -> Draft202012Validator:
    return Draft202012Validator(json.loads(Path(path).read_text(encoding="utf-8")))


def test_stage5ag_schemas_validate_committed_records() -> None:
    pairs = [
        (
            "schemas/source-harvester/local-source-root-inventory-record-v0.schema.json",
            "data/source-harvester/stage5ag-local-source-root-inventory.yaml",
        ),
        (
            "schemas/source-harvester/local-source-file-inventory-summary-record-v0.schema.json",
            "data/source-harvester/stage5ag-local-source-file-inventory-summary.yaml",
        ),
        (
            "schemas/source-harvester/local-archive-inventory-summary-record-v0.schema.json",
            "data/source-harvester/stage5ag-local-archive-inventory-summary.yaml",
        ),
        (
            "schemas/source-harvester/local-source-hash-inventory-summary-record-v0.schema.json",
            "data/source-harvester/stage5ag-local-source-hash-inventory-summary.yaml",
        ),
        (
            "schemas/source-harvester/stage5ag-source-harvester-summary-v0.schema.json",
            "data/source-harvester/stage5ag-source-harvester-summary.yaml",
        ),
    ]
    for schema_path, record_path in pairs:
        _validator(schema_path).validate(_yaml(record_path))

    record_schema_pairs = [
        (
            "schemas/source-harvester/manifest-local-linkage-record-v0.schema.json",
            "data/source-harvester/stage5ag-manifest-local-linkage.yaml",
        ),
        (
            "schemas/source-harvester/source-lock-candidate-summary-record-v0.schema.json",
            "data/source-harvester/stage5ag-source-lock-candidate-summary.yaml",
        ),
        (
            "schemas/source-harvester/local-source-gap-report-record-v0.schema.json",
            "data/source-harvester/stage5ag-local-source-gap-report.yaml",
        ),
        (
            "schemas/source-harvester/research-bundle-readiness-record-v0.schema.json",
            "data/source-harvester/stage5ag-research-bundle-readiness.yaml",
        ),
        (
            "schemas/source-harvester/local-source-manifest-extension-record-v0.schema.json",
            "data/source-harvester/stage5ag-local-source-manifest-extension.yaml",
        ),
        (
            "schemas/source-harvester/stage5ag-source-harvester-next-stage-decision-record-v0.schema.json",
            "data/source-harvester/stage5ag-source-harvester-next-stage-decision.yaml",
        ),
    ]
    for schema_path, record_path in record_schema_pairs:
        validator = _validator(schema_path)
        validator.validate(_yaml(record_path))
        for record in _records(record_path):
            validator.validate(record)


def test_stage5ag_schemas_reject_forbidden_flags() -> None:
    summary_validator = _validator(
        "schemas/source-harvester/stage5ag-source-harvester-summary-v0.schema.json"
    )
    summary = _yaml("data/source-harvester/stage5ag-source-harvester-summary.yaml")
    with pytest.raises(ValidationError):
        summary_validator.validate({**summary, "solve_claim": True})
    with pytest.raises(ValidationError):
        summary_validator.validate({**summary, "cuda_execution_performed": True})
    with pytest.raises(ValidationError):
        summary_validator.validate({**summary, "new_cuda_kernels_added": 1})
    with pytest.raises(ValidationError):
        summary_validator.validate({**summary, "generated_outputs_committed": True})

    guardrail_validator = _validator(
        "schemas/source-harvester/local-source-guardrail-record-v0.schema.json"
    )
    guardrail = _yaml("data/source-harvester/stage5ag-local-source-guardrail.yaml")
    with pytest.raises(ValidationError):
        guardrail_validator.validate({**guardrail, "google_drive_storage_used": True})
