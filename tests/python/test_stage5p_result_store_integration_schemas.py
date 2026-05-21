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


def test_stage5p_committed_records_validate_against_schemas() -> None:
    cases = [
        (
            "gematria-cuda-result-store-integration-record-v0.schema.json",
            _records("data/cuda/stage5p-gematria-cuda-result-store-integration.yaml"),
        ),
        (
            "gematria-cuda-score-summary-integration-record-v0.schema.json",
            _records("data/cuda/stage5p-gematria-cuda-score-summary-integration.yaml"),
        ),
        (
            "gematria-cuda-method-status-impact-record-v0.schema.json",
            _records("data/cuda/stage5p-gematria-cuda-method-status-impact.yaml"),
        ),
        (
            "gematria-cuda-generated-body-policy-record-v0.schema.json",
            _records("data/cuda/stage5p-gematria-cuda-generated-body-policy.yaml"),
        ),
        (
            "gematria-cuda-controlled-expansion-candidate-record-v0.schema.json",
            _records("data/cuda/stage5p-gematria-controlled-expansion-candidates.yaml"),
        ),
    ]
    for schema_name, records in cases:
        for record in records:
            assert _errors(schema_name, record) == []

    summary = _yaml("data/cuda/stage5p-cuda-result-store-integration-summary.yaml")
    assert _errors("stage5p-cuda-result-store-integration-summary-v0.schema.json", summary) == []


def test_stage5p_schemas_reject_guardrail_violations() -> None:
    result_store = _records("data/cuda/stage5p-gematria-cuda-result-store-integration.yaml")[0]
    result_schema = "gematria-cuda-result-store-integration-record-v0.schema.json"
    assert _errors(result_schema, {**result_store, "solve_claim": True})
    assert _errors(result_schema, {**result_store, "cuda_execution_performed": True})
    assert _errors(result_schema, {**result_store, "generated_outputs_committed": True})

    score = _records("data/cuda/stage5p-gematria-cuda-score-summary-integration.yaml")[0]
    score_schema = "gematria-cuda-score-summary-integration-record-v0.schema.json"
    assert _errors(score_schema, {**score, "confidence_label": "new_unreviewed_label"})

    summary = _yaml("data/cuda/stage5p-cuda-result-store-integration-summary.yaml")
    summary_schema = "stage5p-cuda-result-store-integration-summary-v0.schema.json"
    assert _errors(summary_schema, {**summary, "method_status_upgrade_allowed": True})
