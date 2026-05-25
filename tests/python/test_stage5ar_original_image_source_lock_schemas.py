from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from jsonschema import ValidationError, validate


def _schema(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _yaml(path: str) -> dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def test_stage5ar_schemas_validate_committed_records() -> None:
    pairs = [
        ("data/token-block/stage5ar-original-page-image-source-lock.yaml", "schemas/token-block/original-page-image-source-lock-v0.schema.json"),
        ("data/token-block/stage5ar-original-page-image-variants.yaml", "schemas/token-block/original-page-image-variant-v0.schema.json"),
        ("data/token-block/stage5ar-page-split-policy.yaml", "schemas/token-block/page-split-policy-v0.schema.json"),
        ("data/token-block/stage5ar-page-split-records.yaml", "schemas/token-block/page-split-record-v0.schema.json"),
        ("data/token-block/stage5ar-token-pixel-coordinate-policy.yaml", "schemas/token-block/token-pixel-coordinate-policy-v0.schema.json"),
        ("data/token-block/stage5ar-token-pixel-coordinate-records.yaml", "schemas/token-block/token-pixel-coordinate-record-v0.schema.json"),
        ("data/token-block/stage5ar-token-case-policy.yaml", "schemas/token-block/token-case-policy-v0.schema.json"),
        ("data/token-block/stage5ar-token-case-ambiguity-records.yaml", "schemas/token-block/token-case-ambiguity-record-v0.schema.json"),
        ("data/token-block/stage5ar-token-coordinate-validation.yaml", "schemas/token-block/token-coordinate-validation-v0.schema.json"),
        ("data/token-block/stage5ar-token-block-source-lock-update.yaml", "schemas/token-block/token-block-source-lock-update-v0.schema.json"),
        ("data/token-block/stage5ar-token-block-null-control-update.yaml", "schemas/token-block/token-block-null-control-update-v0.schema.json"),
        ("data/token-block/stage5ar-dwh-coordinate-context.yaml", "schemas/token-block/dwh-coordinate-context-v0.schema.json"),
        ("data/project-state/stage5ar-summary.yaml", "schemas/project-state/stage5ar-summary-v0.schema.json"),
    ]
    for data_path, schema_path in pairs:
        validate(_yaml(data_path), _schema(schema_path))


def test_original_source_lock_schema_rejects_screenshot_coordinate_source() -> None:
    payload = _yaml("data/token-block/stage5ar-original-page-image-source-lock.yaml")
    payload["records"][0]["coordinate_source_class"] = "derived_screenshot"
    with pytest.raises(ValidationError):
        validate(payload, _schema("schemas/token-block/original-page-image-source-lock-v0.schema.json"))
