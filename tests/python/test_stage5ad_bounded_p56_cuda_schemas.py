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


def test_stage5ad_schemas_validate_committed_records() -> None:
    cases = [
        (
            "schemas/cuda/bounded-p56-cuda-run-record-v0.schema.json",
            "data/cuda/stage5ad-bounded-p56-cuda-run.yaml",
        ),
        (
            "schemas/cuda/bounded-p56-cuda-parity-record-v0.schema.json",
            "data/cuda/stage5ad-bounded-p56-cuda-parity.yaml",
        ),
        (
            "schemas/cuda/bounded-p56-cuda-result-store-preflight-record-v0.schema.json",
            "data/cuda/stage5ad-bounded-p56-cuda-result-store-preflight.yaml",
        ),
        (
            "schemas/cuda/bounded-p56-cuda-score-summary-preflight-record-v0.schema.json",
            "data/cuda/stage5ad-bounded-p56-cuda-score-summary-preflight.yaml",
        ),
        (
            "schemas/cuda/bounded-p56-cuda-full-p56-blocker-record-v0.schema.json",
            "data/cuda/stage5ad-bounded-p56-cuda-full-p56-blocker.yaml",
        ),
        (
            "schemas/cuda/bounded-p56-cuda-scored-experiment-deferral-record-v0.schema.json",
            "data/cuda/stage5ad-bounded-p56-cuda-scored-experiment-deferral.yaml",
        ),
        (
            "schemas/cuda/bounded-p56-cuda-doc-staleness-validation-record-v0.schema.json",
            "data/cuda/stage5ad-bounded-p56-cuda-doc-staleness-validation.yaml",
        ),
        (
            "schemas/cuda/bounded-p56-cuda-device-subset-audit-record-v0.schema.json",
            "data/cuda/stage5ad-bounded-p56-cuda-device-subset-audit.yaml",
        ),
        (
            "schemas/cuda/bounded-p56-cuda-next-stage-decision-record-v0.schema.json",
            "data/cuda/stage5ad-bounded-p56-cuda-next-stage-decision.yaml",
        ),
    ]
    for schema, record_path in cases:
        validator = _validator(schema)
        for record in _records(record_path):
            validator.validate(record)

    _validator("schemas/cuda/stage5ad-bounded-p56-cuda-parity-summary-v0.schema.json").validate(
        _yaml("data/cuda/stage5ad-bounded-p56-cuda-parity-summary.yaml")
    )


def test_stage5ad_run_schema_rejects_solve_claim_and_generated_commit() -> None:
    validator = _validator("schemas/cuda/bounded-p56-cuda-run-record-v0.schema.json")
    record = _records("data/cuda/stage5ad-bounded-p56-cuda-run.yaml")[0]

    with pytest.raises(ValidationError):
        validator.validate({**record, "solve_claim": True})
    with pytest.raises(ValidationError):
        validator.validate({**record, "generated_outputs_committed": True})
