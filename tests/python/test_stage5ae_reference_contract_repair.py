from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.corrected_bounded_p56_reporting.models import CORRECTED_FORMULA_HASH, HISTORICAL_EXPECTED_HASH


def test_stage5ae_reference_contract_separates_hash_roles() -> None:
    records = yaml.safe_load(Path("data/cuda/stage5ae-bounded-p56-reference-contract-repair.yaml").read_text())["records"]
    by_hash = {record["hash_value"]: record for record in records}

    assert by_hash[CORRECTED_FORMULA_HASH]["valid_for_formula_parity"] is True
    assert by_hash[CORRECTED_FORMULA_HASH]["valid_for_reference_parity"] is False
    assert by_hash[HISTORICAL_EXPECTED_HASH]["valid_for_formula_parity"] is False
    assert by_hash[HISTORICAL_EXPECTED_HASH]["valid_for_reference_parity"] is True
    assert by_hash[CORRECTED_FORMULA_HASH]["reference_contract_repair_complete"] is True
