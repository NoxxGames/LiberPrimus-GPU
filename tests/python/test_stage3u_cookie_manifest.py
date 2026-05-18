from __future__ import annotations

from pathlib import Path

from libreprimus.post_discord.cookie_signed_variant_pack import load_cookie_manifest

MANIFEST = Path("experiments/manifests/post-discord/EXP-3R-001-cookie-sha256-signed-variants-a.yaml")


def test_stage3u_manifest_validates() -> None:
    manifest = load_cookie_manifest(MANIFEST)

    assert manifest.experiment_id == "EXP-3R-001"
    assert manifest.candidate_cap == 576
    assert manifest.algorithm == "sha256"
    assert manifest.payload["cuda_enabled"] is False
    assert manifest.payload["no_solve_claim"] is True


def test_stage3u_manifest_candidate_space_is_bounded() -> None:
    manifest = load_cookie_manifest(MANIFEST)

    assert len(manifest.base_strings) == 13
    assert len(manifest.byte_variants) == 12
    assert len(manifest.base_strings) * len(manifest.byte_variants) <= manifest.candidate_cap
