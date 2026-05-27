from pathlib import Path

import yaml


def test_stage5bd_archive_review_marker_records_commit_context() -> None:
    payload = yaml.safe_load(Path("data/project-state/stage5bd-archive-review-marker.yaml").read_text())

    assert payload["stage_id"] == "stage-5bd"
    assert payload["archive_commit_marker_required_for_future_zip_reviews"] is True
    assert payload["git_directory_required_in_review_zip"] is False
    assert payload["current_commit_detected"]
