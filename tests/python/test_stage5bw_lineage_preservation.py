from pathlib import Path

from test_stage5bw_common import load_yaml


def test_stage5bw_active_lineage_uses_correct_stage5aw_path() -> None:
    lineage = load_yaml("data/token-block/stage5bw-active-lineage-preservation.yaml")
    paths = lineage["preserved_active_record_paths"]

    assert "data/token-block/stage5ap-token-block-canonical-transcription.yaml" in paths
    assert "data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml" in paths
    assert "data/token-block/stage5aw-repaired-branch-manifest.yaml" not in paths
    assert "data/token-block/stage5ay-branch-eligibility-policy.yaml" in paths
    assert "data/token-block/stage5az-repaired-bounded-variant-family-manifest.yaml" in paths
    assert "data/token-block/stage5bb-active-manifest-registry.yaml" in paths
    assert "data/token-block/stage5bd-dry-run-plan-manifest.yaml" in paths
    assert all(Path(path).is_file() for path in paths)
    assert lineage["active_token_block_manifest_changed"] is False


def test_stage5bw_lineage_digest_resolves_all_paths() -> None:
    digest = load_yaml("data/token-block/stage5bw-preserved-active-lineage-digest-index.yaml")
    assert digest["lineage_record_count"] == 8
    assert digest["all_lineage_paths_resolve"] is True
    assert digest["deprecated_stage5aw_path_included"] is False
    assert digest["correct_stage5aw_path_included"] is True
