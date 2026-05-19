from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMAS = [
    "schemas/stego/stego-positive-control-readiness-v0.schema.json",
    "schemas/stego/audio-positive-control-readiness-v0.schema.json",
    "schemas/stego/stego-fixture-cache-record-v0.schema.json",
    "schemas/stego/stego-expected-output-record-v0.schema.json",
    "schemas/stego/stego-toolchain-readiness-v0.schema.json",
    "schemas/stego/stego-positive-control-summary-v0.schema.json",
]


def test_stage4n_schemas_parse() -> None:
    for schema_path in SCHEMAS:
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_stage4n_schema_rejects_solve_claim() -> None:
    schema = json.loads(Path("schemas/stego/stego-positive-control-readiness-v0.schema.json").read_text())
    validator = Draft202012Validator(schema)
    record = _readiness_record()
    record["solve_claim"] = True
    assert list(validator.iter_errors(record))


def _readiness_record() -> dict:
    return {
        "record_type": "stego_positive_control_readiness",
        "readiness_id": "stage4n-test",
        "source_record_id": "source-test",
        "fixture_category": "outguess_known_positive_candidate",
        "ready_state": "blocked_expected_output_unknown",
        "expected_output_required": True,
        "raw_file_committed": False,
        "binary_committed": False,
        "image_committed": False,
        "audio_committed": False,
        "font_committed": False,
        "archive_committed": False,
        "extracted_payload_committed": False,
        "solve_claim": False,
        "execution_performed": False,
        "tool_executed": False,
    }
