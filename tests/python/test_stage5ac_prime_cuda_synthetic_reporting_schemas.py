from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


def _yaml(path: str) -> Any:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def _records(path: str) -> list[dict[str, Any]]:
    return list(_yaml(path)["records"])


def _validator(path: str) -> Draft202012Validator:
    return Draft202012Validator(json.loads(Path(path).read_text(encoding="utf-8")))


def test_stage5ac_schemas_validate_committed_records() -> None:
    cases = [
        (
            "schemas/cuda/prime-minus-one-cuda-synthetic-parity-report-record-v0.schema.json",
            "data/cuda/stage5ac-prime-minus-one-cuda-synthetic-parity-report.yaml",
        ),
        (
            "schemas/cuda/prime-minus-one-cuda-synthetic-result-store-integration-record-v0.schema.json",
            "data/cuda/stage5ac-prime-minus-one-cuda-synthetic-result-store-integration.yaml",
        ),
        (
            "schemas/cuda/prime-minus-one-cuda-synthetic-score-summary-integration-record-v0.schema.json",
            "data/cuda/stage5ac-prime-minus-one-cuda-synthetic-score-summary-integration.yaml",
        ),
        (
            "schemas/cuda/prime-minus-one-cuda-synthetic-method-status-impact-record-v0.schema.json",
            "data/cuda/stage5ac-prime-minus-one-cuda-synthetic-method-status-impact.yaml",
        ),
        (
            "schemas/cuda/prime-minus-one-cuda-synthetic-generated-body-policy-record-v0.schema.json",
            "data/cuda/stage5ac-prime-minus-one-cuda-synthetic-generated-body-policy.yaml",
        ),
        (
            "schemas/cuda/bounded-p56-cuda-parity-preflight-record-v0.schema.json",
            "data/cuda/stage5ac-bounded-p56-cuda-parity-preflight.yaml",
        ),
        (
            "schemas/cuda/prime-minus-one-cuda-synthetic-full-p56-blocker-record-v0.schema.json",
            "data/cuda/stage5ac-prime-minus-one-cuda-synthetic-full-p56-blocker.yaml",
        ),
        (
            "schemas/cuda/prime-minus-one-cuda-synthetic-scored-experiment-deferral-record-v0.schema.json",
            "data/cuda/stage5ac-prime-minus-one-cuda-synthetic-scored-experiment-deferral.yaml",
        ),
        (
            "schemas/cuda/prime-minus-one-cuda-synthetic-doc-staleness-validation-record-v0.schema.json",
            "data/cuda/stage5ac-prime-minus-one-cuda-synthetic-doc-staleness-validation.yaml",
        ),
        (
            "schemas/cuda/prime-minus-one-cuda-synthetic-next-stage-decision-record-v0.schema.json",
            "data/cuda/stage5ac-prime-minus-one-cuda-synthetic-next-stage-decision.yaml",
        ),
    ]
    for schema, record_path in cases:
        validator = _validator(schema)
        for record in _records(record_path):
            validator.validate(record)

    _validator("schemas/cuda/stage5ac-prime-minus-one-cuda-synthetic-reporting-summary-v0.schema.json").validate(
        _yaml("data/cuda/stage5ac-prime-minus-one-cuda-synthetic-reporting-summary.yaml")
    )
