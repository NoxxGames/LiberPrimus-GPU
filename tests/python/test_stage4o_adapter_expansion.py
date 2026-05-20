from __future__ import annotations

from pathlib import Path

from libreprimus.cpu_batch.adapter_expansion import build_adapter_coverage


def test_stage4o_adapter_expansion_reports_supported_and_deferred(tmp_path: Path) -> None:
    payload = build_adapter_coverage(
        registry_path=Path("data/transform-registry/cpu-reference-transforms-v0.json"),
        out_dir=tmp_path,
    )
    assert payload["supported_adapter_count"] >= 9
    assert payload["deferred_adapter_count"] >= 1
    deferred = [record for record in payload["records"] if record["adapter_status"] == "deferred"]
    assert all(record["reason"] for record in deferred)


def test_stage4o_adapter_expansion_marks_hash_and_stego_non_adapters(tmp_path: Path) -> None:
    payload = build_adapter_coverage(
        registry_path=Path("data/transform-registry/cpu-reference-transforms-v0.json"),
        out_dir=tmp_path,
    )
    unsupported = {record["transform_family"] for record in payload["records"] if record["adapter_status"] == "unsupported_by_design"}
    assert "cookie_hash" in unsupported
    assert "stego_audio" in unsupported
