from libreprimus.token_block.stage5co import validate_stage5co_stage5cm_boundary_preservation

from test_stage5co_common import load_yaml


def test_stage5co_preserves_stage5cm_boundary() -> None:
    payload = load_yaml("data/token-block/stage5co-stage5cm-boundary-preservation.yaml")
    assert payload["stage5cm_status_preserved"] is True
    assert payload["stage5cm_approval_readiness_boundary_preserved"] is True
    assert payload["stage5cm_fixture_vs_real_boundary_preserved"] is True
    assert payload["stage5cm_end_to_end_readiness_boundary_preserved"] is True
    assert payload["stage5cm_credential_redaction_policy_preserved"] is True
    assert payload["stage5cm_parallel_worker_cap_preserved"] == 8

    counts, errors = validate_stage5co_stage5cm_boundary_preservation()
    assert errors == []
    assert counts["stage5co_stage5cm_boundary_preservation_valid"] is True
