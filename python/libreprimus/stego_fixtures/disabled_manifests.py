"""Disabled future manifests for Stage 4F fixture work."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.stego_fixtures.models import DISABLED_MANIFEST_IDS


def build_disabled_manifests() -> list[dict[str, Any]]:
    """Return disabled Stage 4F future manifests."""

    purposes = {
        "exp_stage4f_outguess_positive_negative_matrix": "Prepare a source-locked OutGuess positive/negative fixture matrix.",
        "exp_stage4f_openpuff_interconnectedness_fixture_prep": "Prepare Interconnectedness/OpenPuff fixture provenance.",
        "exp_stage4f_mp3_instar_regression_prep": "Prepare MP3/Instar deterministic regression provenance.",
        "exp_stage4f_audio_hexdump_string_baseline": "Prepare audio hexdump/string baseline metadata.",
    }
    return [_manifest(manifest_id, purposes[manifest_id]) for manifest_id in sorted(DISABLED_MANIFEST_IDS)]


def write_disabled_manifests(manifest_dir: Path) -> list[Path]:
    """Write disabled Stage 4F manifests."""

    manifest_dir.mkdir(parents=True, exist_ok=True)
    readme = manifest_dir / "README.md"
    readme.write_text(
        "# Stage 4F Disabled Stego/Audio Fixture Manifests\n\n"
        "These manifests are source-lock preparation records only. They must remain disabled until a later explicit execution stage.\n",
        encoding="utf-8",
    )
    written = [readme]
    for manifest in build_disabled_manifests():
        path = manifest_dir / f"{manifest['manifest_id']}.yaml"
        path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
        written.append(path)
    return written


def _manifest(manifest_id: str, purpose: str) -> dict[str, Any]:
    return {
        "record_type": "historical_stego_fixture_manifest",
        "manifest_id": manifest_id,
        "stage": "stage4f",
        "purpose": purpose,
        "execution_enabled": False,
        "cuda_enabled": False,
        "raw_file_committed": False,
        "binary_committed": False,
        "audio_committed": False,
        "image_committed": False,
        "extracted_payload_committed": False,
        "font_committed": False,
        "trusted_as_canonical": False,
        "solve_claim": False,
        "notes": "Disabled future manifest; Stage 4F records metadata only.",
    }
