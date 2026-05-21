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


def test_stage5o_committed_records_validate_against_schemas() -> None:
    cases = [
        (
            "gematria-solved-fixture-cuda-repeat-run-record-v0.schema.json",
            _records("data/cuda/stage5o-gematria-solved-fixture-cuda-repeat-run.yaml"),
        ),
        (
            "gematria-solved-fixture-cuda-repeat-parity-record-v0.schema.json",
            _records("data/cuda/stage5o-gematria-solved-fixture-cuda-repeat-parity.yaml"),
        ),
        (
            "gematria-cuda-result-store-preflight-v0.schema.json",
            _records("data/cuda/stage5o-gematria-cuda-result-store-preflight.yaml"),
        ),
        (
            "gematria-cuda-score-summary-preflight-v0.schema.json",
            _records("data/cuda/stage5o-gematria-cuda-score-summary-preflight.yaml"),
        ),
        (
            "gematria-cuda-expansion-decision-record-v0.schema.json",
            _records("data/cuda/stage5o-gematria-cuda-expansion-decision.yaml"),
        ),
    ]
    for schema_name, records in cases:
        for record in records:
            assert _errors(schema_name, record) == []

    summary = _yaml("data/cuda/stage5o-repeat-verification-result-store-summary.yaml")
    assert _errors("stage5o-repeat-verification-result-store-summary-v0.schema.json", summary) == []


def test_stage5o_schemas_reject_guardrail_violations() -> None:
    run = _records("data/cuda/stage5o-gematria-solved-fixture-cuda-repeat-run.yaml")[0]
    run_schema = "gematria-solved-fixture-cuda-repeat-run-record-v0.schema.json"
    assert _errors(run_schema, {**run, "solve_claim": True})
    assert _errors(run_schema, {**run, "cuda_source_modified": True})

    result_store = _records("data/cuda/stage5o-gematria-cuda-result-store-preflight.yaml")[0]
    result_schema = "gematria-cuda-result-store-preflight-v0.schema.json"
    assert _errors(result_schema, {**result_store, "generated_outputs_committed": True})
    assert _errors(result_schema, {**result_store, "speedup_claim": True})

    summary = _yaml("data/cuda/stage5o-repeat-verification-result-store-summary.yaml")
    summary_schema = "stage5o-repeat-verification-result-store-summary-v0.schema.json"
    assert _errors(summary_schema, {**summary, "unsolved_page_cuda_used": True})
