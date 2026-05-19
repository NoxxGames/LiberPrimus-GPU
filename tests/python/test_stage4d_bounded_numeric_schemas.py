from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMAS = [
    "schemas/experiments/bounded-numeric-manifest-v0.schema.json",
    "schemas/experiments/bounded-numeric-result-record-v0.schema.json",
    "schemas/experiments/numeric-negative-control-result-v0.schema.json",
    "schemas/experiments/delimiter-handedness-audit-record-v0.schema.json",
]


def test_stage4d_bounded_numeric_schemas_validate() -> None:
    for schema_path in SCHEMAS:
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_stage4d_result_schema_requires_no_solve_claim_false() -> None:
    schema = json.loads(
        Path("schemas/experiments/bounded-numeric-result-record-v0.schema.json").read_text(
            encoding="utf-8"
        )
    )
    validator = Draft202012Validator(schema)
    payload = {
        "record_type": "bounded_numeric_result_record",
        "result_id": "synthetic",
        "execution_manifest_id": "exp_stage4b_onion7_raw_routes_v1",
        "audit_type": "number_square_raw_routes",
        "status": "skipped_missing_raw_values",
        "candidate_count": 0,
        "cap": 96,
        "raw_values": None,
        "derived_values": [],
        "no_fudge_policy": True,
        "solve_claim": False,
        "cuda_used": False,
        "trusted_as_canonical": False,
    }
    assert list(validator.iter_errors(payload)) == []
    payload["solve_claim"] = True
    assert list(validator.iter_errors(payload))
