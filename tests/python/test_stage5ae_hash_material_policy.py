from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ae_hash_material_policy_forbids_cross_use() -> None:
    records = yaml.safe_load(Path("data/cuda/stage5ae-hash-material-policy.yaml").read_text())["records"]
    formula = next(record for record in records if record["hash_material_kind"] == "formula_output_tokens")
    reference = next(record for record in records if record["hash_material_kind"] == "candidate_major_reference_outputs")

    assert "formula_output_vs_candidate_major_reference" in formula["forbidden_comparison_contexts"]
    assert "candidate_major_reference_vs_formula_output" in reference["forbidden_comparison_contexts"]
    assert formula["hash_material_policy_repair_complete"] is True
