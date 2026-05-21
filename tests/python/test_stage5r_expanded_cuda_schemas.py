from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
import yaml


def _schema(name: str) -> dict[str, Any]:
    return json.loads(Path("schemas/cuda", name).read_text(encoding="utf-8"))


def _records(path: str) -> list[dict[str, Any]]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"]


def _yaml(path: str) -> dict[str, Any]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def _errors(schema_name: str, record: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(_schema(schema_name))
    return [error.message for error in validator.iter_errors(record)]


def test_stage5r_committed_records_validate_against_schemas() -> None:
    cases = [
        (
            "gematria-expanded-solved-fixture-cuda-run-record-v0.schema.json",
            _records("data/cuda/stage5r-gematria-expanded-solved-fixture-cuda-run.yaml"),
        ),
        (
            "gematria-expanded-solved-fixture-cuda-parity-record-v0.schema.json",
            _records("data/cuda/stage5r-gematria-expanded-solved-fixture-cuda-parity.yaml"),
        ),
        (
            "gematria-expanded-solved-fixture-cuda-boundary-record-v0.schema.json",
            _records("data/cuda/stage5r-gematria-expanded-solved-fixture-cuda-boundary.yaml"),
        ),
        (
            "gematria-expanded-solved-fixture-result-store-preflight-record-v0.schema.json",
            _records("data/cuda/stage5r-gematria-expanded-solved-fixture-result-store-preflight.yaml"),
        ),
        (
            "gematria-expanded-solved-fixture-score-summary-preflight-record-v0.schema.json",
            _records("data/cuda/stage5r-gematria-expanded-solved-fixture-score-summary-preflight.yaml"),
        ),
    ]
    for schema_name, records in cases:
        for record in records:
            assert _errors(schema_name, record) == []

    summary = _yaml("data/cuda/stage5r-expanded-solved-fixture-cuda-parity-summary.yaml")
    assert _errors("stage5r-expanded-solved-fixture-cuda-parity-summary-v0.schema.json", summary) == []


def test_stage5r_schemas_reject_guardrail_violations() -> None:
    run = _records("data/cuda/stage5r-gematria-expanded-solved-fixture-cuda-run.yaml")[0]
    run_schema = "gematria-expanded-solved-fixture-cuda-run-record-v0.schema.json"
    assert _errors(run_schema, {**run, "solve_claim": True})
    assert _errors(run_schema, {**run, "unsolved_page_cuda_used": True})
    assert _errors(run_schema, {**run, "real_liber_primus_cuda_data_used": True})
    assert _errors(run_schema, {**run, "new_cuda_kernels_added": 1})
    assert _errors(run_schema, {**run, "gpu_benchmark_performed": True})
    assert _errors(run_schema, {**run, "speedup_claim": True})

    summary = _yaml("data/cuda/stage5r-expanded-solved-fixture-cuda-parity-summary.yaml")
    summary_schema = "stage5r-expanded-solved-fixture-cuda-parity-summary-v0.schema.json"
    assert _errors(summary_schema, {**summary, "generated_outputs_committed": True})
    assert _errors(summary_schema, {**summary, "raw_data_processed": True})
    assert _errors(summary_schema, {**summary, "codex_output_committed": True})


def test_stage5r_score_summary_schema_uses_stage4i_label_vocabulary() -> None:
    score = _records("data/cuda/stage5r-gematria-expanded-solved-fixture-score-summary-preflight.yaml")[0]
    schema_name = "gematria-expanded-solved-fixture-score-summary-preflight-record-v0.schema.json"
    assert _errors(schema_name, score) == []
    assert _errors(schema_name, {**score, "confidence_label": "solve_evidence"})
