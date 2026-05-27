from test_stage5bi_fandom_page_triage import load_yaml


def test_stage5bi_summary_counts_match_record_files() -> None:
    summary = load_yaml("data/project-state/stage5bi-summary.yaml")
    page_triage = load_yaml("data/historical-route/stage5bi-fandom-page-triage.yaml")
    candidates = load_yaml("data/historical-route/stage5bi-fandom-item-source-lock-candidates.yaml")
    crosswalk = load_yaml("data/historical-route/stage5bi-original-archive-crosswalk-candidates.yaml")
    gaps = load_yaml("data/historical-route/stage5bi-source-gap-register.yaml")
    negative = load_yaml("data/historical-route/stage5bi-negative-control-quarantine.yaml")

    assert summary["fandom_page_triage_count"] == len(page_triage["records"])
    assert summary["item_source_lock_candidate_count"] == len(candidates["records"])
    assert summary["original_archive_crosswalk_candidate_count"] == len(crosswalk["records"])
    assert summary["source_gap_count"] == len(gaps["gaps"])
    assert summary["negative_control_count"] == len(negative["records"])
    assert summary["stage5bd_dry_run_records_remain_valid"] is True
    assert summary["future_token_block_execution_remains_blocked"] is True
    assert summary["active_token_block_manifest_changed"] is False
    assert summary["recommended_next_stage_title"].startswith("Stage 5BJ - Original-archive crosswalk closure")


def test_stage5bi_next_stage_decision_is_metadata_only() -> None:
    payload = load_yaml("data/project-state/stage5bi-next-stage-decision.yaml")

    assert payload["selected_next_stage_id"] == "stage-5bj"
    assert payload["token_block_execution_selected"] is False
    assert payload["dwh_hash_search_selected"] is False
    assert payload["scored_experiments_selected"] is False
    assert payload["benchmark_selected"] is False
    assert payload["cuda_selected"] is False
    assert payload["public_website_expansion_selected"] is False
    assert payload["stego_execution_selected"] is False
    assert payload["pgp_verification_selected"] is False
