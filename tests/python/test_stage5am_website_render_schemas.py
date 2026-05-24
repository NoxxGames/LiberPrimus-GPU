from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, validate

from libreprimus.paths import repo_root


SCHEMA_DIR = repo_root() / "schemas/website-render"
DATA_DIR = repo_root() / "data/website-render"


def _schema(name: str) -> dict:
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def _yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_stage5am_schemas_validate() -> None:
    for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        Draft202012Validator.check_schema(json.loads(path.read_text(encoding="utf-8")))


def test_stage5am_records_validate_against_schemas() -> None:
    validate(_yaml(DATA_DIR / "stage5am-render-policy.yaml"), _schema("render-policy-v0.schema.json"))
    validate(_yaml(DATA_DIR / "stage5am-render-inputs.yaml"), _schema("render-inputs-v0.schema.json"))
    validate(_yaml(DATA_DIR / "stage5am-render-output-manifest.yaml"), _schema("render-output-manifest-v0.schema.json"))
    validate(_yaml(DATA_DIR / "stage5am-static-site-validation.yaml"), _schema("static-site-validation-v0.schema.json"))
    validate(_yaml(DATA_DIR / "stage5am-privacy-publication-audit.yaml"), _schema("privacy-publication-audit-v0.schema.json"))
    validate(_yaml(DATA_DIR / "stage5am-upload-instructions.yaml"), _schema("upload-instructions-v0.schema.json"))
    validate(_yaml(DATA_DIR / "stage5am-summary.yaml"), _schema("stage5am-summary-v0.schema.json"))
