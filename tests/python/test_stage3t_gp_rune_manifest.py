from __future__ import annotations

from pathlib import Path

from libreprimus.post_discord.gp_rune_claim_verifier import load_gp_rune_manifest


MANIFEST = Path("experiments/manifests/post-discord/EXP-3R-004-gp-rune-claim-verifier-a.yaml")


def test_stage3t_manifest_validates() -> None:
    manifest = load_gp_rune_manifest(MANIFEST)
    assert manifest.experiment_id == "EXP-3R-004"
    assert manifest.claim_cap == 64
    assert manifest.payload["cuda_enabled"] is False
    assert manifest.payload["no_solve_claim"] is True


def test_stage3t_claim_cap_is_64() -> None:
    assert load_gp_rune_manifest(MANIFEST).claim_cap == 64
