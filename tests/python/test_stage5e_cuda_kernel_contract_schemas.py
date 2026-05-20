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


def test_stage5e_committed_records_validate_against_schemas() -> None:
    fixtures = [
        ("cuda-first-kernel-contract-record-v0.schema.json", "data/cuda/stage5e-first-kernel-contract.yaml"),
        ("cuda-adapter-selection-record-v0.schema.json", "data/cuda/stage5e-cuda-adapter-selection.yaml"),
        ("cuda-native-parity-adapter-record-v0.schema.json", "data/cuda/stage5e-native-parity-adapter-map.yaml"),
        ("cuda-implementation-readiness-record-v0.schema.json", "data/cuda/stage5e-implementation-readiness.yaml"),
    ]
    for schema_name, data_path in fixtures:
        payload = yaml.safe_load(Path(data_path).read_text(encoding="utf-8"))
        for record in payload["records"]:
            assert _validate(schema_name, record) == []

    summary = yaml.safe_load(Path("data/cuda/stage5e-first-kernel-contract-summary.yaml").read_text(encoding="utf-8"))
    assert _validate("stage5e-first-kernel-contract-summary-v0.schema.json", summary) == []


@pytest.mark.parametrize(
    ("schema_name", "source_path", "field_name"),
    [
        ("cuda-first-kernel-contract-record-v0.schema.json", "data/cuda/stage5e-first-kernel-contract.yaml", "cuda_kernel_added"),
        ("cuda-adapter-selection-record-v0.schema.json", "data/cuda/stage5e-cuda-adapter-selection.yaml", "cuda_source_modified"),
        ("cuda-native-parity-adapter-record-v0.schema.json", "data/cuda/stage5e-native-parity-adapter-map.yaml", "gpu_benchmark_performed"),
        ("cuda-implementation-readiness-record-v0.schema.json", "data/cuda/stage5e-implementation-readiness.yaml", "solve_claim"),
        ("stage5e-first-kernel-contract-summary-v0.schema.json", "data/cuda/stage5e-first-kernel-contract-summary.yaml", "speedup_claim"),
    ],
)
def test_stage5e_schemas_reject_prohibited_true_flags(schema_name: str, source_path: str, field_name: str) -> None:
    payload = yaml.safe_load(Path(source_path).read_text(encoding="utf-8"))
    record = payload if schema_name == "stage5e-first-kernel-contract-summary-v0.schema.json" else payload["records"][0]
    record[field_name] = True
    assert _validate(schema_name, record)
