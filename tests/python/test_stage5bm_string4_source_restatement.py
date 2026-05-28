from test_stage5bm_common import load_yaml


def test_stage5bm_string4_source_restatement_preserves_hashes_without_body() -> None:
    record = load_yaml("data/token-block/stage5bm-string4-source-restatement.yaml")

    assert record["source_byte_string_id"] == "stage5bk-iddqd-v2-byte-string-4"
    assert record["hex_length"] == 512
    assert record["claimed_byte_length_if_hex"] == 256
    assert record["string4_hex_sha256"] == "93ee9ddeda9e30ae42827d9f61b4192d4da15726781f822d401d888ea6e96e6d"
    assert record["string4_decoded_byte_sha256"] == "3b9b07d9a26e6d55c432d94d2661fdff3c2b348daed06821f2bdb23184a4b290"
    assert record["full_hex_body_committed"] is False
    assert record["decoded_byte_body_committed"] is False
    assert record["reconstructed_token_stream_committed"] is False
