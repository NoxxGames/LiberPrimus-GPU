from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMAS = [
    "schemas/stego/stego-fixture-source-record-v0.schema.json",
    "schemas/stego/audio-fixture-source-record-v0.schema.json",
    "schemas/stego/historical-stego-fixture-manifest-v0.schema.json",
    "schemas/stego/fixture-source-health-record-v0.schema.json",
    "schemas/stego/toolchain-requirement-record-v0.schema.json",
]


def test_stage4f_schemas_parse() -> None:
    for schema_path in SCHEMAS:
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_stage4f_stego_schema_rejects_raw_committed_flags() -> None:
    schema = json.loads(Path("schemas/stego/stego-fixture-source-record-v0.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    record = {
        "record_type": "stego_fixture_source_record",
        "fixture_id": "bad",
        "source_id": "source",
        "source_url": "https://example.invalid/file.jpg",
        "source_path": "file.jpg",
        "artifact_type": "image_fixture_candidate",
        "expected_role": "known_positive_candidate",
        "local_availability": "source_only",
        "toolchain": ["outguess"],
        "raw_file_committed": True,
        "binary_committed": False,
        "audio_committed": False,
        "image_committed": False,
        "extracted_payload_committed": False,
        "font_committed": False,
        "trusted_as_canonical": False,
        "solve_claim": False,
    }
    assert list(validator.iter_errors(record))


def test_stage4f_audio_schema_rejects_binary_audio_image_font_flags() -> None:
    schema = json.loads(Path("schemas/stego/audio-fixture-source-record-v0.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    base = {
        "record_type": "audio_fixture_source_record",
        "fixture_id": "bad",
        "source_id": "source",
        "source_url": "https://example.invalid/file.mp3",
        "source_path": "file.mp3",
        "artifact_type": "audio_fixture_candidate",
        "expected_role": "known_positive_candidate",
        "local_availability": "source_only",
        "toolchain": ["mp3stego"],
        "raw_file_committed": False,
        "binary_committed": False,
        "audio_committed": False,
        "image_committed": False,
        "extracted_payload_committed": False,
        "font_committed": False,
        "trusted_as_canonical": False,
        "solve_claim": False,
    }
    for key in ("binary_committed", "audio_committed", "image_committed", "font_committed"):
        record = dict(base)
        record[key] = True
        assert list(validator.iter_errors(record)), key
