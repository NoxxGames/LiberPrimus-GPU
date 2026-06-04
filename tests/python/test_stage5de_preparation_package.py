from __future__ import annotations

from test_stage5de_common import SELECTED_OPTION_ID, ensure_stage5de_built, load_yaml


def test_stage5de_creates_preparation_package_only() -> None:
    ensure_stage5de_built()
    package = load_yaml(
        "data/token-block/stage5de-real-operator-approval-preparation-package.yaml"
    )

    assert package["real_operator_approval_preparation_package_created"] is True
    assert package["real_operator_approval_preparation_package_status"] == "preparation_package_only"
    assert package["selected_option_id"] == SELECTED_OPTION_ID
    assert package["real_operator_approval_record_created_now"] is False
    assert package["operator_approval_record_present_now"] is False
    assert package["approval_gate_satisfied_now"] is False
    assert package["selected_option_authorizes_activation_now"] is False


def test_stage5de_records_future_target_context_without_validation() -> None:
    ensure_stage5de_built()
    package = load_yaml(
        "data/token-block/stage5de-real-operator-approval-preparation-package.yaml"
    )

    assert package["target_class_context_recorded_for_future_design_only"] is True
    assert "v3_onion_hostname" in package["future_target_class_context"]
    assert package["target_class_validation_implemented"] is False
    assert package["tor_network_access_performed"] is False
