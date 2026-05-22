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


def test_stage5u_committed_records_validate_against_schemas() -> None:
    cases = [
        ("candidate-batch-abi-record-v0.schema.json", _records("data/cuda/stage5u-candidate-batch-abi.yaml")),
        ("token-buffer-contract-record-v0.schema.json", _records("data/cuda/stage5u-token-buffer-contract.yaml")),
        (
            "transform-parameter-contract-record-v0.schema.json",
            _records("data/cuda/stage5u-transform-parameter-contract.yaml"),
        ),
        ("key-schedule-contract-record-v0.schema.json", _records("data/cuda/stage5u-key-schedule-contract.yaml")),
        ("stream-schedule-contract-record-v0.schema.json", _records("data/cuda/stage5u-stream-schedule-contract.yaml")),
        ("score-vector-contract-record-v0.schema.json", _records("data/cuda/stage5u-score-vector-contract.yaml")),
        ("topk-output-contract-record-v0.schema.json", _records("data/cuda/stage5u-topk-output-contract.yaml")),
        ("backend-surface-contract-record-v0.schema.json", _records("data/cuda/stage5u-backend-surface-contract.yaml")),
        (
            "candidate-batch-result-store-compatibility-record-v0.schema.json",
            _records("data/cuda/stage5u-result-store-compatibility.yaml"),
        ),
        ("candidate-batch-abi-gap-closure-record-v0.schema.json", _records("data/cuda/stage5u-abi-gap-closure.yaml")),
    ]
    for schema_name, records in cases:
        for record in records:
            assert _errors(schema_name, record) == []

    summary = _yaml("data/cuda/stage5u-candidate-batch-abi-summary.yaml")
    assert _errors("stage5u-candidate-batch-abi-summary-v0.schema.json", summary) == []


def test_stage5u_schemas_reject_guardrail_violations() -> None:
    abi = _records("data/cuda/stage5u-candidate-batch-abi.yaml")[0]
    schema_name = "candidate-batch-abi-record-v0.schema.json"
    assert _errors(schema_name, {**abi, "solve_claim": True})
    assert _errors(schema_name, {**abi, "cuda_execution_performed": True})
    assert _errors(schema_name, {**abi, "cuda_source_modified": True})
    assert _errors(schema_name, {**abi, "generated_outputs_committed": True})

    summary = _yaml("data/cuda/stage5u-candidate-batch-abi-summary.yaml")
    summary_schema = "stage5u-candidate-batch-abi-summary-v0.schema.json"
    assert _errors(summary_schema, {**summary, "gpu_benchmark_performed": True})
    assert _errors(summary_schema, {**summary, "deep_research_recommended_next": True})
