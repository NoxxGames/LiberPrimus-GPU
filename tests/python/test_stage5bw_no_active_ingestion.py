from test_stage5bw_common import load_yaml


def test_stage5bw_no_active_ingestion_flags_stay_false() -> None:
    proof = load_yaml("data/token-block/stage5bw-no-active-ingestion-proof.yaml")

    assert proof["active_ingestion_performed"] is False
    assert proof["string4_active_input_allowed"] is False
    assert proof["string4_dry_run_ingestion_allowed_now"] is False
    assert proof["string4_execution_input_allowed"] is False
    assert proof["real_byte_stream_generated"] is False
    assert proof["variant_byte_streams_generated"] is False
    assert proof["full_cartesian_product_enumerated"] is False
    assert proof["dwh_hash_search_performed"] is False
    assert proof["decode_attempt_performed"] is False
    assert proof["scoring_performed"] is False
    assert proof["cuda_execution_performed"] is False
