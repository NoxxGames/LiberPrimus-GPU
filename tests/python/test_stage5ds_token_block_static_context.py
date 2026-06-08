from __future__ import annotations

from test_stage5ds_common import ensure_stage5ds_built, load_yaml


def test_stage5ds_token_block_primary60_static_metadata() -> None:
    ensure_stage5ds_built()
    scope = load_yaml("data/token-block/stage5ds-token-block-static-machine-code-scope-control.yaml")
    assert scope["token_count"] == 256
    assert scope["row_count"] == 32
    assert scope["column_count"] == 8
    assert scope["first_16_bytes_hex"] == "cbe7a7ba61ed7eb75cf99cdef704b7d4"
    assert len(scope["primary60_byte_stream_sha256"]) == 64
    assert scope["machine_code_execution_performed_now"] is False
    assert scope["full_byte_stream_committed"] is False


def test_stage5ds_token_block_static_candidates_not_execution() -> None:
    ensure_stage5ds_built()
    record = load_yaml(
        "data/historical-route/stage5ds-token-block-machine-code-static-sanity-candidate-v0.yaml"
    )
    assert record["native_code_likelihood"] == "low"
    assert record["vm_or_table_likelihood"] == "medium"
    assert record["byte_stream_generation_authorized_now"] is False
    assert record["token_block_experiment_executed"] is False
