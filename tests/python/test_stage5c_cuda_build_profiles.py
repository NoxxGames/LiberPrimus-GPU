from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.cuda_build.toolchain_detection import build_profiles


def test_stage5c_build_profiles_are_deterministic_and_no_gpu_safe(tmp_path: Path) -> None:
    out = tmp_path / "profiles.yaml"
    records = build_profiles(profiles_out=out, out_dir=tmp_path / "out")
    payload = yaml.safe_load(out.read_text(encoding="utf-8"))

    assert records == payload["records"]
    assert [record["vram_profile"] for record in records] == [
        "ci_no_gpu",
        "compatibility_8gb",
        "local_optional_16gb",
    ]
    assert all(record["local_16gb_profile_required"] is False for record in records)
    assert all(record["cuda_kernel_added"] is False for record in records)
    assert all(record["gpu_benchmark_performed"] is False for record in records)
