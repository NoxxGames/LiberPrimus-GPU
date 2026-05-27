from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator


def load_yaml(path: str) -> dict[str, Any]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}


def load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_schema(schema_path: str, record_path: str) -> None:
    Draft202012Validator(load_json(schema_path)).validate(load_yaml(record_path))


def assert_stage5bf_metadata_only(payload: dict[str, Any]) -> None:
    for key in (
        "execution_performed",
        "hash_search_performed",
        "decode_attempt_performed",
        "raw_archive_files_committed",
    ):
        if key in payload:
            assert payload[key] is False, key


SCHEMA_PAIRS = {
    "schemas/historical-route/local-archive-location-v0.schema.json": (
        "data/historical-route/stage5bf-local-archive-location.yaml"
    ),
    "schemas/historical-route/archive-tree-summary-v0.schema.json": (
        "data/historical-route/stage5bf-archive-tree-summary.yaml"
    ),
    "schemas/historical-route/archive-source-inventory-summary-v0.schema.json": (
        "data/historical-route/stage5bf-archive-source-inventory-summary.yaml"
    ),
    "schemas/historical-route/annual-route-inventory-v0.schema.json": (
        "data/historical-route/stage5bf-annual-route-inventory.yaml"
    ),
    "schemas/historical-route/high-priority-artifact-index-v0.schema.json": (
        "data/historical-route/stage5bf-high-priority-artifact-index.yaml"
    ),
    "schemas/historical-route/artifact-family-taxonomy-v0.schema.json": (
        "data/historical-route/stage5bf-artifact-family-taxonomy.yaml"
    ),
    "schemas/historical-route/trust-classification-policy-v0.schema.json": (
        "data/historical-route/stage5bf-trust-classification-policy.yaml"
    ),
    "schemas/historical-route/artifact-trust-classifications-v0.schema.json": (
        "data/historical-route/stage5bf-artifact-trust-classifications.yaml"
    ),
    "schemas/historical-route/pgp-source-lock-candidates-v0.schema.json": (
        "data/historical-route/stage5bf-pgp-source-lock-candidates.yaml"
    ),
    "schemas/historical-route/stego-source-lock-candidates-v0.schema.json": (
        "data/historical-route/stage5bf-stego-source-lock-candidates.yaml"
    ),
    "schemas/historical-route/outguess-positive-control-candidates-v0.schema.json": (
        "data/historical-route/stage5bf-outguess-positive-control-candidates.yaml"
    ),
    "schemas/historical-route/openpuff-mp3-candidates-v0.schema.json": (
        "data/historical-route/stage5bf-openpuff-mp3-candidates.yaml"
    ),
    "schemas/historical-route/magic-square-artifacts-v0.schema.json": (
        "data/historical-route/stage5bf-magic-square-artifacts.yaml"
    ),
    "schemas/historical-route/hex-jpeg-extraction-candidates-v0.schema.json": (
        "data/historical-route/stage5bf-hex-jpeg-extraction-candidates.yaml"
    ),
    "schemas/historical-route/onion-route-artifacts-v0.schema.json": (
        "data/historical-route/stage5bf-onion-route-artifacts.yaml"
    ),
    "schemas/historical-route/book-code-artifacts-v0.schema.json": (
        "data/historical-route/stage5bf-book-code-artifacts.yaml"
    ),
    "schemas/historical-route/network-byte-channel-artifacts-v0.schema.json": (
        "data/historical-route/stage5bf-network-byte-channel-artifacts.yaml"
    ),
    "schemas/historical-route/liber-primus-historical-artifacts-v0.schema.json": (
        "data/historical-route/stage5bf-liber-primus-historical-artifacts.yaml"
    ),
    "schemas/historical-route/historical-technique-taxonomy-v0.schema.json": (
        "data/historical-route/stage5bf-historical-technique-taxonomy.yaml"
    ),
    "schemas/historical-route/token-block-planning-impact-v0.schema.json": (
        "data/historical-route/stage5bf-token-block-planning-impact.yaml"
    ),
    "schemas/historical-route/source-gap-register-v0.schema.json": (
        "data/historical-route/stage5bf-source-gap-register.yaml"
    ),
    "schemas/historical-route/deep-research-readiness-v0.schema.json": (
        "data/historical-route/stage5bf-deep-research-readiness.yaml"
    ),
    "schemas/historical-route/dwh-historical-context-v0.schema.json": (
        "data/historical-route/stage5bf-dwh-historical-context.yaml"
    ),
    "schemas/historical-route/stage5bf-guardrail-v0.schema.json": "data/historical-route/stage5bf-guardrail.yaml",
    "schemas/project-state/stage5bf-summary-v0.schema.json": "data/project-state/stage5bf-summary.yaml",
}


def test_stage5bf_schemas_validate_committed_records() -> None:
    for schema_path, record_path in SCHEMA_PAIRS.items():
        validate_schema(schema_path, record_path)


def test_stage5bf_local_archive_location_is_hash_locked_without_network() -> None:
    payload = load_yaml("data/historical-route/stage5bf-local-archive-location.yaml")

    assert payload["archive_available"] is True
    assert payload["selected_archive_path"] == "third_party/CicadaSolversIddqd"
    assert payload["selected_archive_path_kind"] == "project_relative"
    assert payload["fallback_absolute_path"] is None
    assert payload["fallback_absolute_path_recorded"] is False
    assert payload["local_archive_tree_digest"] == "bdc8739120be85fc7015e495704ee80bc80ef3a25cfc32c43e3b4d7de40270af"
    assert payload["network_fetch_performed"] is False
    assert payload["upstream_clone_performed"] is False
    assert payload["raw_archive_files_committed"] is False
