from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

REPO = Path(__file__).resolve().parents[2]


def test_stage3p_schemas_validate_as_json_schema() -> None:
    for name in [
        "image-transform-record-v0.schema.json",
        "image-transform-metric-record-v0.schema.json",
        "visual-transform-candidate-v0.schema.json",
        "contact-sheet-record-v0.schema.json",
        "image-transform-run-summary-v0.schema.json",
    ]:
        schema = json.loads((REPO / "schemas/visual" / name).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_stage3p_candidate_schema_rejects_seed_and_solve_flags() -> None:
    schema = json.loads((REPO / "schemas/visual/visual-transform-candidate-v0.schema.json").read_text(encoding="utf-8"))
    payload = {
        "record_type": "visual_transform_candidate",
        "candidate_id": "synthetic-sparse",
        "image_id": "synthetic",
        "feature_type": "sparse_dot_like_candidate",
        "transform_names": ["threshold_64"],
        "feature_score": 0.5,
        "evidence_fields": {},
        "review_status": "human_review_required",
        "output_references": ["experiments/results/image-transforms/stage3p/derived_images/synthetic/threshold_64.png"],
        "trusted_as_canonical": False,
        "usable_as_experiment_seed": False,
        "solve_claim": False,
        "notes": "review only",
    }
    errors = list(Draft202012Validator(schema).iter_errors(payload))
    assert errors == []

    payload["usable_as_experiment_seed"] = True
    errors = list(Draft202012Validator(schema).iter_errors(payload))
    assert errors
