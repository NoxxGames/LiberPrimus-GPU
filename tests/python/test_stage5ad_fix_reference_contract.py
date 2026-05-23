from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ad_fix_reference_contract_requires_reporting_repair_not_kernel_repair() -> None:
    record = yaml.safe_load(Path("data/cuda/stage5ad-fix-bounded-p56-mismatch-reference-contract.yaml").read_text())["records"][0]

    assert record["cuda_formula_matches_stage5x_formula"] is True
    assert record["cuda_formula_matches_stage5w_expected"] is False
    assert record["reference_contract_repair_required"] is True
    assert record["hash_material_policy_repair_required"] is True
    assert record["cuda_kernel_repair_required"] is False
