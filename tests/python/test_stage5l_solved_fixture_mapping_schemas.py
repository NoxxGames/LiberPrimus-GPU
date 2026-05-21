from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from libreprimus.gematria_solved_fixture_mapping.export import read_record_set
from libreprimus.paths import repo_root


def test_stage5l_schemas_validate_committed_records() -> None:
    root = repo_root()
    cases = [
        (
            root / "schemas/cuda/gematria-solved-fixture-token-mapping-record-v0.schema.json",
            read_record_set(root / "data/cuda/stage5l-gematria-solved-fixture-token-mapping.yaml"),
        ),
        (
            root / "schemas/cuda/gematria-solved-fixture-native-parity-record-v0.schema.json",
            read_record_set(root / "data/cuda/stage5l-gematria-solved-fixture-native-parity.yaml"),
        ),
        (
            root / "schemas/cuda/gematria-solved-fixture-output-hash-contract-v0.schema.json",
            read_record_set(root / "data/cuda/stage5l-gematria-solved-fixture-output-hash-contract.yaml"),
        ),
        (
            root / "schemas/cuda/gematria-solved-fixture-score-summary-shape-v0.schema.json",
            read_record_set(root / "data/cuda/stage5l-gematria-solved-fixture-score-summary-shape.yaml"),
        ),
    ]
    for schema_path, records in cases:
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        for record in records:
            assert list(validator.iter_errors(record)) == []


def test_stage5l_schema_rejects_cuda_execution() -> None:
    schema_path = repo_root() / "schemas/cuda/gematria-solved-fixture-token-mapping-record-v0.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    record = read_record_set(repo_root() / "data/cuda/stage5l-gematria-solved-fixture-token-mapping.yaml")[0]
    record = {**record, "cuda_execution_performed": True}
    assert list(Draft202012Validator(schema).iter_errors(record))
