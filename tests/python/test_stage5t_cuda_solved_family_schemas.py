from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
import yaml


def _schema(name: str) -> dict[str, Any]:
    return json.loads(Path("schemas/cuda", name).read_text(encoding="utf-8"))


def _records(path: str) -> list[dict[str, Any]]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"]


def _yaml(path: str) -> dict[str, Any]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def _errors(schema_name: str, record: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(_schema(schema_name))
    return [error.message for error in validator.iter_errors(record)]


def test_stage5t_committed_records_validate_against_schemas() -> None:
    cases = [
        (
            "solved-family-cuda-inventory-record-v0.schema.json",
            _records("data/cuda/stage5t-solved-family-cuda-inventory.yaml"),
        ),
        (
            "solved-family-cuda-parity-matrix-record-v0.schema.json",
            _records("data/cuda/stage5t-solved-family-cuda-parity-matrix.yaml"),
        ),
        (
            "cuda-kernel-readiness-record-v0.schema.json",
            _records("data/cuda/stage5t-cuda-kernel-readiness.yaml"),
        ),
        (
            "cuda-candidate-batch-abi-gap-record-v0.schema.json",
            _records("data/cuda/stage5t-cuda-candidate-batch-abi-gaps.yaml"),
        ),
        (
            "cuda-benchmark-readiness-record-v0.schema.json",
            _records("data/cuda/stage5t-cuda-benchmark-readiness.yaml"),
        ),
        (
            "cuda-no-unsolved-guardrail-review-record-v0.schema.json",
            _records("data/cuda/stage5t-cuda-no-unsolved-guardrail-review.yaml"),
        ),
        (
            "cuda-next-stage-decision-record-v0.schema.json",
            _records("data/cuda/stage5t-cuda-next-stage-decision.yaml"),
        ),
    ]
    for schema_name, records in cases:
        for record in records:
            assert _errors(schema_name, record) == []

    summary = _yaml("data/cuda/stage5t-cuda-solved-family-readiness-summary.yaml")
    assert _errors("stage5t-cuda-solved-family-readiness-summary-v0.schema.json", summary) == []


def test_stage5t_schemas_reject_core_guardrail_violations() -> None:
    matrix = _records("data/cuda/stage5t-solved-family-cuda-parity-matrix.yaml")[0]
    schema_name = "solved-family-cuda-parity-matrix-record-v0.schema.json"
    assert _errors(schema_name, {**matrix, "solve_claim": True})
    assert _errors(schema_name, {**matrix, "cuda_execution_performed": True})
    assert _errors(schema_name, {**matrix, "cuda_source_modified": True})
    assert _errors(schema_name, {**matrix, "gpu_benchmark_performed": True})

    summary = _yaml("data/cuda/stage5t-cuda-solved-family-readiness-summary.yaml")
    summary_schema = "stage5t-cuda-solved-family-readiness-summary-v0.schema.json"
    assert _errors(summary_schema, {**summary, "speedup_claim": True})
    assert _errors(summary_schema, {**summary, "method_status_upgraded": True})
