from pathlib import Path

from test_stage5bs_common import ROOT, load_yaml


def test_stage5bs_preserves_stage5bd_plan_and_active_manifests() -> None:
    stage5bd = load_yaml("data/token-block/stage5bs-stage5bd-plan-preservation.yaml")
    active = load_yaml("data/token-block/stage5bs-active-manifest-preservation.yaml")

    assert stage5bd["stage5bd_dry_run_records_remain_valid"] is True
    assert stage5bd["stage5bd_dry_run_plan_changed"] is False
    assert stage5bd["stage5bd_run_plan_ids_changed"] is False
    assert stage5bd["string4_added_to_active_dry_run_inputs"] is False
    assert active["active_token_block_manifest_changed"] is False
    assert active["stage5aw_branch_manifest_changed"] is False
    assert active["stage5az_variant_family_manifest_changed"] is False
    paths = active["preserved_active_record_paths"]
    assert "data/token-block/stage5aw-repaired-branch-manifest.yaml" not in paths
    assert "data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml" in paths
    assert all((ROOT / Path(path)).is_file() for path in paths)


def test_stage5bs_no_active_ingestion_proof_blocks_string4_use() -> None:
    payload = load_yaml("data/token-block/stage5bs-no-active-ingestion-proof.yaml")

    assert payload["stage5bd_run_plan_ids_changed"] is False
    assert payload["stage5bd_dry_run_plan_manifest_changed"] is False
    assert payload["canonical_transcription_changed"] is False
    assert payload["string4_active_input_allowed"] is False
    assert payload["string4_byte_stream_generation_allowed"] is False
    assert payload["real_byte_stream_generated"] is False


def test_stage5bs_dwh_quarantine_and_guardrail_block_execution() -> None:
    dwh = load_yaml("data/historical-route/stage5bs-dwh-quarantine-reaffirmation.yaml")
    guardrail = load_yaml("data/historical-route/stage5bs-guardrail.yaml")

    assert dwh["dwh_relationship_status"] == "quarantined"
    assert dwh["hash_search_performed"] is False
    assert dwh["decode_attempt_performed"] is False
    assert guardrail["planning_ingestion_gate_only"] is True
    assert guardrail["future_token_block_execution_remains_blocked"] is True
    assert guardrail["cuda_execution_performed"] is False
    assert guardrail["solve_claim"] is False
