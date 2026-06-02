from libreprimus.token_block.stage5cw import PREFLIGHT_MISUSE_CASES

from test_stage5cw_common import ensure_stage5cw_built, load_yaml


def test_stage5cw_preflight_misuse_matrix_fails_closed() -> None:
    ensure_stage5cw_built()
    payload = load_yaml("data/token-block/stage5cw-preflight-misuse-validation-matrix.yaml")

    rows = payload["matrix_rows"]
    assert payload["preflight_misuse_case_count"] == len(PREFLIGHT_MISUSE_CASES)
    assert {row["misuse_case_id"] for row in rows} == set(PREFLIGHT_MISUSE_CASES)
    for row in rows:
        assert row["must_fail_closed"] is True
        assert row["allowed_now"] is False
        assert row["gate_opening"] is False
        assert row["authorizes_approval"] is False
        assert row["authorizes_activation"] is False
        assert row["authorizes_execution"] is False
        assert row["solve_claim"] is False
