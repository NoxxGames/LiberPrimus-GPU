"""Summary helpers for Stage 4B source-lock triage."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.source_lock_triage.loaders import load_yaml_payload, load_yaml_records


def summarize_records(
    *,
    promoted_sources: Path,
    visual_observations: Path,
    negative_controls: Path,
    manifest_dir: Path,
) -> dict[str, Any]:
    """Return a concise Stage 4B committed-record summary."""

    source_records = load_yaml_records(promoted_sources)
    visual_records = load_yaml_records(visual_observations)
    negative_records = load_yaml_records(negative_controls)
    manifests = sorted(manifest_dir.glob("exp_stage4b_*.yaml"))
    cuneiform_count = sum(
        1 for record in visual_records if record.get("observation_family") == "cuneiform_base60"
    )
    delimiter_count = sum(
        1
        for record in visual_records
        if record.get("observation_family") == "mirrored_three_dot_delimiter"
    )
    dot_count = sum(
        1 for record in visual_records if record.get("observation_family") == "dot_binary_ambiguity"
    )
    return {
        "promoted_source_count": len(source_records),
        "visual_observation_count": len(visual_records),
        "cuneiform_observation_count": cuneiform_count,
        "delimiter_observation_count": delimiter_count,
        "dot_ambiguity_observation_count": dot_count,
        "negative_control_count": len(negative_records),
        "disabled_manifest_count": len(manifests),
        "manifest_ids": [load_yaml_payload(path).get("manifest_id") for path in manifests],
        "solve_claim": False,
        "execution_enabled": False,
    }
