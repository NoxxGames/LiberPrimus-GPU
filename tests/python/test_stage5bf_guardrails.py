from test_stage5bf_local_archive_location import load_yaml


def test_stage5bf_guardrails_preserve_no_execution_boundary() -> None:
    payload = load_yaml("data/historical-route/stage5bf-guardrail.yaml")

    assert payload["historical_source_lock_only"] is True
    assert payload["execution_performed"] is False
    assert payload["token_experiments_executed"] is False
    assert payload["real_token_block_byte_streams_generated"] is False
    assert payload["outguess_execution_performed"] is False
    assert payload["pgp_network_key_fetch_performed"] is False
    assert payload["hash_preimage_claim"] is False
    assert payload["cuda_execution_performed"] is False
    assert payload["cuda_source_modified"] is False
    assert payload["new_cuda_kernels_added"] == 0
    assert payload["solve_claim"] is False
