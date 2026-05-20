from __future__ import annotations

from libreprimus.cuda_parity.backend_capability import build_backend_capability


def test_stage5b_backend_capability_records_no_cuda_required(tmp_path) -> None:
    records = build_backend_capability(out_dir=tmp_path, backend_capability_out=tmp_path / "backend.yaml")
    profiles = {record["vram_profile"] for record in records}
    assert profiles == {"ci_no_gpu", "compatibility_8gb", "local_16gb"}
    assert all(record["cuda_hardware_required"] is False for record in records)
    assert all(record["local_16gb_profile_required"] is False for record in records)
    assert all(record["cuda_kernel_added"] is False for record in records)


def test_stage5b_backend_capability_16gb_optional_and_8gb_present(tmp_path) -> None:
    records = build_backend_capability(out_dir=tmp_path, backend_capability_out=tmp_path / "backend.yaml")
    by_profile = {record["vram_profile"]: record for record in records}
    assert by_profile["local_16gb"]["local_16gb_profile_supported"] is True
    assert by_profile["local_16gb"]["local_16gb_profile_required"] is False
    assert by_profile["compatibility_8gb"]["vram_gb"] == 8
