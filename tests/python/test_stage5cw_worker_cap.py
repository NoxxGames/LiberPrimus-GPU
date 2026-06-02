from test_stage5cw_common import ensure_stage5cw_built, load_yaml


def test_stage5cw_preserves_eight_worker_cap() -> None:
    ensure_stage5cw_built()
    payload = load_yaml("data/project-state/stage5cw-reviewable-validation-evidence.yaml")

    assert payload["parallel_worker_cap"] == 8
    assert payload["parallel_worker_cap_for_stage5cw_and_later"] == 8
    assert payload["parallel_validation_workers_observed_locally"] == 8
    assert payload["parallel_validation_pytest_workers_observed_locally"] == 8
    assert payload["old_16_worker_default_reintroduced"] is False
