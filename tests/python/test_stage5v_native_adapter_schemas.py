from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "schemas" / "cuda"


def _records(path: str) -> list[dict[str, object]]:
    payload = yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))
    return list(payload["records"])


def _mapping(path: str) -> dict[str, object]:
    return dict(yaml.safe_load((ROOT / path).read_text(encoding="utf-8")))


def _errors(schema_name: str, payload: dict[str, object]) -> list[str]:
    schema = json.loads((SCHEMA_DIR / schema_name).read_text(encoding="utf-8"))
    return [error.message for error in Draft202012Validator(schema).iter_errors(payload)]


def test_stage5v_committed_records_validate_against_schemas() -> None:
    cases = [
        ("native-candidate-batch-adapter-record-v0.schema.json", _records("data/cuda/stage5v-native-candidate-batch-adapter.yaml")),
        (
            "candidate-batch-conformance-fixture-record-v0.schema.json",
            _records("data/cuda/stage5v-candidate-batch-conformance-fixtures.yaml"),
        ),
        ("token-buffer-conformance-record-v0.schema.json", _records("data/cuda/stage5v-token-buffer-conformance.yaml")),
        ("schedule-conformance-record-v0.schema.json", _records("data/cuda/stage5v-schedule-conformance.yaml")),
        ("score-vector-conformance-record-v0.schema.json", _records("data/cuda/stage5v-score-vector-conformance.yaml")),
        ("topk-conformance-record-v0.schema.json", _records("data/cuda/stage5v-topk-conformance.yaml")),
        ("native-conformance-result-store-record-v0.schema.json", _records("data/cuda/stage5v-native-conformance-result-store.yaml")),
        (
            "candidate-batch-abi-implementation-status-record-v0.schema.json",
            _records("data/cuda/stage5v-abi-implementation-status.yaml"),
        ),
    ]
    for schema_name, records in cases:
        for record in records:
            assert _errors(schema_name, record) == []
    summary = _mapping("data/cuda/stage5v-native-candidate-batch-conformance-summary.yaml")
    assert _errors("stage5v-native-candidate-batch-conformance-summary-v0.schema.json", summary) == []


def test_stage5v_schemas_reject_cuda_and_solve_claim_drift() -> None:
    record = _records("data/cuda/stage5v-native-candidate-batch-adapter.yaml")[0]
    bad_cuda = {**record, "cuda_execution_performed": True}
    bad_solve = {**record, "solve_claim": True}
    assert _errors("native-candidate-batch-adapter-record-v0.schema.json", bad_cuda)
    assert _errors("native-candidate-batch-adapter-record-v0.schema.json", bad_solve)
