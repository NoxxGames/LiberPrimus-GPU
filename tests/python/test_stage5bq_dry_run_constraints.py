from test_stage5bq_common import load_yaml


def test_stage5bq_dry_run_constraint_does_not_change_current_plans() -> None:
    payload = load_yaml("data/token-block/stage5bq-errata-aware-dry-run-constraint-update.yaml")

    assert "future_runner_citation_required" in payload["dry_run_planning_effects"]
    assert payload["current_stage5bd_dry_run_plan_changed"] is False
    assert payload["current_run_plan_ids_changed"] is False
    assert payload["string4_added_to_active_dry_run_inputs"] is False


def test_stage5bq_no_active_ingestion_proof_blocks_inputs() -> None:
    payload = load_yaml("data/token-block/stage5bq-string4-no-active-ingestion-proof.yaml")

    assert payload["stage5bo_errata_aware_universe_active"] is False
    assert payload["stage5bd_run_plan_ids_changed"] is False
    assert payload["real_byte_stream_generated"] is False
    assert payload["variant_materialisation_performed"] is False


def test_stage5bq_stage5bd_lineage_preserved() -> None:
    payload = load_yaml("data/token-block/stage5bq-stage5bd-dry-run-lineage-preservation.yaml")

    assert payload["stage5bd_dry_run_records_remain_valid"] is True
    assert payload["run_plan_ids_changed"] is False
    assert payload["string4_added_to_dry_run_plan_inputs"] is False
