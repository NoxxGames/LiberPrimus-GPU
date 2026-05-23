from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ad_fix_hash_material_separates_formula_and_candidate_major_material() -> None:
    records = yaml.safe_load(Path("data/cuda/stage5ad-fix-bounded-p56-mismatch-hash-material.yaml").read_text())["records"]
    by_kind = {record["hash_material_kind"]: record for record in records}

    assert by_kind["formula_output_tokens"]["cuda_formula_hash_match"] is True
    assert by_kind["formula_output_tokens"]["expected_hash_match"] is False
    assert by_kind["stage5l_candidate_major_reference_outputs"]["expected_hash_match"] is True
    assert by_kind["stage5l_candidate_major_reference_outputs"]["cuda_formula_hash_match"] is False
