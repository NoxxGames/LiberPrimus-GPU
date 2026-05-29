from pathlib import Path

import yaml

from libreprimus.token_block.stage5bu import validate_stage5bu_lineage_paths
from test_stage5bu_common import ROOT, load_yaml


def test_stage5bu_active_manifest_preservation_uses_resolving_stage5aw_path() -> None:
    payload = load_yaml("data/token-block/stage5bs-active-manifest-preservation.yaml")
    paths = payload["preserved_active_record_paths"]

    assert "data/token-block/stage5aw-repaired-branch-manifest.yaml" not in paths
    assert "data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml" in paths
    assert all((ROOT / path).is_file() for path in paths)


def test_stage5bu_lineage_validator_rejects_deprecated_stage5aw_path(tmp_path: Path) -> None:
    active = load_yaml("data/token-block/stage5bs-active-manifest-preservation.yaml")
    active["preserved_active_record_paths"] = [
        "data/token-block/stage5aw-repaired-branch-manifest.yaml"
    ]
    active_path = tmp_path / "active.yaml"
    active_path.write_text(yaml.safe_dump(active), encoding="utf-8")

    _, errors = validate_stage5bu_lineage_paths(active_preservation=active_path)
    assert any("deprecated_stage5aw_path_active" in error for error in errors)
