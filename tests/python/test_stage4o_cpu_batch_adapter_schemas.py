from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMAS = [
    "schemas/experiments/cpu-batch-adapter-coverage-v0.schema.json",
    "schemas/experiments/cpu-batch-parity-expectation-v0.schema.json",
    "schemas/experiments/cpu-batch-adapter-expansion-summary-v0.schema.json",
    "schemas/experiments/cpu-batch-solved-fixture-stream-v0.schema.json",
    "schemas/experiments/cpu-batch-scoring-compatibility-v0.schema.json",
]


def test_stage4o_schemas_parse() -> None:
    for schema_path in SCHEMAS:
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_stage4o_parity_schema_rejects_cuda_and_solve_claim() -> None:
    schema = json.loads(Path("schemas/experiments/cpu-batch-parity-expectation-v0.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    record = _parity_record()
    record["cuda_used"] = True
    assert list(validator.iter_errors(record))
    record = _parity_record()
    record["no_solve_claim"] = False
    assert list(validator.iter_errors(record))


def _parity_record() -> dict:
    return {
        "record_type": "cpu_batch_parity_expectation",
        "parity_contract_version": "stage4o-cpu-cuda-parity-v0",
        "input_stream_id": "stream",
        "candidate_id": "candidate",
        "transform_family": "direct_translation",
        "transform_id": "direct_translation",
        "parity_status": "passed",
        "output_token_hash": "0" * 64,
        "output_text_hash": "1" * 64,
        "transform_parameters_hash": "2" * 64,
        "cpu_only": True,
        "cuda_used": False,
        "cuda_required": False,
        "no_solve_claim": True,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "generated_outputs_committed": False,
    }
