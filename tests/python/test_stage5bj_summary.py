from test_stage5bj_crosswalk_closure import load_yaml


def test_stage5bj_summary_counts_match_record_files() -> None:
    summary = load_yaml("data/project-state/stage5bj-summary.yaml")
    closure = load_yaml("data/historical-route/stage5bj-original-archive-crosswalk-closure.yaml")
    surfaces = load_yaml("data/historical-route/stage5bj-2014-exact-surface-source-locks.yaml")
    page_body = load_yaml("data/historical-route/stage5bj-fandom-page-body-crosswalk.yaml")
    media = load_yaml("data/historical-route/stage5bj-media-equivalence-closure.yaml")
    gaps = load_yaml("data/historical-route/stage5bj-source-gap-update.yaml")

    assert summary["crosswalk_closure_record_count"] == len(closure["records"])
    assert summary["exact_512_hex_surface_locked_count"] == surfaces["exact_512_hex_surface_locked_count"]
    assert summary["fandom_page_body_crosswalk_count"] == len(page_body["records"])
    assert summary["media_equivalence_record_count"] == len(media["records"])
    assert summary["source_gap_closed_count"] == gaps["source_gap_closed_count"]
    assert summary["stage5bd_dry_run_records_remain_valid"] is True
    assert summary["future_token_block_execution_remains_blocked"] is True
    assert summary["recommended_next_stage_title"].startswith("Stage 5BK - Historical-route planning")


def test_stage5bj_next_stage_decision_is_metadata_only() -> None:
    payload = load_yaml("data/project-state/stage5bj-next-stage-decision.yaml")

    assert payload["selected_next_stage_id"] == "stage-5bk"
    assert payload["metadata_review_only"] is True
    for key, value in payload.items():
        if key.endswith("_selected") or key == "solve_claim":
            assert value is False, key
