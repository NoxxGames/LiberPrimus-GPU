from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator
import pytest
import yaml


SCHEMA_DIR = Path("schemas/native-cpu")


def _schema(name: str) -> dict[str, object]:
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def _validate(name: str, record: dict[str, object]) -> list[str]:
    validator = Draft202012Validator(_schema(name))
    return [error.message for error in validator.iter_errors(record)]


def test_stage5d_committed_records_validate_against_schemas() -> None:
    fixtures = [
        ("native-cpu-backend-capability-record-v0.schema.json", "data/native-cpu/stage5d-native-cpu-backend-capabilities.yaml"),
        ("native-cpu-threading-record-v0.schema.json", "data/native-cpu/stage5d-native-cpu-threading-records.yaml"),
        ("native-cpu-parity-record-v0.schema.json", "data/native-cpu/stage5d-native-cpu-parity-records.yaml"),
        ("native-cpu-diagnostic-record-v0.schema.json", "data/native-cpu/stage5d-native-cpu-diagnostic-records.yaml"),
    ]
    for schema_name, data_path in fixtures:
        payload = yaml.safe_load(Path(data_path).read_text(encoding="utf-8"))
        for record in payload["records"]:
            assert _validate(schema_name, record) == []

    summary = yaml.safe_load(Path("data/native-cpu/stage5d-native-cpu-summary.yaml").read_text(encoding="utf-8"))
    assert _validate("stage5d-native-cpu-summary-v0.schema.json", summary) == []


@pytest.mark.parametrize(
    ("schema_name", "source_path", "field_name"),
    [
        ("native-cpu-backend-capability-record-v0.schema.json", "data/native-cpu/stage5d-native-cpu-backend-capabilities.yaml", "cuda_used"),
        ("native-cpu-threading-record-v0.schema.json", "data/native-cpu/stage5d-native-cpu-threading-records.yaml", "gpu_benchmark_performed"),
        ("native-cpu-parity-record-v0.schema.json", "data/native-cpu/stage5d-native-cpu-parity-records.yaml", "solve_claim"),
        ("native-cpu-diagnostic-record-v0.schema.json", "data/native-cpu/stage5d-native-cpu-diagnostic-records.yaml", "speedup_claim"),
        ("stage5d-native-cpu-summary-v0.schema.json", "data/native-cpu/stage5d-native-cpu-summary.yaml", "cxx_launches_python_workers"),
    ],
)
def test_stage5d_schemas_reject_prohibited_true_flags(schema_name: str, source_path: str, field_name: str) -> None:
    payload = yaml.safe_load(Path(source_path).read_text(encoding="utf-8"))
    record = payload if schema_name == "stage5d-native-cpu-summary-v0.schema.json" else payload["records"][0]
    record[field_name] = True
    assert _validate(schema_name, record)
