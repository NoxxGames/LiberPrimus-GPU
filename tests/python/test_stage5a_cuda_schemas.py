from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMAS = [
    "schemas/cuda/cuda-target-plan-record-v0.schema.json",
    "schemas/cuda/cuda-parity-scaffold-record-v0.schema.json",
    "schemas/cuda/cuda-implementation-gate-record-v0.schema.json",
    "schemas/cuda/cuda-non-target-record-v0.schema.json",
    "schemas/cuda/cuda-planning-summary-v0.schema.json",
]


def test_stage5a_schemas_parse() -> None:
    for schema_path in SCHEMAS:
        Draft202012Validator.check_schema(_schema(schema_path))


def test_stage5a_target_schema_rejects_cuda_and_speedup_claims() -> None:
    validator = Draft202012Validator(_schema("schemas/cuda/cuda-target-plan-record-v0.schema.json"))
    for key, value in (
        ("cuda_implementation_added", True),
        ("cuda_kernel_added", True),
        ("gpu_benchmark_performed", True),
        ("speedup_claim", True),
        ("solve_claim", True),
    ):
        record = _target_record()
        record[key] = value
        assert list(validator.iter_errors(record)), key


def _schema(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _target_record() -> dict:
    return {
        "record_type": "cuda_target_plan",
        "stage_id": "stage-5a",
        "target_id": "stage5a-direct_translation-cuda-target",
        "source_readiness_id": "stage4q-direct_translation-cuda-parity-readiness",
        "transform_id": "direct_translation",
        "canonical_transform_id": "direct_translation",
        "transform_family": "direct_translation",
        "target_status": "ready_for_planning",
        "blockers": [],
        "cpu_reference_path": "python/libreprimus/cpu_batch/",
        "score_summary_contract": "stage4i",
        "stage4q_readiness_status": "ready_for_future_cuda_planning",
        "stage4o_parity_expectation_id": "stage4o-direct-an-v0",
        "stage4p_unified_result_reference": "stage4p-example",
        "output_text_hash": "a" * 64,
        "output_token_hash": "b" * 64,
        "score_summary_shape_hash": "c" * 64,
        "parity_contract_version": "stage4o-cpu-cuda-parity-v0",
        "no_raw_data_required": True,
        "broad_campaign_required": False,
        "notes": ["planning only"],
        "cuda_planning_only": True,
        "cuda_implementation_added": False,
        "cuda_kernel_added": False,
        "cuda_source_modified": False,
        "gpu_benchmark_performed": False,
        "performance_claim": False,
        "speedup_claim": False,
        "broad_experiment_executed": False,
        "raw_data_processed": False,
        "solve_claim": False,
        "no_solve_claim": True,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "generated_outputs_committed": False,
        "codex_output_committed": False,
        "cuda_used": False,
        "cuda_required": False,
    }
