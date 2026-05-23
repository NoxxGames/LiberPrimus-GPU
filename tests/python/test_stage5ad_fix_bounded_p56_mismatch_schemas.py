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


def test_stage5ad_fix_schemas_validate_committed_records() -> None:
    cases = [
        ("schemas/cuda/bounded-p56-mismatch-hash-lineage-record-v0.schema.json", "data/cuda/stage5ad-fix-bounded-p56-mismatch-hash-lineage.yaml"),
        ("schemas/cuda/bounded-p56-mismatch-token-trace-record-v0.schema.json", "data/cuda/stage5ad-fix-bounded-p56-mismatch-token-trace.yaml"),
        ("schemas/cuda/bounded-p56-mismatch-stream-trace-record-v0.schema.json", "data/cuda/stage5ad-fix-bounded-p56-mismatch-stream-trace.yaml"),
        ("schemas/cuda/bounded-p56-mismatch-formula-trace-record-v0.schema.json", "data/cuda/stage5ad-fix-bounded-p56-mismatch-formula-trace.yaml"),
        ("schemas/cuda/bounded-p56-mismatch-hash-material-record-v0.schema.json", "data/cuda/stage5ad-fix-bounded-p56-mismatch-hash-material.yaml"),
        ("schemas/cuda/bounded-p56-mismatch-reference-contract-record-v0.schema.json", "data/cuda/stage5ad-fix-bounded-p56-mismatch-reference-contract.yaml"),
        ("schemas/cuda/bounded-p56-mismatch-root-cause-record-v0.schema.json", "data/cuda/stage5ad-fix-bounded-p56-mismatch-root-cause.yaml"),
        ("schemas/cuda/bounded-p56-mismatch-repair-readiness-record-v0.schema.json", "data/cuda/stage5ad-fix-bounded-p56-mismatch-repair-readiness.yaml"),
        ("schemas/cuda/bounded-p56-mismatch-guardrail-record-v0.schema.json", "data/cuda/stage5ad-fix-bounded-p56-mismatch-guardrail.yaml"),
        ("schemas/cuda/bounded-p56-mismatch-next-stage-decision-record-v0.schema.json", "data/cuda/stage5ad-fix-bounded-p56-mismatch-next-stage-decision.yaml"),
    ]
    for schema, record_path in cases:
        validator = _validator(schema)
        for record in _records(record_path):
            validator.validate(record)
    _validator("schemas/cuda/stage5ad-fix-bounded-p56-mismatch-summary-v0.schema.json").validate(
        _yaml("data/cuda/stage5ad-fix-bounded-p56-mismatch-summary.yaml")
    )


def test_stage5ad_fix_schema_rejects_forbidden_flags() -> None:
    validator = _validator("schemas/cuda/bounded-p56-mismatch-reference-contract-record-v0.schema.json")
    record = _records("data/cuda/stage5ad-fix-bounded-p56-mismatch-reference-contract.yaml")[0]
    with pytest.raises(ValidationError):
        validator.validate({**record, "solve_claim": True})
    with pytest.raises(ValidationError):
        validator.validate({**record, "cuda_execution_performed": True})
    with pytest.raises(ValidationError):
        validator.validate({**record, "generated_outputs_committed": True})
