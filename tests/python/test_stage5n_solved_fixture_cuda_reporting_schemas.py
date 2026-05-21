from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator
import yaml


def _schema(name: str) -> dict[str, object]:
    return json.loads(Path("schemas/cuda", name).read_text(encoding="utf-8"))


def _records(path: str) -> list[dict[str, object]]:
    payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return payload["records"]


def _errors(schema_name: str, record: dict[str, object]) -> list[str]:
    validator = Draft202012Validator(_schema(schema_name))
    return [error.message for error in validator.iter_errors(record)]


def test_stage5n_committed_records_validate_against_schemas() -> None:
    cases = [
        ("gematria-solved-fixture-cuda-report-record-v0.schema.json", _records("data/cuda/stage5n-gematria-solved-fixture-cuda-report.yaml")),
        ("gematria-cuda-controlled-expansion-gate-record-v0.schema.json", _records("data/cuda/stage5n-gematria-controlled-expansion-gate.yaml")),
        ("gematria-cuda-boundary-review-record-v0.schema.json", _records("data/cuda/stage5n-gematria-cuda-boundary-review.yaml")),
        ("gematria-cuda-result-store-preflight-record-v0.schema.json", _records("data/cuda/stage5n-gematria-cuda-result-store-preflight.yaml")),
        ("gematria-no-unsolved-guardrail-record-v0.schema.json", _records("data/cuda/stage5n-gematria-no-unsolved-guardrail.yaml")),
    ]
    for schema_name, records in cases:
        for record in records:
            assert _errors(schema_name, record) == []

    summary = yaml.safe_load(Path("data/cuda/stage5n-solved-fixture-cuda-reporting-summary.yaml").read_text(encoding="utf-8"))
    assert _errors("stage5n-solved-fixture-cuda-reporting-summary-v0.schema.json", summary) == []


def test_stage5n_schemas_reject_solve_cuda_and_generated_publication_flags() -> None:
    parity = _records("data/cuda/stage5n-gematria-solved-fixture-cuda-report.yaml")[0]
    assert _errors("gematria-solved-fixture-cuda-report-record-v0.schema.json", {**parity, "solve_claim": True})
    assert _errors("gematria-solved-fixture-cuda-report-record-v0.schema.json", {**parity, "cuda_source_modified": True})

    summary = yaml.safe_load(Path("data/cuda/stage5n-solved-fixture-cuda-reporting-summary.yaml").read_text(encoding="utf-8"))
    assert _errors("stage5n-solved-fixture-cuda-reporting-summary-v0.schema.json", {**summary, "generated_outputs_committed": True})
