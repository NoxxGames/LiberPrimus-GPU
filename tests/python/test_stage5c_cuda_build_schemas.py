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


def test_stage5c_committed_records_validate_against_schemas() -> None:
    fixtures = [
        ("cuda-build-profile-record-v0.schema.json", "data/cuda/stage5c-cuda-build-profiles.yaml"),
        ("cuda-toolchain-detection-record-v0.schema.json", "data/cuda/stage5c-cuda-toolchain-detection.yaml"),
        ("cuda-device-detection-record-v0.schema.json", "data/cuda/stage5c-cuda-device-detection.yaml"),
        ("cuda-smoke-build-record-v0.schema.json", "data/cuda/stage5c-cuda-smoke-build-records.yaml"),
    ]
    for schema_name, data_path in fixtures:
        payload = yaml.safe_load(Path(data_path).read_text(encoding="utf-8"))
        for record in payload["records"]:
            assert _validate(schema_name, record) == []

    summary = yaml.safe_load(Path("data/cuda/stage5c-cuda-build-device-summary.yaml").read_text(encoding="utf-8"))
    assert _validate("stage5c-cuda-build-device-summary-v0.schema.json", summary) == []


@pytest.mark.parametrize(
    ("schema_name", "field_name"),
    [
        ("cuda-build-profile-record-v0.schema.json", "cuda_kernel_added"),
        ("cuda-toolchain-detection-record-v0.schema.json", "gpu_benchmark_performed"),
        ("cuda-device-detection-record-v0.schema.json", "solve_claim"),
        ("cuda-smoke-build-record-v0.schema.json", "speedup_claim"),
        ("stage5c-cuda-build-device-summary-v0.schema.json", "website_expansion"),
    ],
)
def test_stage5c_schemas_reject_prohibited_true_flags(schema_name: str, field_name: str) -> None:
    payload = yaml.safe_load(Path("data/cuda/stage5c-cuda-build-device-summary.yaml").read_text(encoding="utf-8"))
    if schema_name != "stage5c-cuda-build-device-summary-v0.schema.json":
        source = {
            "cuda-build-profile-record-v0.schema.json": "data/cuda/stage5c-cuda-build-profiles.yaml",
            "cuda-toolchain-detection-record-v0.schema.json": "data/cuda/stage5c-cuda-toolchain-detection.yaml",
            "cuda-device-detection-record-v0.schema.json": "data/cuda/stage5c-cuda-device-detection.yaml",
            "cuda-smoke-build-record-v0.schema.json": "data/cuda/stage5c-cuda-smoke-build-records.yaml",
        }[schema_name]
        payload = yaml.safe_load(Path(source).read_text(encoding="utf-8"))["records"][0]
    payload[field_name] = True
    assert _validate(schema_name, payload)
