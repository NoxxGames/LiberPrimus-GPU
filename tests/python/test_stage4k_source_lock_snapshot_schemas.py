from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMAS = [
    "schemas/history/source-lock-snapshot-record-v0.schema.json",
    "schemas/history/source-lock-snapshot-summary-v0.schema.json",
    "schemas/history/public-source-lock-policy-v0.schema.json",
    "schemas/history/source-fetch-record-v0.schema.json",
    "schemas/history/source-copyright-policy-record-v0.schema.json",
]


def test_stage4k_schemas_parse() -> None:
    for schema_path in SCHEMAS:
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_stage4k_snapshot_schema_rejects_raw_binary_font_and_solve_claim() -> None:
    schema = json.loads(Path("schemas/history/source-lock-snapshot-record-v0.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    for key in ("raw_private_data_committed", "binary_committed", "font_committed", "solve_claim"):
        record = _snapshot_record()
        record[key] = True
        assert list(validator.iter_errors(record)), key


def _snapshot_record() -> dict:
    return {
        "record_type": "source_lock_snapshot_record",
        "snapshot_record_id": "stage4k-test",
        "source_url": "https://github.com/rtkd/iddqd",
        "canonical_url": "https://github.com/rtkd/iddqd/tree/0123456789abcdef0123456789abcdef01234567",
        "source_class": "github_repository",
        "retrieval_status": "metadata_only",
        "snapshot_policy": "commit_addressed_reference",
        "lock_status": "commit_address_locked",
        "licence_or_copyright_note": "Public GitHub metadata only.",
        "committed_snapshot": False,
        "raw_private_data_committed": False,
        "binary_committed": False,
        "image_committed": False,
        "audio_committed": False,
        "font_committed": False,
        "archive_committed": False,
        "solve_claim": False,
    }
