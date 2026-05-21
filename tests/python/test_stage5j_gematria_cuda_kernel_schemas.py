from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from libreprimus.benchmark_planning.export import read_yaml


SCHEMA_FILES = [
    Path("schemas/cuda/gematria-cuda-kernel-implementation-record-v0.schema.json"),
    Path("schemas/cuda/gematria-cuda-kernel-build-record-v0.schema.json"),
    Path("schemas/cuda/gematria-cuda-synthetic-parity-record-v0.schema.json"),
    Path("schemas/cuda/stage5j-gematria-cuda-kernel-summary-v0.schema.json"),
]


def test_stage5j_schemas_parse() -> None:
    for schema_path in SCHEMA_FILES:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_stage5j_committed_records_validate_against_schemas() -> None:
    pairs = [
        (
            Path("data/cuda/stage5j-gematria-cuda-kernel-implementation.yaml"),
            Path("schemas/cuda/gematria-cuda-kernel-implementation-record-v0.schema.json"),
        ),
        (
            Path("data/cuda/stage5j-gematria-cuda-kernel-build-records.yaml"),
            Path("schemas/cuda/gematria-cuda-kernel-build-record-v0.schema.json"),
        ),
        (
            Path("data/cuda/stage5j-gematria-cuda-synthetic-parity-records.yaml"),
            Path("schemas/cuda/gematria-cuda-synthetic-parity-record-v0.schema.json"),
        ),
    ]
    for payload_path, schema_path in pairs:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        for record in read_yaml(payload_path)["records"]:
            assert list(validator.iter_errors(record)) == []

    summary_schema = json.loads(Path("schemas/cuda/stage5j-gematria-cuda-kernel-summary-v0.schema.json").read_text(encoding="utf-8"))
    assert list(Draft202012Validator(summary_schema).iter_errors(read_yaml(Path("data/cuda/stage5j-gematria-cuda-kernel-summary.yaml")))) == []
