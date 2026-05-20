from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


SCHEMA_RECORDS = [
    ("gematria-shift-score-contract-record-v0.schema.json", "data/cuda/stage5h-gematria-shift-score-contract.yaml"),
    ("gematria-native-parity-fixture-record-v0.schema.json", "data/cuda/stage5h-gematria-native-parity-fixtures.yaml"),
    ("gematria-solved-fixture-safe-mapping-record-v0.schema.json", "data/cuda/stage5h-gematria-solved-fixture-safe-mapping.yaml"),
    ("gematria-score-summary-parity-plan-record-v0.schema.json", "data/cuda/stage5h-gematria-score-summary-parity-plan.yaml"),
]


def test_stage5h_schemas_validate_committed_records() -> None:
    for schema_name, record_path in SCHEMA_RECORDS:
        schema = json.loads(Path("schemas/cuda", schema_name).read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        payload = yaml.safe_load(Path(record_path).read_text(encoding="utf-8"))
        for record in payload["records"]:
            assert list(validator.iter_errors(record)) == []
    summary_schema = json.loads(Path("schemas/cuda/stage5h-gematria-shift-contract-summary-v0.schema.json").read_text(encoding="utf-8"))
    summary = yaml.safe_load(Path("data/cuda/stage5h-gematria-shift-contract-summary.yaml").read_text(encoding="utf-8"))
    assert list(Draft202012Validator(summary_schema).iter_errors(summary)) == []


def test_stage5h_schema_rejects_cuda_execution_claim() -> None:
    schema = json.loads(Path("schemas/cuda/gematria-shift-score-contract-record-v0.schema.json").read_text(encoding="utf-8"))
    payload = yaml.safe_load(Path("data/cuda/stage5h-gematria-shift-score-contract.yaml").read_text(encoding="utf-8"))["records"][0]
    payload["stage5h_cuda_execution_allowed"] = True
    assert list(Draft202012Validator(schema).iter_errors(payload))
