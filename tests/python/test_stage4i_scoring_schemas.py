from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMAS = [
    "schemas/scoring/scorer-record-v0.schema.json",
    "schemas/scoring/scoring-calibration-profile-v0.schema.json",
    "schemas/scoring/score-summary-record-v0.schema.json",
    "schemas/scoring/confidence-label-record-v0.schema.json",
    "schemas/scoring/scorer-compatibility-map-v0.schema.json",
    "schemas/scoring/scoring-calibration-report-v0.schema.json",
]


def test_stage4i_schemas_parse() -> None:
    for schema_path in SCHEMAS:
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_stage4i_score_summary_rejects_solve_claim_and_cuda() -> None:
    schema = json.loads(Path("schemas/scoring/score-summary-record-v0.schema.json").read_text(encoding="utf-8"))
    record = _score_summary()
    record["solve_claim"] = True
    assert list(Draft202012Validator(schema).iter_errors(record))
    record = _score_summary()
    record["cuda_used"] = True
    assert list(Draft202012Validator(schema).iter_errors(record))


def _score_summary() -> dict:
    return {
        "record_type": "score_summary_record",
        "scorer_id": "minimal_triage_v0",
        "scorer_version": "minimal-triage-score-v0",
        "input_stream_id": "stream-1",
        "candidate_id": "candidate-1",
        "transform_family": "direct_translation",
        "score_status": "scored",
        "score_value": 1.0,
        "score_components": {"total_score": 1.0},
        "calibration_profile_id": "stage4i-stage3c-minimal-triage-calibration-v0",
        "confidence_label": "noisy",
        "solve_claim": False,
        "trusted_as_canonical": False,
        "cuda_used": False,
    }
