from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5h_contract_requires_numeric_token_domain_and_direction() -> None:
    record = yaml.safe_load(Path("data/cuda/stage5h-gematria-shift-score-contract.yaml").read_text(encoding="utf-8"))["records"][0]
    assert record["token_domain"] == "integers_0_to_28"
    assert record["token_domain_min"] == 0
    assert record["token_domain_max"] == 28
    assert record["arithmetic_direction"] == "forward_add_shift_mod29"
    assert record["arithmetic_formula"] == "(token + shift) % 29"


def test_stage5h_contract_requires_separator_policy() -> None:
    record = yaml.safe_load(Path("data/cuda/stage5h-gematria-shift-score-contract.yaml").read_text(encoding="utf-8"))["records"][0]
    assert record["separator_policy"] == "non_transformable_separators_preserved_unshifted"
    assert "word_separator" in record["non_transformable_token_kinds"]
    assert record["current_stage5f_kernel_scope"] == "synthetic_uppercase_latin_only"
