from __future__ import annotations

from test_stage5ds_common import ensure_stage5ds_built, load_yaml


def test_stage5ds_ouroboros_arithmetic_records() -> None:
    ensure_stage5ds_built()
    ouroboros = load_yaml(
        "data/historical-route/stage5ds-ouroboros-gp-167-music-cycle-candidate-v0.yaml"
    )
    pdd = load_yaml(
        "data/historical-route/stage5ds-pdd153-ouroboros-167-mod153-offset14-candidate-v0.yaml"
    )
    cycle = load_yaml(
        "data/historical-route/stage5ds-pdd153-56311-ouroboric-cycle-candidate-v0.yaml"
    )
    assert ouroboros["gp_sum"] == 167
    assert pdd["offset"] == 14
    assert cycle["sequence"] == [5, 6, 3, 11]
    assert cycle["closed_state_period"] == 612
    assert cycle["route_extraction_performed_now"] is False


def test_stage5ds_gp_scan_preserves_expected_values() -> None:
    ensure_stage5ds_built()
    scan = load_yaml(
        "data/historical-route/stage5ds-ouroboros-see-also-gp-arithmetic-scan-v0.yaml"
    )
    values = {row["phrase"]: row["gp_sum"] for row in scan["gp_scan_records"]}
    assert values["SELF REFERENCE"] == 529
    assert values["SELF FULFILLING PROPHECY"] == 841
    assert values["INFINITE LOOP"] == 409
