from __future__ import annotations

from pathlib import Path

import yaml


def test_stage5ad_fix_repair_readiness_keeps_cuda_kernel_repair_not_required() -> None:
    records = yaml.safe_load(Path("data/cuda/stage5ad-fix-bounded-p56-mismatch-repair-readiness.yaml").read_text())["records"]
    by_id = {record["repair_id"]: record for record in records}

    assert by_id["reference_contract_repair"]["repair_required"] is True
    assert by_id["hash_material_policy_repair"]["repair_required"] is True
    assert by_id["cuda_kernel_repair"]["repair_required"] is False
