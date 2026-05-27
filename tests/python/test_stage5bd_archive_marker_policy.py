from pathlib import Path

import yaml


def test_stage5bd_archive_marker_policy_requires_review_markers() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bd-archive-marker-policy.yaml").read_text())

    assert payload["archive_commit_marker_required_for_future_zip_reviews"] is True
    assert payload["generated_zips_committed"] is False
    assert {"ARCHIVE_COMMIT.txt", "ARCHIVE_MANIFEST.json"}.issubset(
        set(payload["recommended_marker_files"])
    )
