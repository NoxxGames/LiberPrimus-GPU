from __future__ import annotations

from libreprimus.native_cpu.runner import python_reference_run
from libreprimus.native_cpu.validation import validate_stage5d_results


def test_stage5d_python_reference_is_deterministic() -> None:
    one = python_reference_run(threads=1)
    two = python_reference_run(threads=2)
    assert one["output_hash"] == two["output_hash"]
    assert [record["candidate_id"] for record in one["records"]] == [
        "native-shift-00",
        "native-shift-01",
        "native-shift-03",
        "native-shift-07",
        "native-shift-13",
        "native-shift-28",
    ]


def test_stage5d_committed_records_validate() -> None:
    counts, errors = validate_stage5d_results()
    assert errors == []
    assert counts["thread_counts_tested"] == [1, 2, 4, 8, 16]
    assert counts["one_thread_equals_multi_thread"] is True
    assert counts["python_native_parity"] is True
