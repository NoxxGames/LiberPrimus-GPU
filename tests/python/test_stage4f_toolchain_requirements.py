from __future__ import annotations

from libreprimus.stego_fixtures.toolchain_requirements import build_toolchain_requirements


def test_stage4f_toolchain_records_are_separate_and_not_executed() -> None:
    records = build_toolchain_requirements()
    toolchains = {record["toolchain"] for record in records}
    assert toolchains == {"outguess", "openpuff", "mp3stego", "hexdump/strings", "audio_rendering"}
    assert all(record["execution_status"] == "not_executed_stage4f" for record in records)
    assert all(record["solve_claim"] is False for record in records)
