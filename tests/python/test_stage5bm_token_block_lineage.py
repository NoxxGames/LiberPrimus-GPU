from test_stage5bm_common import load_yaml


def test_stage5bm_token_block_lineage_is_preserved() -> None:
    record = load_yaml("data/token-block/stage5bm-token-block-lineage-preservation.yaml")

    assert "data/token-block/stage5ap-token-block-canonical-transcription.yaml" in record["source_records"]
    assert record["canonical_transcription_changed"] is False
    assert record["stage5aw_branch_manifest_changed"] is False
    assert record["stage5bd_dry_run_records_remain_valid"] is True
    assert record["future_token_block_execution_remains_blocked"] is True
