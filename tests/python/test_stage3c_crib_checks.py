from __future__ import annotations

from libreprimus.scoring.crib_checks import crib_check
from libreprimus.scoring.validation import validate_crib_check_result


def test_crib_checks_detect_known_cribs_without_solve_claim() -> None:
    result = validate_crib_check_result(crib_check("LIBER PRIMUS ANSWER", cribs=["LIBER", "PRIMUS", "ANSWER"]))

    assert result["crib_hit_count"] == 3
    assert result["crib_hits"] == ["ANSWER", "LIBER", "PRIMUS"]
    assert result["solve_claim"] is False
