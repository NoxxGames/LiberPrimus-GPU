from test_stage5ck_common import load_yaml


def test_activation_decision_review_package_is_review_only() -> None:
    payload = load_yaml("data/token-block/stage5ck-activation-decision-review-package.yaml")
    assert payload["activation_decision_review_package_created"] is True
    assert payload["activation_decision_review_package_status"] == "review_package_only"
    assert payload["activation_decision_review_package_authorizes_activation"] is False
    assert payload["activation_decision_review_package_authorizes_active_input"] is False
    assert payload["activation_decision_review_package_authorizes_byte_stream_generation"] is False
    assert payload["activation_decision_review_package_authorizes_execution"] is False
    assert payload["review_checklist_count"] >= 15
