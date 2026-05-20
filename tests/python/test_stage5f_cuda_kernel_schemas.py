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


def test_stage5f_committed_records_validate_against_schemas() -> None:
    fixtures = [
        (
            "cuda-synthetic-kernel-implementation-record-v0.schema.json",
            "data/cuda/stage5f-cuda-synthetic-kernel-implementation.yaml",
        ),
        ("cuda-kernel-build-record-v0.schema.json", "data/cuda/stage5f-cuda-kernel-build-records.yaml"),
        ("cuda-synthetic-parity-run-record-v0.schema.json", "data/cuda/stage5f-cuda-synthetic-parity-records.yaml"),
    ]
    for schema_name, data_path in fixtures:
        assert _validate(schema_name, _first_record(data_path)) == []

    summary = yaml.safe_load(Path("data/cuda/stage5f-cuda-synthetic-kernel-summary.yaml").read_text(encoding="utf-8"))
    assert _validate("stage5f-synthetic-cuda-kernel-summary-v0.schema.json", summary) == []


@pytest.mark.parametrize(
    ("schema_name", "source_path", "field_name"),
    [
        (
            "cuda-synthetic-kernel-implementation-record-v0.schema.json",
            "data/cuda/stage5f-cuda-synthetic-kernel-implementation.yaml",
            "real_liber_primus_data_used",
        ),
        ("cuda-kernel-build-record-v0.schema.json", "data/cuda/stage5f-cuda-kernel-build-records.yaml", "gpu_benchmark_performed"),
        ("cuda-synthetic-parity-run-record-v0.schema.json", "data/cuda/stage5f-cuda-synthetic-parity-records.yaml", "solve_claim"),
        (
            "stage5f-synthetic-cuda-kernel-summary-v0.schema.json",
            "data/cuda/stage5f-cuda-synthetic-kernel-summary.yaml",
            "speedup_claim",
        ),
    ],
)
def test_stage5f_schemas_reject_prohibited_true_flags(schema_name: str, source_path: str, field_name: str) -> None:
    payload = yaml.safe_load(Path(source_path).read_text(encoding="utf-8"))
    record = payload if schema_name == "stage5f-synthetic-cuda-kernel-summary-v0.schema.json" else payload["records"][0]
    record[field_name] = True
    assert _validate(schema_name, record)


def test_stage5f_schema_requires_selected_kernel() -> None:
    record = _first_record("data/cuda/stage5f-cuda-synthetic-kernel-implementation.yaml")
    record["selected_kernel_id"] = "other_kernel"
    assert _validate("cuda-synthetic-kernel-implementation-record-v0.schema.json", record)
