from __future__ import annotations

from pathlib import Path

from libreprimus.cuda_parity_reporting.device_code_audit import build_device_code_subset_audit


def test_stage5g_device_code_subset_audit_committed_sources_are_compliant() -> None:
    record = build_device_code_subset_audit()[0]
    assert record["device_code_subset_compliant"] is True
    assert record["stl_used_in_cuda_device_path"] is False
    assert record["std_array_used_in_cuda_device_path"] is False
    assert record["cxx_exceptions_in_cuda_device_path"] is False


def test_stage5g_device_code_subset_audit_rejects_stl_tokens(tmp_path: Path) -> None:
    bad = tmp_path / "bad.cu"
    bad.write_text("#include <array>\nstd::array<int, 1> value;\n", encoding="utf-8")
    record = build_device_code_subset_audit(
        device_code_audit_out=tmp_path / "audit.yaml",
        out_dir=tmp_path / "out",
        source_paths=(bad,),
    )[0]
    assert record["device_code_subset_compliant"] is False
    assert record["stl_used_in_cuda_device_path"] is True
    assert record["std_array_used_in_cuda_device_path"] is True


def test_stage5g_device_code_subset_audit_rejects_throw(tmp_path: Path) -> None:
    bad = tmp_path / "bad.cuh"
    bad.write_text("void f() { throw 1; }\n", encoding="utf-8")
    record = build_device_code_subset_audit(
        device_code_audit_out=tmp_path / "audit.yaml",
        out_dir=tmp_path / "out",
        source_paths=(bad,),
    )[0]
    assert record["device_code_subset_compliant"] is False
    assert record["cxx_exceptions_in_cuda_device_path"] is True
