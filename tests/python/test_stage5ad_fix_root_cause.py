from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ad_fix_root_cause_selects_reference_lineage_mismatch() -> None:
    records = yaml.safe_load(Path("data/cuda/stage5ad-fix-bounded-p56-mismatch-root-cause.yaml").read_text())["records"]
    selected = [record for record in records if record["primary_root_cause"] is True]

    assert len(selected) == 1
    assert selected[0]["cause_id"] == "expected_hash_reference_lineage_mismatch"
    assert selected[0]["cuda_kernel_repair_required"] is False
    assert selected[0]["reference_contract_repair_required"] is True
