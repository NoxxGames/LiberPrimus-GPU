from __future__ import annotations

from typer.testing import CliRunner

from libreprimus.cli import app
from libreprimus.consistency.state_drift import (
    DEFAULT_OPERATIONAL_FILES,
    REQUIRED_ONBOARDING_FILES,
    check_state_drift_consistency,
)


def test_stage3z_state_drift_includes_onboarding_docs() -> None:
    for relative in REQUIRED_ONBOARDING_FILES:
        assert relative in DEFAULT_OPERATIONAL_FILES


def test_stage3z_state_drift_passes_current_repo() -> None:
    failures = [result for result in check_state_drift_consistency() if result.is_failure]

    assert failures == []


def test_stage3z_research_synthesis_validate_passes() -> None:
    result = CliRunner().invoke(
        app,
        [
            "research-synthesis",
            "validate",
            "--data-dir",
            "data/research",
            "--staged-plan",
            "docs/roadmap/staged-plan.md",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "research_synthesis_valid=true" in result.output
