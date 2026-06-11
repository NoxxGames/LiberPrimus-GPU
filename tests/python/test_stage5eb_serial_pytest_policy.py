from __future__ import annotations

from test_stage5eb_common import ROOT, ensure_stage5eb_built, load_yaml


def test_stage5eb_full_serial_pytest_is_rare_explicit_fallback() -> None:
    ensure_stage5eb_built()

    record = load_yaml("data/project-state/stage5eb-serial-pytest-policy.yaml")

    assert record["full_serial_pytest_default_for_future_stages"] is False
    assert record["full_serial_pytest_required_for_normal_stage_completion"] is False
    assert record["full_serial_pytest_profile_name"] == "full-serial-rare"
    assert record["full_serial_pytest_allowed_only_when_explicitly_requested"] is True
    assert record["full_serial_pytest_must_not_run_inside_ci_profile"] is True
    assert record["full_serial_pytest_must_not_run_inside_local_fast_profile"] is True
    assert record["full_serial_pytest_must_not_run_inside_full_parallel_profile"] is True


def test_stage5eb_stage_validation_profiles_keep_serial_rare() -> None:
    ensure_stage5eb_built()

    ps1 = (ROOT / "scripts/ci/run-stage-validation.ps1").read_text(encoding="utf-8")
    sh = (ROOT / "scripts/ci/run-stage-validation.sh").read_text(encoding="utf-8")

    assert "full-serial-rare" in ps1
    assert "full serial pytest is a rare fallback" in ps1.lower()
    assert "full-serial-rare" in sh
    assert "full serial pytest is a rare fallback" in sh.lower()
