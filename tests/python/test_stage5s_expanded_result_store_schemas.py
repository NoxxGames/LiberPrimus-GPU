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


def test_stage5s_committed_records_validate_against_schemas() -> None:
    cases = [
        (
            "gematria-expanded-cuda-parity-report-record-v0.schema.json",
            _records("data/cuda/stage5s-gematria-expanded-cuda-parity-report.yaml"),
        ),
        (
            "gematria-expanded-cuda-result-store-integration-record-v0.schema.json",
            _records("data/cuda/stage5s-gematria-expanded-cuda-result-store-integration.yaml"),
        ),
        (
            "gematria-expanded-cuda-score-summary-integration-record-v0.schema.json",
            _records("data/cuda/stage5s-gematria-expanded-cuda-score-summary-integration.yaml"),
        ),
        (
            "gematria-expanded-cuda-method-status-impact-record-v0.schema.json",
            _records("data/cuda/stage5s-gematria-expanded-cuda-method-status-impact.yaml"),
        ),
        (
            "gematria-expanded-cuda-generated-body-policy-record-v0.schema.json",
            _records("data/cuda/stage5s-gematria-expanded-cuda-generated-body-policy.yaml"),
        ),
        (
            "gematria-expanded-cuda-boundary-review-record-v0.schema.json",
            _records("data/cuda/stage5s-gematria-expanded-cuda-boundary-review.yaml"),
        ),
        (
            "gematria-expanded-cuda-next-step-decision-record-v0.schema.json",
            _records("data/cuda/stage5s-gematria-expanded-cuda-next-step-decision.yaml"),
        ),
    ]
    for schema_name, records in cases:
        for record in records:
            assert _errors(schema_name, record) == []

    summary = _yaml("data/cuda/stage5s-expanded-cuda-result-store-integration-summary.yaml")
    assert _errors("stage5s-expanded-cuda-result-store-integration-summary-v0.schema.json", summary) == []


def test_stage5s_schemas_reject_core_guardrail_violations() -> None:
    parity = _records("data/cuda/stage5s-gematria-expanded-cuda-parity-report.yaml")[0]
    parity_schema = "gematria-expanded-cuda-parity-report-record-v0.schema.json"
    assert _errors(parity_schema, {**parity, "solve_claim": True})
    assert _errors(parity_schema, {**parity, "cuda_execution_performed": True})
    assert _errors(parity_schema, {**parity, "gpu_benchmark_performed": True})
    assert _errors(parity_schema, {**parity, "speedup_claim": True})

    score = _records("data/cuda/stage5s-gematria-expanded-cuda-score-summary-integration.yaml")[0]
    score_schema = "gematria-expanded-cuda-score-summary-integration-record-v0.schema.json"
    assert _errors(score_schema, {**score, "confidence_label": "plaintext_verified"})

    summary = _yaml("data/cuda/stage5s-expanded-cuda-result-store-integration-summary.yaml")
    summary_schema = "stage5s-expanded-cuda-result-store-integration-summary-v0.schema.json"
    assert _errors(summary_schema, {**summary, "method_status_upgrade_allowed": True})
