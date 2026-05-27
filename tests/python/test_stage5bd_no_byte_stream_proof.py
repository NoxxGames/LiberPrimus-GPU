from pathlib import Path

import yaml


def test_stage5bd_no_byte_stream_proof_blocks_materialisation() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bd-no-byte-stream-proof.yaml").read_text())

    assert payload["real_token_block_byte_streams_generated"] is False
    assert payload["real_variant_byte_streams_generated"] is False
    assert payload["real_variant_branches_materialised"] is False
    assert payload["full_cartesian_product_enumerated"] is False
