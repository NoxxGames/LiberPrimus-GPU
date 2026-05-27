from test_stage5bf_local_archive_location import load_yaml


def test_stage5bf_deep_research_readiness_excludes_raw_archive_bodies() -> None:
    payload = load_yaml("data/historical-route/stage5bf-deep-research-readiness.yaml")

    assert payload["ready_for_deep_research_review"] is True
    assert payload["raw_archive_files_included"] is False
    assert payload["generated_content_pack_committed"] is False
    assert payload["recommended_next_stage"] == "Stage 5BG - Deep Research historical route source-lock review"
