from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMAS = [
    "schemas/history/source-delta-audit-record-v0.schema.json",
    "schemas/history/source-path-candidate-record-v0.schema.json",
    "schemas/history/source-variant-comparison-record-v0.schema.json",
    "schemas/visual/image-compression-artifact-observation-v0.schema.json",
    "schemas/experiments/future-image-artifact-manifest-v0.schema.json",
]


def test_stage4e_schemas_parse() -> None:
    for schema_path in SCHEMAS:
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_stage4e_source_delta_schema_rejects_raw_file_committed() -> None:
    schema = json.loads(Path("schemas/history/source-delta-audit-record-v0.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    record = {
        "record_type": "source_delta_audit_record",
        "audit_id": "bad",
        "source_id": "source",
        "repo_url": "https://example.invalid/repo.git",
        "remote_head": None,
        "path_count": 0,
        "source_class": "strong_community_technical",
        "recommended_action": "defer",
        "raw_file_committed": True,
        "binary_committed": False,
        "font_committed": False,
        "trusted_as_canonical": False,
        "solve_claim": False,
    }
    assert list(validator.iter_errors(record))
