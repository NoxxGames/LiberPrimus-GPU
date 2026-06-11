from __future__ import annotations

from pathlib import Path

from test_stage5dy_common import ensure_stage5dy_built, load_yaml


def test_consistency_profile_policy_and_scripts() -> None:
    ensure_stage5dy_built()
    payload = load_yaml("data/project-state/stage5dy-consistency-profile-policy.yaml")
    ps1 = Path("scripts/ci/run-consistency-checks.ps1").read_text(encoding="utf-8")
    sh = Path("scripts/ci/run-consistency-checks.sh").read_text(encoding="utf-8")

    assert payload["fast_profile_available"] is True
    assert payload["stage_profile_available"] is True
    assert payload["full_profile_preserved"] is True
    assert payload["long_tail_checks_default_local"] is False
    assert "validate-stage5dy" in ps1
    assert "validate-stage5dz" in ps1
    assert "validate-stage5ea" in ps1
    assert "--profile" in sh
