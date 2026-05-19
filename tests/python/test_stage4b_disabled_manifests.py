from __future__ import annotations

from libreprimus.source_lock_triage.disabled_manifests import build_disabled_manifests


def test_stage4b_disabled_manifests_have_safety_flags() -> None:
    manifests = build_disabled_manifests()

    assert len(manifests) == 7
    for manifest in manifests:
        assert manifest["execution_enabled"] is False
        assert manifest["no_solve_claim"] is True
        assert manifest["cuda_enabled"] is False
        assert manifest["canonical_corpus_active"] is False
        assert manifest["page_boundaries_final"] is False
