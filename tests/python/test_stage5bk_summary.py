from test_stage5bk_common import load_yaml


def test_stage5bk_summary_counts_match_records() -> None:
    summary = load_yaml("data/project-state/stage5bk-summary.yaml")
    byte_strings = load_yaml("data/historical-route/stage5bk-iddqd-v2-byte-strings-source-lock.yaml")
    gaps = load_yaml("data/historical-route/stage5bk-source-gap-severity-register.yaml")
    errata = load_yaml("data/historical-route/stage5bk-stage5bj-crosswalk-review-and-errata.yaml")
    assert summary["status"] == "complete"
    assert summary["iddqd_v2_byte_string_count"] == byte_strings["byte_string_count"]
    assert summary["source_gap_severity_record_count"] == gaps["source_gap_severity_record_count"]
    assert summary["stage5bj_crosswalk_errata_count"] == errata["stage5bj_crosswalk_errata_count"]
    assert summary["codex_output_directory_used"] is False
