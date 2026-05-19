"""Load and write Stage 4L observation promotion records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.observation_promotion.models import (
    DISABLED_MANIFEST_DIRS,
    RELEVANT_RECORD_PATHS,
    STAGE4J_DECISIONS,
    STAGE4J_PROMOTIONS,
    STAGE4J_QUARANTINE,
    STAGE4J_SUMMARY,
    STAGE4K_FETCH_RECORDS,
    STAGE4K_SNAPSHOT_RECORDS,
    STAGE4K_SUMMARY,
    STAGE4L_COMMUNITY_INTAKE,
)
from libreprimus.paths import repo_root


def load_yaml_records(path: Path) -> list[dict[str, Any]]:
    """Load a Stage-style YAML record set, singleton YAML document, or empty path."""

    if not path.is_file():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if isinstance(data, dict) and isinstance(data.get("records"), list):
        return [record for record in data["records"] if isinstance(record, dict)]
    if isinstance(data, dict):
        return [data]
    return []


def write_yaml_records(path: Path, *, record_set_id: str, schema: str, records: list[dict[str, Any]]) -> None:
    """Write a Stage-style YAML record set."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(
            {"record_set_id": record_set_id, "schema": schema, "records": records},
            sort_keys=False,
            allow_unicode=False,
        ),
        encoding="utf-8",
    )


def write_yaml_document(path: Path, payload: dict[str, Any]) -> None:
    """Write a singleton YAML document."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")


def load_stage4l_inputs(root: Path | None = None) -> dict[str, Any]:
    """Load committed inputs used by Stage 4L."""

    base = root or repo_root()
    stage4j_decisions = load_yaml_records(base / STAGE4J_DECISIONS)
    community_intake = load_yaml_records(base / STAGE4L_COMMUNITY_INTAKE)
    return {
        "decisions": [*stage4j_decisions, *community_intake],
        "stage4j_decisions": stage4j_decisions,
        "stage4l_community_intake": community_intake,
        "stage4j_promotions": load_yaml_records(base / STAGE4J_PROMOTIONS),
        "stage4j_quarantine": load_yaml_records(base / STAGE4J_QUARANTINE),
        "stage4j_summary": load_yaml_records(base / STAGE4J_SUMMARY),
        "source_locks": load_yaml_records(base / STAGE4K_SNAPSHOT_RECORDS),
        "fetch_records": load_yaml_records(base / STAGE4K_FETCH_RECORDS),
        "stage4k_summary": load_yaml_records(base / STAGE4K_SUMMARY),
        "relevant_record_counts": _record_counts(base),
        "disabled_manifest_paths": _disabled_manifest_paths(base),
    }


def _record_counts(base: Path) -> dict[str, int]:
    return {path.as_posix(): len(load_yaml_records(base / path)) for path in RELEVANT_RECORD_PATHS}


def _disabled_manifest_paths(base: Path) -> list[str]:
    paths: list[str] = []
    for manifest_dir in DISABLED_MANIFEST_DIRS:
        full = base / manifest_dir
        if full.is_dir():
            paths.extend(path.relative_to(base).as_posix() for path in sorted(full.glob("*.yaml")))
    return paths
