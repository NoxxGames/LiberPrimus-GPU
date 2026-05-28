from test_stage5bm_common import load_yaml


def test_stage5bm_source_gap_severity_adds_string4_row() -> None:
    record = load_yaml("data/historical-route/stage5bm-source-gap-severity-update.yaml")
    gap = record["records"][-1]

    assert gap["source_gap_id"] == "stage5bk-string4-stage5ap-branch-membership-unreconciled"
    assert gap["closure_status"] == "partially_closed_branch_match"
    assert gap["blocks_string4_ingestion_or_active_use"] is True
    assert record["new_source_gap_count"] == 1
