from test_stage5bq_common import load_yaml


def test_stage5bq_active_manifests_are_preserved() -> None:
    payload = load_yaml("data/token-block/stage5bq-active-manifest-preservation.yaml")

    assert payload["canonical_transcription_changed"] is False
    assert payload["stage5aw_branch_manifest_changed"] is False
    assert payload["stage5ay_branch_eligibility_changed"] is False
    assert payload["stage5az_variant_family_manifest_changed"] is False
    assert payload["active_token_block_manifest_changed"] is False


def test_stage5bq_source_gap_closed_for_metadata_only() -> None:
    payload = load_yaml("data/historical-route/stage5bq-source-gap-severity-update.yaml")
    record = payload["records"][0]

    assert record["status_after_stage5bq"] == "closed_for_metadata_planning_only"
    assert record["blocks_metadata_planning"] is False
    assert record["blocks_string4_ingestion_or_active_use"] is True
    assert record["blocks_future_token_block_execution"] is True


def test_stage5bq_dwh_quarantine_forbids_search() -> None:
    payload = load_yaml("data/historical-route/stage5bq-dwh-quarantine-reaffirmation.yaml")

    assert payload["DWH_relationship_remains_quarantined"] is True
    assert payload["string4_is_not_dwh_target"] is True
    assert payload["hash_search_performed"] is False
    assert payload["hash_preimage_search_performed"] is False
    assert payload["decode_attempt_performed"] is False


def test_stage5bq_guardrail_blocks_all_execution_surfaces() -> None:
    payload = load_yaml("data/historical-route/stage5bq-guardrail.yaml")

    assert payload["operator_errata_dry_run_planning_integration_only"] is True
    assert payload["future_token_block_execution_remains_blocked"] is True
    assert payload["string4_active_input_allowed"] is False
    assert payload["real_byte_stream_generated"] is False
    assert payload["cuda_execution_performed"] is False
    assert payload["solve_claim"] is False
