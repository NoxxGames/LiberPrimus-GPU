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
    return list(_yaml(path)["records"])


def _validator(path: str) -> Draft202012Validator:
    return Draft202012Validator(json.loads(Path(path).read_text(encoding="utf-8")))


def test_stage5ae_schemas_validate_committed_records() -> None:
    cases = [
        ("schemas/cuda/corrected-bounded-p56-formula-parity-report-record-v0.schema.json", "data/cuda/stage5ae-corrected-bounded-p56-formula-parity-report.yaml"),
        ("schemas/cuda/bounded-p56-reference-contract-repair-record-v0.schema.json", "data/cuda/stage5ae-bounded-p56-reference-contract-repair.yaml"),
        ("schemas/cuda/hash-material-policy-record-v0.schema.json", "data/cuda/stage5ae-hash-material-policy.yaml"),
        ("schemas/cuda/corrected-bounded-p56-result-store-integration-record-v0.schema.json", "data/cuda/stage5ae-corrected-bounded-p56-result-store-integration.yaml"),
        ("schemas/cuda/corrected-bounded-p56-score-summary-integration-record-v0.schema.json", "data/cuda/stage5ae-corrected-bounded-p56-score-summary-integration.yaml"),
        ("schemas/cuda/corrected-bounded-p56-method-status-impact-record-v0.schema.json", "data/cuda/stage5ae-corrected-bounded-p56-method-status-impact.yaml"),
        ("schemas/cuda/corrected-bounded-p56-generated-body-policy-record-v0.schema.json", "data/cuda/stage5ae-corrected-bounded-p56-generated-body-policy.yaml"),
        ("schemas/cuda/corrected-bounded-p56-full-p56-blocker-record-v0.schema.json", "data/cuda/stage5ae-corrected-bounded-p56-full-p56-blocker.yaml"),
        ("schemas/cuda/corrected-bounded-p56-scored-experiment-deferral-record-v0.schema.json", "data/cuda/stage5ae-corrected-bounded-p56-scored-experiment-deferral.yaml"),
        ("schemas/cuda/archive-source-lock-deferral-record-v0.schema.json", "data/cuda/stage5ae-archive-source-lock-deferral.yaml"),
        ("schemas/cuda/corrected-bounded-p56-doc-staleness-validation-record-v0.schema.json", "data/cuda/stage5ae-corrected-bounded-p56-doc-staleness-validation.yaml"),
        ("schemas/cuda/corrected-bounded-p56-next-stage-decision-record-v0.schema.json", "data/cuda/stage5ae-corrected-bounded-p56-next-stage-decision.yaml"),
    ]
    for schema, record_path in cases:
        validator = _validator(schema)
        for record in _records(record_path):
            validator.validate(record)
    _validator("schemas/cuda/stage5ae-corrected-bounded-p56-reporting-summary-v0.schema.json").validate(
        _yaml("data/cuda/stage5ae-corrected-bounded-p56-reporting-summary.yaml")
    )


def test_stage5ae_schema_rejects_forbidden_flags() -> None:
    validator = _validator("schemas/cuda/corrected-bounded-p56-formula-parity-report-record-v0.schema.json")
    record = _records("data/cuda/stage5ae-corrected-bounded-p56-formula-parity-report.yaml")[0]
    with pytest.raises(ValidationError):
        validator.validate({**record, "solve_claim": True})
    with pytest.raises(ValidationError):
        validator.validate({**record, "cuda_execution_performed": True})
    with pytest.raises(ValidationError):
        validator.validate({**record, "generated_outputs_committed": True})
    with pytest.raises(ValidationError):
        validator.validate({**record, "historical_stage5ad_reclassified_as_passed": True})
