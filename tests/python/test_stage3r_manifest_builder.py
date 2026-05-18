from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.discord_lead_promotion.manifest_builder import (
    build_post_discord_manifests,
    post_discord_manifests,
)


def test_post_discord_manifests_have_required_caps_and_disabled_policy() -> None:
    manifests = {manifest["experiment_id"]: manifest for manifest in post_discord_manifests()}
    assert manifests["EXP-3R-001"]["candidate_count_cap"] == 576
    assert manifests["EXP-3R-003"]["candidate_count_cap"] == 144
    assert manifests["EXP-3R-004"]["candidate_count_cap"] == 64
    for manifest in manifests.values():
        assert manifest["execution_enabled"] is False
        assert manifest["cuda_enabled"] is False
        assert manifest["no_solve_claim"] is True
        assert manifest["canonical_corpus_active"] is False


def test_manifest_builder_writes_three_files(tmp_path: Path) -> None:
    summary = build_post_discord_manifests(out_dir=tmp_path, audit_summary=None)
    assert summary["manifest_count"] == 3
    files = sorted(path.name for path in tmp_path.glob("EXP-3R-*.yaml"))
    assert len(files) == 3
    payload = yaml.safe_load((tmp_path / "EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml").read_text(encoding="utf-8"))
    assert payload["candidate_generation"]["candidate_count_estimate"] == 72
