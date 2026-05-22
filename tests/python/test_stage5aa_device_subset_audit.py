from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_cuda_synthetic.device_subset_audit import build_device_subset_audit


def test_stage5aa_device_subset_audit_passes_current_files(tmp_path: Path) -> None:
    record = build_device_subset_audit(device_subset_audit_out=tmp_path / "audit.yaml", out_dir=tmp_path)[0]
    assert record["forbidden_finding_count"] == 0
    assert record["cuda_c_style_subset_status"] == "passed"
