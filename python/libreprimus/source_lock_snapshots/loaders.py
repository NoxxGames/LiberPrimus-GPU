"""Load Stage 4K source-lock snapshot candidate inputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.paths import repo_root
from libreprimus.source_lock_snapshots.models import SourceCandidate, SOURCE_RECORD_PATHS


def load_yaml_records(path: Path) -> list[dict[str, Any]]:
    """Load records from a Stage-style YAML record set, singleton dict, or missing file."""

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


def load_source_candidates(root: Path | None = None) -> list[SourceCandidate]:
    """Load source candidates from committed Stage 4B/4E/4F/4J records."""

    base = root or repo_root()
    candidates: list[SourceCandidate] = []
    candidates.extend(_stage4b_candidates(base / SOURCE_RECORD_PATHS["stage4b_sources"]))
    candidates.extend(_stage4e_candidates(base / SOURCE_RECORD_PATHS["stage4e_source_delta"]))
    candidates.extend(_stage4f_candidates(base / SOURCE_RECORD_PATHS["stage4f_outguess"], "stage4f_outguess"))
    candidates.extend(_stage4f_candidates(base / SOURCE_RECORD_PATHS["stage4f_audio"], "stage4f_audio"))
    candidates.extend(_stage4j_source_reference_candidates(base / SOURCE_RECORD_PATHS["stage4j_review_decisions"]))
    return candidates


def _stage4b_candidates(path: Path) -> list[SourceCandidate]:
    candidates: list[SourceCandidate] = []
    for record in load_yaml_records(path):
        url = str(record.get("url") or record.get("source_url") or "").strip()
        source_id = str(record.get("source_id") or record.get("record_id") or "")
        if not source_id or not url:
            continue
        candidates.append(
            SourceCandidate(
                candidate_id=source_id,
                source_url=url,
                source_family="stage4b_sources",
                title=str(record.get("title") or source_id),
                artifact_type=str(record.get("source_class") or "public_source"),
                source_basis="Stage 4B promoted public source record",
                payload=record,
            )
        )
    return candidates


def _stage4e_candidates(path: Path) -> list[SourceCandidate]:
    candidates: list[SourceCandidate] = []
    for record in load_yaml_records(path):
        source_id = str(record.get("source_id") or "stage4e-cicada-solvers-iddqd")
        repo_url = str(record.get("repo_url") or "").removesuffix(".git")
        if repo_url:
            candidates.append(
                SourceCandidate(
                    candidate_id=source_id,
                    source_url=repo_url,
                    source_family="stage4e_source_delta",
                    title="cicada-solvers iddqd repository",
                    artifact_type="github_repository",
                    source_basis="Stage 4E source-delta repository record",
                    payload=record,
                )
            )
        for item in record.get("selected_path_candidates") or []:
            if not isinstance(item, dict):
                continue
            path_value = str(item.get("path") or "")
            if not path_value:
                continue
            item_id = str(item.get("candidate_id") or f"{source_id}-{path_value}")
            candidates.append(
                SourceCandidate(
                    candidate_id=item_id,
                    source_url=f"https://github.com/cicada-solvers/iddqd/blob/master/{path_value}",
                    source_family="stage4e_source_delta",
                    title=f"cicada-solvers iddqd {path_value}",
                    source_path=path_value,
                    artifact_type=str(item.get("artifact_type") or "artifact_metadata"),
                    source_basis="Stage 4E selected source path candidate",
                    payload=item,
                )
            )
    return candidates


def _stage4f_candidates(path: Path, family: str) -> list[SourceCandidate]:
    candidates: list[SourceCandidate] = []
    for record in load_yaml_records(path):
        source_url = str(record.get("source_url") or "").strip()
        fixture_id = str(record.get("fixture_id") or record.get("audio_fixture_id") or "")
        if not fixture_id or not source_url:
            continue
        candidates.append(
            SourceCandidate(
                candidate_id=fixture_id,
                source_url=source_url,
                source_family=family,
                title=fixture_id.replace("-", " "),
                source_path=str(record.get("source_path") or ""),
                artifact_type=str(record.get("artifact_type") or "fixture_metadata"),
                source_basis="Stage 4F fixture source metadata",
                payload=record,
            )
        )
    return candidates


def _stage4j_source_reference_candidates(path: Path) -> list[SourceCandidate]:
    candidates: list[SourceCandidate] = []
    for record in load_yaml_records(path):
        if record.get("observation_type") != "source_link":
            continue
        payload = record.get("source_payload") if isinstance(record.get("source_payload"), dict) else record.get("payload")
        if not isinstance(payload, dict):
            payload = {}
        url = str(payload.get("url") or payload.get("source_url") or "").strip()
        if not url:
            continue
        source_id = str(payload.get("source_id") or record.get("observation_id") or "")
        candidates.append(
            SourceCandidate(
                candidate_id=f"stage4j-{source_id}",
                source_url=url,
                source_family="stage4j_review_decisions",
                title=str(record.get("observation_id") or source_id),
                artifact_type=str(payload.get("source_class") or "source_link"),
                source_basis="Stage 4J accepted source-reference decision",
                payload=record,
            )
        )
    return candidates
