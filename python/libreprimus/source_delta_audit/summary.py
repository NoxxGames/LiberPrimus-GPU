"""Stage 4E source-delta summary helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.source_delta_audit.validation import load_yaml_records


def summarize_records(
    *,
    source_delta: Path,
    source_health: Path,
    image_artifact: Path,
    manifest_dir: Path,
) -> dict[str, Any]:
    """Summarize committed Stage 4E records."""

    delta_records = load_yaml_records(source_delta)
    health_records = load_yaml_records(source_health)
    artifact_records = load_yaml_records(image_artifact)
    manifests = sorted(manifest_dir.glob("exp_stage4e_*.yaml")) if manifest_dir.is_dir() else []
    audit = delta_records[0] if delta_records else {}
    return {
        "run_id": "stage4e-source-delta-audit",
        "remote_reachable": bool(audit.get("reachable")),
        "remote_head": audit.get("remote_head"),
        "path_count": int(audit.get("path_count") or 0),
        "source_delta_records_count": len(delta_records),
        "source_health_records_count": len(health_records),
        "duplicate_candidate_count": sum(1 for item in audit.get("selected_path_candidates", []) if item.get("duplicate_of")),
        "unique_candidate_count": sum(1 for item in audit.get("selected_path_candidates", []) if not item.get("duplicate_of")),
        "image_artifact_records_count": len(artifact_records),
        "disabled_manifest_count": len(manifests),
    }
