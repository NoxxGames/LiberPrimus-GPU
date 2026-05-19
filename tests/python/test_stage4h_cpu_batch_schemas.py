from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from libreprimus.cpu_batch.parity_contract import parity_contract_record


SCHEMAS = [
    "schemas/experiments/cpu-batch-manifest-v0.schema.json",
    "schemas/experiments/cpu-batch-input-stream-v0.schema.json",
    "schemas/experiments/cpu-batch-transform-candidate-v0.schema.json",
    "schemas/experiments/cpu-batch-result-record-v0.schema.json",
    "schemas/experiments/cpu-batch-run-summary-v0.schema.json",
    "schemas/experiments/cpu-cuda-parity-contract-v0.schema.json",
]


def test_stage4h_schemas_parse() -> None:
    for schema_path in SCHEMAS:
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_stage4h_result_schema_enforces_cpu_only_flags() -> None:
    schema = json.loads(
        Path("schemas/experiments/cpu-batch-result-record-v0.schema.json").read_text(
            encoding="utf-8"
        )
    )
    record = _result_record()
    record["cuda_used"] = True
    assert list(Draft202012Validator(schema).iter_errors(record))


def test_stage4h_parity_schema_accepts_contract_record() -> None:
    schema = json.loads(
        Path("schemas/experiments/cpu-cuda-parity-contract-v0.schema.json").read_text(
            encoding="utf-8"
        )
    )
    assert not list(Draft202012Validator(schema).iter_errors(parity_contract_record()))


def _result_record() -> dict:
    return {
        "record_type": "cpu_batch_result_record",
        "run_id": "run-1",
        "manifest_id": "manifest-1",
        "candidate_id": "candidate-1",
        "input_stream_id": "stream-1",
        "transform_family": "direct_translation",
        "transform_id": "direct_translation",
        "canonical_transform_id": "direct_translation",
        "transform_parameters": {},
        "execution_status": "executed",
        "adapter_status": "executed",
        "token_count": 1,
        "transformable_token_count": 1,
        "output_text": "F",
        "output_text_hash": "f" * 64,
        "output_token_hash": "0" * 64,
        "score_summary": {"score_status": "scoring_disabled"},
        "warnings": [],
        "cpu_only": True,
        "cuda_used": False,
        "cuda_required": False,
        "no_solve_claim": True,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "generated_outputs_committed": False,
    }
