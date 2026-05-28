from test_stage5bm_common import load_yaml


def test_stage5bm_string4_stage5ap_mismatch_counts_are_compact() -> None:
    record = load_yaml("data/token-block/stage5bm-string4-stage5ap-mismatch-analysis.yaml")

    assert record["string4_reparsed_from_local_source"] is True
    assert record["stage5ap_token_count"] == 256
    assert record["string4_decoded_byte_count"] == 256
    assert record["string4_matches_stage5ap_primary60_bytes"] is False
    assert record["mismatch_count"] == 7
    assert record["canonical_match_count"] == 249
    assert len(record["mismatch_summary_records"]) == 7
    assert record["full_mismatch_table_committed"] is False
