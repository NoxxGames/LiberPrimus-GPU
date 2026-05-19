from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMAS = [
    "schemas/visual/image-source-variant-preflight-record-v0.schema.json",
    "schemas/visual/image-compression-preflight-record-v0.schema.json",
    "schemas/visual/image-artifact-review-candidate-v0.schema.json",
    "schemas/visual/image-preflight-summary-v0.schema.json",
    "schemas/experiments/bigram-frequency-pattern-readiness-v0.schema.json",
]


def test_stage4m_schemas_parse() -> None:
    for schema_path in SCHEMAS:
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_stage4m_compression_schema_rejects_solve_claim() -> None:
    schema = json.loads(Path("schemas/visual/image-compression-preflight-record-v0.schema.json").read_text())
    validator = Draft202012Validator(schema)
    record = _compression_record()
    record["solve_claim"] = True
    assert list(validator.iter_errors(record))


def _compression_record() -> dict:
    return {
        "record_type": "image_compression_preflight_record",
        "compression_record_id": "stage4m-test",
        "image_id": "image-test",
        "relative_path": "third_party/LiberPrimusPages/test.jpg",
        "file_name": "test.jpg",
        "sha256": "0" * 64,
        "compression_metric_status": "computed",
        "metric_only": True,
        "jpeg_like_metric_flag": False,
        "raw_image_committed": False,
        "generated_image_committed": False,
        "solve_claim": False,
        "trusted_as_canonical": False,
        "usable_as_experiment_seed": False,
        "image_interpretation_claim": False,
    }
