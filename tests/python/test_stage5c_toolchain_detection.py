from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.cuda_build import toolchain_detection


def test_stage5c_toolchain_detection_tolerates_missing_cuda(monkeypatch: object, tmp_path: Path) -> None:
    monkeypatch.setattr(toolchain_detection.shutil, "which", lambda _name: None)

    out = tmp_path / "toolchain.yaml"
    records = toolchain_detection.detect_toolchain(toolchain_out=out, out_dir=tmp_path / "out")
    payload = yaml.safe_load(out.read_text(encoding="utf-8"))

    assert records == payload["records"]
    assert {record["tool_id"] for record in records} == {"cmake", "nvcc", "nvidia_smi"}
    assert all(record["tool_status"] == "missing" for record in records)
    assert all(record["tool_required_for_ci"] is False for record in records)
    assert all(record["absolute_path_committed"] is False for record in records)
