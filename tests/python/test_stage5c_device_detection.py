from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.cuda_build import device_detection


def test_stage5c_device_detection_tolerates_no_gpu(monkeypatch: object, tmp_path: Path) -> None:
    monkeypatch.setattr(device_detection.shutil, "which", lambda _name: None)

    out = tmp_path / "devices.yaml"
    records = device_detection.detect_devices(devices_out=out, out_dir=tmp_path / "out")
    payload = yaml.safe_load(out.read_text(encoding="utf-8"))

    assert records == payload["records"]
    assert [record["vram_profile"] for record in records] == [
        "ci_no_gpu",
        "compatibility_8gb",
        "local_optional_16gb",
    ]
    assert records[-1]["device_status"] == "not_detected"
    assert records[-1]["local_16gb_profile_detected"] is False


def test_stage5c_parse_mib_extracts_memory() -> None:
    assert device_detection._parse_mib("16376 MiB") == 16376
    assert device_detection._parse_mib("unknown") == 0
