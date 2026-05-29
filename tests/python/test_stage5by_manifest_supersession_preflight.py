from test_stage5by_common import load_yaml


def test_stage5by_manifest_supersession_is_preflight_only() -> None:
    preflight = load_yaml("data/token-block/stage5by-manifest-supersession-readiness-preflight.yaml")
    assert preflight["manifest_supersession_preflight_carried_forward"] is True
    assert preflight["manifest_supersession_performed"] is False
    assert preflight["current_active_records_preserved"] is True
