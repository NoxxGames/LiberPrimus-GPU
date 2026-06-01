from test_stage5cs_common import ensure_stage5cs_built, load_yaml


def test_stage5cs_preserves_8_worker_cap_without_16_worker_default() -> None:
    ensure_stage5cs_built()
    payload = load_yaml("data/project-state/stage5cs-reviewable-validation-evidence.yaml")
    assert payload["parallel_worker_cap_for_stage5cs_and_later"] == 8
    assert payload["parallel_validation_workers_observed_locally"] == 8
    assert payload["parallel_validation_pytest_workers_observed_locally"] == 8
