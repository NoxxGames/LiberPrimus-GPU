from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, validate

from libreprimus.paths import repo_root


SCHEMA_DIR = repo_root() / "schemas/website-ingest"
DATA_DIR = repo_root() / "data/website-ingest/stage5al"


def _schema(name: str) -> dict:
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def _yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_stage5al_schemas_validate() -> None:
    for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        Draft202012Validator.check_schema(json.loads(path.read_text(encoding="utf-8")))


def test_stage5al_committed_package_records_validate() -> None:
    validate(instance=_yaml(DATA_DIR / "research-index.yaml"), schema=_schema("research-index-v0.schema.json"))
    for record in _yaml(DATA_DIR / "research-bundles.yaml")["records"]:
        validate(instance=record, schema=_schema("research-bundle-v0.schema.json"))
    for record in _yaml(DATA_DIR / "source-cards.yaml")["records"]:
        validate(instance=record, schema=_schema("source-card-v0.schema.json"))
    for record in _yaml(DATA_DIR / "content-index.yaml")["records"]:
        validate(instance=record, schema=_schema("content-index-record-v0.schema.json"))
    for record in _yaml(DATA_DIR / "community-claims.yaml")["records"]:
        validate(instance=record, schema=_schema("community-claim-record-v0.schema.json"))
    for record in _yaml(DATA_DIR / "publication-gates.yaml")["records"]:
        validate(instance=record, schema=_schema("publication-gate-v0.schema.json"))
