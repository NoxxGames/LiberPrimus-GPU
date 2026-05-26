from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_stage5aw_repaired_branch_manifest_supersedes_stage5av_without_enumeration() -> None:
    manifest = yaml.safe_load(
        (
            ROOT / "data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml"
        ).read_text(encoding="utf-8")
    )
    assert manifest["supersedes_stage5av_branch_manifest"] == (
        "data/token-block/stage5av-token-variant-branch-manifest.yaml"
    )
    assert manifest["use_compact_branch_manifest"] is True
    assert manifest["full_cartesian_product_enumerated"] is False
    assert manifest["variant_byte_streams_generated"] is False
    assert manifest["execution_performed"] is False
