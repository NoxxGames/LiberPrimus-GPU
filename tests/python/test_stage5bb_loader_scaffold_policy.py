from pathlib import Path

import pytest
import yaml

from libreprimus.token_block.stage5bb import ActiveManifestResolver, ExecutionBlockedError


def test_stage5bb_loader_refuses_superseded_active_paths() -> None:
    registry = yaml.safe_load(Path("data/token-block/stage5bb-active-manifest-registry.yaml").read_text())
    resolver = ActiveManifestResolver(registry)

    with pytest.raises(ExecutionBlockedError):
        resolver.load_path_as_active("data/token-block/stage5av-token-variant-branch-manifest.yaml")
    with pytest.raises(ExecutionBlockedError):
        resolver.load_path_as_active("data/token-block/stage5ay-bounded-variant-family-manifest.yaml")


def test_stage5bb_loader_diagnostic_mode_identifies_superseded_paths() -> None:
    registry = yaml.safe_load(Path("data/token-block/stage5bb-active-manifest-registry.yaml").read_text())
    resolver = ActiveManifestResolver(registry)

    diagnostic = resolver.identify_historical_diagnostic_path(
        "data/token-block/stage5ay-bounded-variant-family-manifest.yaml"
    )
    assert diagnostic is not None
    assert diagnostic["historical_diagnostic_load_allowed"] is True
    assert diagnostic["active_load_allowed"] is False
