from test_stage5cu_common import ensure_stage5cu_built, load_yaml


def test_stage5cu_preserves_8_worker_cap_without_16_worker_default() -> None:
    ensure_stage5cu_built()
    payload = load_yaml("data/project-state/stage5cu-reviewable-validation-evidence.yaml")
    assert payload["parallel_worker_cap_for_stage5cu_and_later"] == 8
    assert payload["old_16_worker_default_reintroduced"] is False
