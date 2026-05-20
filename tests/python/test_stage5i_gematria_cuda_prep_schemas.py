from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


SCHEMA_RECORDS = [
    ("gematria-cuda-kernel-preparation-record-v0.schema.json", "data/cuda/stage5i-gematria-cuda-kernel-preparation.yaml"),
    ("gematria-cuda-abi-plan-record-v0.schema.json", "data/cuda/stage5i-gematria-cuda-abi-plan.yaml"),
    ("gematria-cuda-validation-vector-record-v0.schema.json", "data/cuda/stage5i-gematria-cuda-validation-vectors.yaml"),
    ("gematria-cuda-implementation-checklist-record-v0.schema.json", "data/cuda/stage5i-gematria-cuda-implementation-checklist.yaml"),
]


def test_stage5i_schemas_validate_committed_records() -> None:
    for schema_name, record_path in SCHEMA_RECORDS:
        schema = json.loads(Path("schemas/cuda", schema_name).read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        payload = yaml.safe_load(Path(record_path).read_text(encoding="utf-8"))
        for record in payload["records"]:
            assert list(validator.iter_errors(record)) == []
    summary_schema = json.loads(Path("schemas/cuda/stage5i-gematria-cuda-preparation-summary-v0.schema.json").read_text(encoding="utf-8"))
    summary = yaml.safe_load(Path("data/cuda/stage5i-gematria-cuda-preparation-summary.yaml").read_text(encoding="utf-8"))
    assert list(Draft202012Validator(summary_schema).iter_errors(summary)) == []


def test_stage5i_schema_rejects_cuda_execution_claim() -> None:
    schema = json.loads(Path("schemas/cuda/gematria-cuda-kernel-preparation-record-v0.schema.json").read_text(encoding="utf-8"))
    payload = yaml.safe_load(Path("data/cuda/stage5i-gematria-cuda-kernel-preparation.yaml").read_text(encoding="utf-8"))["records"][0]
    payload["cuda_execution_performed"] = True
    assert list(Draft202012Validator(schema).iter_errors(payload))
