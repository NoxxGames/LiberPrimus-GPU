from test_stage5bi_fandom_page_triage import load_yaml


def test_stage5bi_spreadsheet_source_lock_is_local_analysis_metadata_only() -> None:
    payload = load_yaml("data/source-harvester/stage5bi-local-spreadsheet-source-lock.yaml")

    assert payload["source_path"] == "third_party/3N_3p_Bases_49-51.jpg.xlsx"
    assert payload["source_role"] == "local_analysis_metadata"
    assert payload["trusted_as_canonical"] is False
    assert payload["spreadsheet_committed"] is False
    assert payload["cell_body_committed"] is False
    assert payload["generated_extract_committed"] is False
    assert payload["canonical_transcription_changed"] is False
    assert payload["active_token_block_manifest_changed"] is False


def test_stage5bi_spreadsheet_reconciliation_does_not_change_stage5aw() -> None:
    payload = load_yaml("data/token-block/stage5bi-spreadsheet-stage5aw-reconciliation.yaml")

    assert payload["spreadsheet_is_local_analysis_metadata"] is True
    assert payload["trusted_as_canonical"] is False
    assert payload["canonical_transcription_changed"] is False
    assert payload["branch_manifest_changed"] is False
    assert payload["active_token_block_manifest_changed"] is False
    assert payload["execution_allowed"] is False
    assert payload["variant_byte_streams_generated"] is False
