from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _records(path: str) -> list[dict[str, Any]]:
    return list(yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"])


def test_stage5ad_device_subset_audit_reports_no_cuda_source_or_kernel_changes() -> None:
    record = _records("data/cuda/stage5ad-bounded-p56-cuda-device-subset-audit.yaml")[0]

    assert record["audit_status"] == "no_cuda_source_changes_reused_existing_kernel"
    assert record["cuda_source_modified"] is False
    assert record["device_kernel_arithmetic_modified"] is False
    assert record["new_cuda_kernel_added"] is False
    assert record["new_cuda_kernels_added"] == 0
    assert record["forbidden_finding_count"] == 0
    assert record["stl_in_cuda_facing_files"] is False
