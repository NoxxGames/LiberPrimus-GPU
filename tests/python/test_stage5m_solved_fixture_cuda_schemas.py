from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator
import yaml


def _schema(name: str) -> dict[str, object]:
    return json.loads(Path("schemas/cuda", name).read_text(encoding="utf-8"))


def _records(path: str) -> list[dict[str, object]]:
    payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return payload["records"]


def _errors(schema_name: str, record: dict[str, object]) -> list[str]:
    validator = Draft202012Validator(_schema(schema_name))
    return [error.message for error in validator.iter_errors(record)]


def test_stage5m_committed_records_validate_against_schemas() -> None:
    cases = [
        (
            "gematria-solved-fixture-cuda-run-record-v0.schema.json",
            _records("data/cuda/stage5m-gematria-solved-fixture-cuda-run.yaml"),
        ),
        (
            "gematria-solved-fixture-cuda-parity-record-v0.schema.json",
            _records("data/cuda/stage5m-gematria-solved-fixture-cuda-parity.yaml"),
        ),
        (
            "gematria-solved-fixture-cuda-boundary-record-v0.schema.json",
            _records("data/cuda/stage5m-gematria-solved-fixture-cuda-boundaries.yaml"),
        ),
    ]
    for schema_name, records in cases:
        for record in records:
            assert _errors(schema_name, record) == []

    summary = yaml.safe_load(Path("data/cuda/stage5m-solved-fixture-cuda-parity-summary.yaml").read_text(encoding="utf-8"))
    assert _errors("stage5m-solved-fixture-cuda-parity-summary-v0.schema.json", summary) == []


def test_stage5m_schemas_reject_prohibited_true_flags() -> None:
    run_record = _records("data/cuda/stage5m-gematria-solved-fixture-cuda-run.yaml")[0]
    run_record = {**run_record, "solve_claim": True}
    assert _errors("gematria-solved-fixture-cuda-run-record-v0.schema.json", run_record)

    parity_record = _records("data/cuda/stage5m-gematria-solved-fixture-cuda-parity.yaml")[0]
    parity_record = {**parity_record, "unsolved_page_cuda_used": True}
    assert _errors("gematria-solved-fixture-cuda-parity-record-v0.schema.json", parity_record)

    summary = yaml.safe_load(Path("data/cuda/stage5m-solved-fixture-cuda-parity-summary.yaml").read_text(encoding="utf-8"))
    summary = {**summary, "new_cuda_kernels_added": 1}
    assert _errors("stage5m-solved-fixture-cuda-parity-summary-v0.schema.json", summary)
