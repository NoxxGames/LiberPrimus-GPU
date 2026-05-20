from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from libreprimus.benchmark_planning.export import read_yaml


SCHEMAS = [
    "schemas/cuda/cuda-parity-harness-record-v0.schema.json",
    "schemas/cuda/cuda-parity-fixture-record-v0.schema.json",
    "schemas/cuda/cuda-backend-capability-record-v0.schema.json",
    "schemas/cuda/cuda-future-kernel-parity-matrix-v0.schema.json",
    "schemas/cuda/stage5b-cuda-parity-harness-summary-v0.schema.json",
]


def test_stage5b_schemas_parse() -> None:
    for schema_path in SCHEMAS:
        Draft202012Validator.check_schema(_schema(schema_path))


def test_stage5b_harness_schema_rejects_forbidden_true_flags() -> None:
    validator = Draft202012Validator(_schema("schemas/cuda/cuda-parity-harness-record-v0.schema.json"))
    record = _first_record("data/cuda/stage5b-cuda-parity-harness-plan.yaml")
    for key in (
        "cuda_kernel_added",
        "gpu_benchmark_performed",
        "speedup_claim",
        "solve_claim",
        "generated_outputs_committed",
        "codex_output_committed",
    ):
        mutated = copy.deepcopy(record)
        mutated[key] = True
        assert list(validator.iter_errors(mutated)), key


def test_stage5b_summary_schema_rejects_implementation_claims() -> None:
    validator = Draft202012Validator(_schema("schemas/cuda/stage5b-cuda-parity-harness-summary-v0.schema.json"))
    summary = read_yaml(Path("data/cuda/stage5b-cuda-parity-harness-summary.yaml"))
    for key in ("cuda_implementation_added", "performance_claim", "website_expansion"):
        mutated = copy.deepcopy(summary)
        mutated[key] = True
        assert list(validator.iter_errors(mutated)), key


def _schema(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _first_record(path: str) -> dict:
    return read_yaml(Path(path))["records"][0]
