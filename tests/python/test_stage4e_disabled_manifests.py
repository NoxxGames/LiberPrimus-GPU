from __future__ import annotations

from libreprimus.source_delta_audit.disabled_manifests import build_disabled_manifests


def test_stage4e_disabled_manifests_are_disabled() -> None:
    manifests = build_disabled_manifests()
    assert len(manifests) == 4
    for manifest in manifests:
        assert manifest["execution_enabled"] is False
        assert manifest["cuda_enabled"] is False
        assert manifest["solve_claim"] is False
