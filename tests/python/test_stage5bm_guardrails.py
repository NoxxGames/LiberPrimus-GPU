from test_stage5bm_common import load_yaml


def test_stage5bm_guardrails_block_execution_and_publication() -> None:
    record = load_yaml("data/historical-route/stage5bm-guardrail.yaml")

    assert record["string4_branch_crosswalk_metadata_only"] is True
    assert record["canonical_transcription_changed"] is False
    assert record["real_token_block_byte_streams_generated"] is False
    assert record["full_cartesian_product_enumerated"] is False
    assert record["dwh_hash_search_performed"] is False
    assert record["cuda_execution_performed"] is False
    assert record["solve_claim"] is False
