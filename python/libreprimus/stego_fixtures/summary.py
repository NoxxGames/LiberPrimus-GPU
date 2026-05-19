"""Summary helpers for Stage 4F stego fixture records."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from libreprimus.stego_fixtures.loaders import load_yaml_records


def summarize_records(
    *,
    outguess_fixtures: Path,
    audio_fixtures: Path,
    source_health: Path,
    toolchain: Path,
    manifest_dir: Path,
) -> dict[str, Any]:
    """Summarize committed Stage 4F fixture records."""

    outguess = load_yaml_records(outguess_fixtures)
    audio = load_yaml_records(audio_fixtures)
    health = load_yaml_records(source_health)
    tools = load_yaml_records(toolchain)
    manifest_count = len(list(manifest_dir.glob("exp_stage4f_*.yaml"))) if manifest_dir.is_dir() else 0
    availability = Counter(str(record.get("local_availability", "unknown")) for record in [*outguess, *audio])
    return {
        "run_id": "stage4f-stego-fixture-source-lock",
        "outguess_fixture_source_records_count": len(outguess),
        "audio_fixture_source_records_count": len(audio),
        "source_health_records_count": len(health),
        "toolchain_requirement_records_count": len(tools),
        "disabled_manifest_count": manifest_count,
        "local_availability_counts": dict(sorted(availability.items())),
    }
