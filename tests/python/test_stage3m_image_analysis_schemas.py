from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

REPO = Path(__file__).resolve().parents[2]


def _schema(path: str) -> dict:
    return json.loads((REPO / path).read_text(encoding="utf-8"))


def test_image_analysis_record_schema_rejects_solve_claim() -> None:
    schema = _schema("schemas/visual/image-analysis-record-v0.schema.json")
    payload = {
        "record_type": "image_analysis_record",
        "image_id": "synthetic",
        "source_id": "source",
        "image_sha256": "a" * 64,
        "relative_path": "synthetic.png",
        "file_name": "synthetic.png",
        "width": 1,
        "height": 1,
        "image_format": "PNG",
        "color_mode": "L",
        "grayscale_min": 0,
        "grayscale_max": 0,
        "grayscale_mean": 0.0,
        "grayscale_stddev": 0.0,
        "black_pixel_ratio": 1.0,
        "white_pixel_ratio": 0.0,
        "midtone_ratio": 0.0,
        "trusted_as_canonical": False,
        "solve_claim": True,
        "notes": "",
    }

    errors = list(Draft202012Validator(schema).iter_errors(payload))

    assert errors


def test_visual_feature_candidate_schema_requires_non_seed() -> None:
    schema = _schema("schemas/visual/visual-feature-candidate-v0.schema.json")
    usable_schema = schema["properties"]["usable_as_experiment_seed"]

    assert usable_schema == {"const": False}
    assert schema["properties"]["trusted_as_canonical"] == {"const": False}
    assert schema["properties"]["solve_claim"] == {"const": False}
