from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMAS = [
    "schemas/benchmarks/cpu-benchmark-plan-v0.schema.json",
    "schemas/benchmarks/cpu-benchmark-smoke-record-v0.schema.json",
    "schemas/benchmarks/benchmark-environment-record-v0.schema.json",
    "schemas/benchmarks/cuda-parity-benchmark-readiness-v0.schema.json",
    "schemas/benchmarks/stage4q-benchmark-parity-summary-v0.schema.json",
]


def test_stage4q_schemas_parse() -> None:
    for schema_path in SCHEMAS:
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_stage4q_readiness_schema_rejects_cuda_and_solve_claims() -> None:
    validator = Draft202012Validator(_schema("schemas/benchmarks/cuda-parity-benchmark-readiness-v0.schema.json"))
    for key, value in (("cuda_used", True), ("solve_claim", True), ("gpu_benchmark_performed", True)):
        record = _readiness_record()
        record[key] = value
        assert list(validator.iter_errors(record)), key


def _schema(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _readiness_record() -> dict:
    return {
        "record_type": "cuda_parity_benchmark_readiness",
        "readiness_id": "stage4q-direct-cuda-parity-readiness",
        "stage_id": "stage-4q",
        "transform_family": "direct_translation",
        "benchmark_scope": "parity_readiness",
        "benchmark_status": "planned",
        "parity_gate_status": "ready_for_future_cuda_planning",
        "blockers": [],
        "cpu_reference_present": True,
        "stage4o_parity_expectation_available": True,
        "stage4p_unified_result_surface_available": True,
        "cpu_only": True,
        "cuda_used": False,
        "cuda_required": False,
        "gpu_benchmark_performed": False,
        "cuda_implementation_added": False,
        "no_solve_claim": True,
        "solve_claim": False,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "generated_outputs_committed": False,
        "raw_data_processed": False,
        "broad_experiment_executed": False,
    }
