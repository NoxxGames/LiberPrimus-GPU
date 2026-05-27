from test_stage5bf_local_archive_location import load_yaml


def test_stage5bf_trust_classifications_hash_lock_without_raw_commit() -> None:
    payload = load_yaml("data/historical-route/stage5bf-artifact-trust-classifications.yaml")

    assert payload["hash_locked_artifact_count"] == 1017
    assert payload["trust_class_counts"]["pgp_block_present_not_verified"] == 81
    assert payload["classifications"][0]["raw_commit_allowed"] is False
    assert payload["classifications"][0]["sha256"]
