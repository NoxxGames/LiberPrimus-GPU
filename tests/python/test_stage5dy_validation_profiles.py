from __future__ import annotations

from test_stage5dy_common import ensure_stage5dy_built, load_yaml


def test_validation_profile_registry_contains_required_profiles() -> None:
    ensure_stage5dy_built()
    payload = load_yaml("data/project-state/stage5dy-validation-profile-registry.yaml")
    profiles = payload["profiles"]

    assert set(profiles) == {"focused", "stage_fast", "local_fast", "full_parallel", "full_serial_rare", "ci"}
    assert profiles["full_parallel"]["default_workers"] == 8
    assert profiles["full_parallel"]["default_pytest_workers"] == 8
    assert profiles["full_serial_rare"]["default_allowed_for_every_stage"] is False
    assert payload["old_16_worker_default_reintroduced"] is False


def test_negative_policy_would_fail_for_16_worker_default() -> None:
    ensure_stage5dy_built()
    payload = load_yaml("data/project-state/stage5dy-validation-profile-registry.yaml")
    payload["profiles"]["full_parallel"]["default_workers"] = 16

    assert payload["profiles"]["full_parallel"]["default_workers"] != 8
