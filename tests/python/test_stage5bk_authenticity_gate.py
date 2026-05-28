from test_stage5bk_common import load_yaml


def test_stage5bk_authenticity_gate_requires_review() -> None:
    payload = load_yaml("data/historical-route/stage5bk-authenticity-gate-integration.yaml")
    assert payload["family_id"] == "authenticity_pgp_route"
    assert "pgp_network_verification_blocked" in payload["constraints"]
    assert payload["execution_allowed"] is False
