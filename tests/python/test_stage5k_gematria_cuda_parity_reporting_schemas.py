from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator
import pytest
import yaml


SCHEMA_DIR = Path("schemas/cuda")


def _schema(name: str) -> dict[str, object]:
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def _validate(schema_name: str, record: dict[str, object]) -> list[str]:
    validator = Draft202012Validator(_schema(schema_name))
    return [error.message for error in validator.iter_errors(record)]


def _first_record(path: str) -> dict[str, object]:
    payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return payload["records"][0]


def test_stage5k_committed_records_validate_against_schemas() -> None:
    fixtures = [
        ("gematria-cuda-parity-report-record-v0.schema.json", "data/cuda/stage5k-gematria-cuda-parity-report.yaml"),
        (
            "gematria-cuda-device-code-audit-record-v0.schema.json",
            "data/cuda/stage5k-gematria-cuda-device-code-audit.yaml",
        ),
        (
            "gematria-solved-fixture-safe-preflight-record-v0.schema.json",
            "data/cuda/stage5k-gematria-solved-fixture-safe-preflight.yaml",
        ),
        (
            "gematria-cuda-score-summary-preflight-record-v0.schema.json",
            "data/cuda/stage5k-gematria-cuda-score-summary-preflight.yaml",
        ),
    ]
    for schema_name, data_path in fixtures:
        assert _validate(schema_name, _first_record(data_path)) == []

    summary = yaml.safe_load(
        Path("data/cuda/stage5k-gematria-cuda-parity-reporting-summary.yaml").read_text(encoding="utf-8")
    )
    assert _validate("stage5k-gematria-cuda-parity-reporting-summary-v0.schema.json", summary) == []


@pytest.mark.parametrize(
    ("schema_name", "source_path", "field_name"),
    [
        ("gematria-cuda-parity-report-record-v0.schema.json", "data/cuda/stage5k-gematria-cuda-parity-report.yaml", "solve_claim"),
        (
            "gematria-cuda-device-code-audit-record-v0.schema.json",
            "data/cuda/stage5k-gematria-cuda-device-code-audit.yaml",
            "stl_used_in_cuda_device_path",
        ),
        (
            "gematria-solved-fixture-safe-preflight-record-v0.schema.json",
            "data/cuda/stage5k-gematria-solved-fixture-safe-preflight.yaml",
            "solved_fixture_cuda_execution_allowed",
        ),
        (
            "gematria-cuda-score-summary-preflight-record-v0.schema.json",
            "data/cuda/stage5k-gematria-cuda-score-summary-preflight.yaml",
            "performance_claim",
        ),
        (
            "stage5k-gematria-cuda-parity-reporting-summary-v0.schema.json",
            "data/cuda/stage5k-gematria-cuda-parity-reporting-summary.yaml",
            "gpu_benchmark_performed",
        ),
    ],
)
def test_stage5k_schemas_reject_prohibited_true_flags(schema_name: str, source_path: str, field_name: str) -> None:
    payload = yaml.safe_load(Path(source_path).read_text(encoding="utf-8"))
    record = payload if schema_name.startswith("stage5k-") else payload["records"][0]
    record[field_name] = True
    assert _validate(schema_name, record)
