from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator
import pytest
import yaml


SCHEMA_DIR = Path("schemas/cuda")


def _schema(name: str) -> dict[str, object]:
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def _validate(name: str, record: dict[str, object]) -> list[str]:
    validator = Draft202012Validator(_schema(name))
    return [error.message for error in validator.iter_errors(record)]


def _first_record(path: str) -> dict[str, object]:
    payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return payload["records"][0]


def test_stage5g_committed_records_validate_against_schemas() -> None:
    fixtures = [
        ("cuda-shift-score-parity-report-record-v0.schema.json", "data/cuda/stage5g-shift-score-parity-report.yaml"),
        ("cuda-device-code-subset-audit-record-v0.schema.json", "data/cuda/stage5g-cuda-device-code-subset-audit.yaml"),
        (
            "cuda-solved-fixture-safe-preflight-record-v0.schema.json",
            "data/cuda/stage5g-solved-fixture-safe-adapter-preflight.yaml",
        ),
    ]
    for schema_name, data_path in fixtures:
        assert _validate(schema_name, _first_record(data_path)) == []

    summary = yaml.safe_load(Path("data/cuda/stage5g-cuda-parity-reporting-summary.yaml").read_text(encoding="utf-8"))
    assert _validate("stage5g-cuda-parity-reporting-summary-v0.schema.json", summary) == []


@pytest.mark.parametrize(
    ("schema_name", "source_path", "field_name"),
    [
        ("cuda-shift-score-parity-report-record-v0.schema.json", "data/cuda/stage5g-shift-score-parity-report.yaml", "solve_claim"),
        ("cuda-device-code-subset-audit-record-v0.schema.json", "data/cuda/stage5g-cuda-device-code-subset-audit.yaml", "stl_used_in_cuda_device_path"),
        (
            "cuda-solved-fixture-safe-preflight-record-v0.schema.json",
            "data/cuda/stage5g-solved-fixture-safe-adapter-preflight.yaml",
            "production_gematria_mod29_cuda_ready",
        ),
        (
            "stage5g-cuda-parity-reporting-summary-v0.schema.json",
            "data/cuda/stage5g-cuda-parity-reporting-summary.yaml",
            "gpu_benchmark_performed",
        ),
    ],
)
def test_stage5g_schemas_reject_prohibited_true_flags(schema_name: str, source_path: str, field_name: str) -> None:
    payload = yaml.safe_load(Path(source_path).read_text(encoding="utf-8"))
    record = payload if schema_name == "stage5g-cuda-parity-reporting-summary-v0.schema.json" else payload["records"][0]
    record[field_name] = True
    assert _validate(schema_name, record)
