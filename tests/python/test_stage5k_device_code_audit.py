from __future__ import annotations

from pathlib import Path

from libreprimus.gematria_cuda_parity_reporting.device_code_audit import build_device_code_audit


def test_stage5k_device_code_audit_accepts_current_cuda_subset(tmp_path: Path) -> None:
    audit_out = tmp_path / "audit.yaml"
    records = build_device_code_audit(device_code_audit_out=audit_out, out_dir=tmp_path)
    record = records[0]
    assert record["device_code_subset_compliant"] is True
    assert record["banned_token_finding_count"] == 0
    assert record["stl_used_in_cuda_device_path"] is False
    assert record["cxx_exceptions_in_cuda_device_path"] is False
    assert record["dynamic_allocation_in_device_code"] is False


def test_stage5k_device_code_audit_rejects_banned_tokens(tmp_path: Path) -> None:
    source = tmp_path / "bad_kernel.cu"
    source.write_text("#include <vector>\nvoid f(){ throw 1; }\n", encoding="utf-8")
    records = build_device_code_audit(
        device_code_audit_out=tmp_path / "audit.yaml",
        out_dir=tmp_path,
        source_paths=(source,),
    )
    record = records[0]
    assert record["device_code_subset_compliant"] is False
    assert record["stl_used_in_cuda_device_path"] is True
    assert record["cxx_exceptions_in_cuda_device_path"] is True
