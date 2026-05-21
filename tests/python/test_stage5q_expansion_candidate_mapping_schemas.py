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


def test_stage5q_committed_records_validate_against_schemas() -> None:
    cases = [
        (
            "gematria-expansion-candidate-inventory-record-v0.schema.json",
            _records("data/cuda/stage5q-gematria-expansion-candidate-inventory.yaml"),
        ),
        (
            "gematria-expansion-token-mapping-record-v0.schema.json",
            _records("data/cuda/stage5q-gematria-expansion-token-mapping.yaml"),
        ),
        (
            "gematria-expansion-native-parity-record-v0.schema.json",
            _records("data/cuda/stage5q-gematria-expansion-native-parity.yaml"),
        ),
        (
            "gematria-expansion-result-store-preflight-record-v0.schema.json",
            _records("data/cuda/stage5q-gematria-expansion-result-store-preflight.yaml"),
        ),
        (
            "gematria-expansion-gate-record-v0.schema.json",
            _records("data/cuda/stage5q-gematria-expansion-gate.yaml"),
        ),
    ]
    for schema_name, records in cases:
        for record in records:
            assert _errors(schema_name, record) == []

    summary = _yaml("data/cuda/stage5q-expansion-candidate-mapping-summary.yaml")
    assert _errors("stage5q-expansion-candidate-mapping-summary-v0.schema.json", summary) == []


def test_stage5q_schemas_reject_guardrail_violations() -> None:
    mapping = _records("data/cuda/stage5q-gematria-expansion-token-mapping.yaml")[0]
    mapping_schema = "gematria-expansion-token-mapping-record-v0.schema.json"
    assert _errors(mapping_schema, {**mapping, "solve_claim": True})
    assert _errors(mapping_schema, {**mapping, "cuda_execution_performed": True})
    assert _errors(mapping_schema, {**mapping, "generated_outputs_committed": True})
    assert _errors(mapping_schema, {**mapping, "new_cuda_kernels_added": 1})

    preflight = _records("data/cuda/stage5q-gematria-expansion-result-store-preflight.yaml")[0]
    preflight_schema = "gematria-expansion-result-store-preflight-record-v0.schema.json"
    assert _errors(preflight_schema, {**preflight, "confidence_interpretation": "solve_evidence"})

    summary = _yaml("data/cuda/stage5q-expansion-candidate-mapping-summary.yaml")
    summary_schema = "stage5q-expansion-candidate-mapping-summary-v0.schema.json"
    assert _errors(summary_schema, {**summary, "method_status_upgrade_allowed": True})
