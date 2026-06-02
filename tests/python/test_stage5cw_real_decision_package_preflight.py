from test_stage5cw_common import ensure_stage5cw_built, load_yaml


def test_stage5cw_preflight_is_not_real_decision_package() -> None:
    ensure_stage5cw_built()
    payload = load_yaml("data/token-block/stage5cw-real-decision-package-preflight.yaml")

    assert payload["real_decision_package_preflight_created"] is True
    assert payload["real_decision_package_preflight_status"] == "review_preflight_only"
    assert payload["real_decision_package_created_now"] is False
    assert payload["real_decision_package_valid_now"] is False
    assert payload["preflight_authorizes_real_decision_now"] is False
    assert payload["preflight_authorizes_execution_now"] is False
    assert payload["selected_option_id"] is None
