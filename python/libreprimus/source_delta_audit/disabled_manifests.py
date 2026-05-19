"""Disabled Stage 4E future manifests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.source_delta_audit.models import DISABLED_MANIFEST_IDS


MANIFEST_PURPOSES = {
    "exp_stage4e_lp_image_variant_hash_dimension_audit": "Compare source-locked LP image variants by filename, count, SHA-256, dimensions, and metadata only.",
    "exp_stage4e_image_compression_artifact_preflight": "Run deterministic compression-artifact preflight metrics after source variants and controls are locked.",
    "exp_stage4e_lp_outguessed_fixture_source_lock": "Source-lock historical lp_outguessed payload fixture metadata without running stego tools.",
    "exp_stage4e_audio_fixture_source_lock": "Source-lock historical audio fixture metadata without audio or spectrogram analysis.",
}


def build_disabled_manifests() -> list[dict[str, Any]]:
    """Return disabled future manifests."""

    return [
        {
            "record_type": "future_image_artifact_manifest",
            "manifest_id": manifest_id,
            "purpose": MANIFEST_PURPOSES[manifest_id],
            "stage": "stage4e",
            "execution_enabled": False,
            "cuda_enabled": False,
            "raw_outputs_committed": False,
            "generated_outputs_committed": False,
            "solve_claim": False,
            "trusted_as_canonical": False,
            "notes": "Queued only; requires explicit future stage before execution.",
        }
        for manifest_id in DISABLED_MANIFEST_IDS
    ]


def write_disabled_manifests(manifest_dir: Path) -> list[Path]:
    """Write disabled manifests to disk."""

    manifest_dir.mkdir(parents=True, exist_ok=True)
    readme = manifest_dir / "README.md"
    readme.write_text(
        "# Stage 4E Disabled Future Manifests\n\n"
        "These manifests are queued for future source-lock and deterministic image/stego provenance work. "
        "They are disabled and must not be executed without a later explicit stage.\n",
        encoding="utf-8",
    )
    written = [readme]
    for manifest in build_disabled_manifests():
        path = manifest_dir / f"{manifest['manifest_id']}.yaml"
        path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
        written.append(path)
    return written
