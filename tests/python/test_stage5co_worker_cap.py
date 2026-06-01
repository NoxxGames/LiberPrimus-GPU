from test_stage5co_common import load_yaml


def test_stage5co_preserves_8_worker_cap_without_stage5co_16_worker_default() -> None:
    payload = load_yaml("data/project-state/stage5co-reviewable-validation-evidence.yaml")
    assert payload["parallel_worker_cap"] == 8
    assert payload["parallel_worker_cap_for_stage5co_and_later"] == 8
    assert payload["parallel_validation_workers_observed_locally"] == 8
    assert payload["parallel_validation_pytest_workers_observed_locally"] == 8
    rendered = str(payload)
    assert "PytestWorkers 16" not in rendered
    assert "Workers 16" not in rendered
