"""Load solved-baseline run manifests."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import validate

from libreprimus.paths import repo_root
from libreprimus.solved_baselines.models import FixtureGroup, SolvedBaselineManifest

SCHEMA_PATH = repo_root() / "schemas/corpus/solved-baseline-run-manifest-v0.schema.json"


def manifest_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def load_manifest_payload(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Manifest must be a mapping: {path}")
    validate(instance=payload, schema=_load_schema())
    return payload


def load_manifest(path: Path) -> SolvedBaselineManifest:
    manifest_path = path if path.is_absolute() else repo_root() / path
    payload = load_manifest_payload(manifest_path)
    groups = [
        FixtureGroup(
            fixture_group_id=str(item["fixture_group_id"]),
            fixture_dir=str(item["fixture_dir"]),
            method_family=str(item["method_family"]),
            transform_ids=[str(transform_id) for transform_id in item["transform_ids"]],
            expected_fixture_count=int(item["expected_fixture_count"]),
            expected_pass_count=int(item["expected_pass_count"]),
            allow_pending=bool(item["allow_pending"]),
        )
        for item in payload["fixture_groups"]
    ]
    return SolvedBaselineManifest(
        record_type=str(payload["record_type"]),
        manifest_id=str(payload["manifest_id"]),
        manifest_version=str(payload["manifest_version"]),
        description=str(payload["description"]),
        registry_id=str(payload["registry_id"]),
        registry_sha256=str(payload["registry_sha256"]),
        corpus_candidate_id=str(payload["corpus_candidate_id"]),
        canonical_corpus_active=bool(payload["canonical_corpus_active"]),
        page_boundaries_final=bool(payload["page_boundaries_final"]),
        search_enabled=bool(payload["search_enabled"]),
        cuda_enabled=bool(payload["cuda_enabled"]),
        scoring_enabled=bool(payload["scoring_enabled"]),
        fixture_groups=groups,
        output_dir=str(payload["output_dir"]),
        allow_pending=bool(payload["allow_pending"]),
        allow_warnings=bool(payload["allow_warnings"]),
        require_all_pass=bool(payload["require_all_pass"]),
        expected_counts={str(key): int(value) for key, value in payload["expected_counts"].items()},
        provenance=dict(payload["provenance"]),
        notes=[str(item) for item in payload.get("notes", [])],
        manifest_sha256=manifest_sha256(manifest_path),
    )
