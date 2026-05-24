from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import validate


SCHEMA_DIR = Path("schemas/deep-research-export")
DATA_DIR = Path("data/deep-research-export")


def _schema(name: str) -> dict:
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def _yaml(name: str) -> dict:
    return yaml.safe_load((DATA_DIR / name).read_text(encoding="utf-8"))


def test_stage5an_schemas_validate_committed_records() -> None:
    validate(_yaml("stage5an-content-pack-policy.yaml"), _schema("content-pack-policy-v0.schema.json"))
    validate(_yaml("stage5an-content-pack-inputs.yaml"), _schema("content-pack-inputs-v0.schema.json"))
    validate(_yaml("stage5an-content-pack-manifest-summary.yaml"), _schema("content-pack-manifest-summary-v0.schema.json"))
    validate(_yaml("stage5an-hosted-content-export-summary.yaml"), _schema("hosted-content-export-summary-v0.schema.json"))
    validate(_yaml("stage5an-combined-webroot-summary.yaml"), _schema("combined-webroot-summary-v0.schema.json"))
    validate(_yaml("stage5an-file-selection-summary.yaml"), _schema("file-selection-summary-v0.schema.json"))
    validate(_yaml("stage5an-publication-gate-audit.yaml"), _schema("publication-gate-audit-v0.schema.json"))
    validate(_yaml("stage5an-upload-instructions.yaml"), _schema("upload-instructions-v0.schema.json"))
    validate(_yaml("stage5an-deep-research-consumption-guide.yaml"), _schema("deep-research-consumption-guide-v0.schema.json"))
    validate(_yaml("stage5an-summary.yaml"), _schema("stage5an-summary-v0.schema.json"))
