from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import validate


def test_stage3v_stego_schemas_validate_committed_records() -> None:
    schema_dir = Path("schemas/stego")
    artifact_schema = json.loads((schema_dir / "stego-artifact-record-v0.schema.json").read_text(encoding="utf-8"))
    manifest_schema = json.loads((schema_dir / "outguess-regression-manifest-v0.schema.json").read_text(encoding="utf-8"))
    extraction_schema = json.loads((schema_dir / "outguess-extraction-record-v0.schema.json").read_text(encoding="utf-8"))
    summary_schema = json.loads((schema_dir / "outguess-regression-summary-v0.schema.json").read_text(encoding="utf-8"))
    tool_schema = json.loads((schema_dir / "outguess-tool-record-v0.schema.json").read_text(encoding="utf-8"))

    artifacts = yaml.safe_load(Path("data/observations/stego/outguess-artifacts-v0.yaml").read_text(encoding="utf-8"))
    manifest = yaml.safe_load(Path("experiments/manifests/stego/outguess-regression-v1.yaml").read_text(encoding="utf-8"))

    validate(manifest, manifest_schema)
    for record in artifacts["records"]:
        validate(record, artifact_schema)
        assert record["trusted_as_canonical"] is False
        assert record["solve_claim"] is False

    validate(
        {
            "record_type": "outguess_tool_record",
            "tool_name": "outguess",
            "tool_available": False,
            "tool_path": None,
            "help_output_sha256": None,
            "detected_at_utc": "2026-05-16T00:00:00Z",
            "platform": "test",
            "notes": "missing",
        },
        tool_schema,
    )
    validate(
        {
            "record_type": "outguess_extraction_record",
            "run_id": "run",
            "case_id": "case",
            "artifact_id": "artifact",
            "expected_role": "synthetic_negative",
            "tool_available": False,
            "asset_available": False,
            "extraction_attempted": False,
            "extraction_exit_code": None,
            "extracted_payload_sha256": None,
            "extracted_payload_size_bytes": None,
            "expected_payload_sha256": None,
            "payload_match": None,
            "status": "skipped_tool_missing",
            "output_paths": {},
            "raw_payload_committed": False,
            "solve_claim": False,
            "cuda_used": False,
            "notes": "test",
        },
        extraction_schema,
    )
    validate(
        {
            "record_type": "outguess_regression_summary",
            "run_id": "run",
            "generated_at_utc": "2026-05-16T00:00:00Z",
            "tool_available": False,
            "case_count": 1,
            "attempted_count": 0,
            "passed_count": 0,
            "failed_count": 0,
            "skipped_tool_missing_count": 1,
            "skipped_asset_missing_count": 0,
            "extraction_error_count": 0,
            "unexpected_payload_count": 0,
            "output_paths": {},
            "raw_payloads_committed": False,
            "solve_claim": False,
            "cuda_used": False,
            "notes": "test",
        },
        summary_schema,
    )
