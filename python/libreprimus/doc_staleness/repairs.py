"""Document staleness repair metadata helpers."""

from __future__ import annotations


def repair_summary_record(*, before_count: int, after_count: int, repaired_paths: list[str]) -> dict:
    return {
        "record_type": "stage5ab_doc_staleness_repair_summary",
        "before_finding_count": before_count,
        "after_finding_count": after_count,
        "repaired_paths": sorted(repaired_paths),
    }
