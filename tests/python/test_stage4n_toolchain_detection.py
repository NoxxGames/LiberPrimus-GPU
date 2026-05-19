from __future__ import annotations

from libreprimus.stego_positive_controls.toolchain_detection import detect_toolchains


def test_stage4n_toolchain_unavailable_does_not_fail_validation() -> None:
    records = detect_toolchains()
    assert records
    assert all(record["tool_executed"] is False for record in records)
    assert all(record["execution_performed"] is False for record in records)
    assert all(record.get("tool_path") in {None, "available_on_path"} for record in records)
