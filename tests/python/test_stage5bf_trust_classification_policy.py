from test_stage5bf_local_archive_location import load_yaml


def test_stage5bf_trust_policy_is_not_authenticity_proof() -> None:
    payload = load_yaml("data/historical-route/stage5bf-trust-classification-policy.yaml")
    classes = {record["trust_class"]: record["meaning"] for record in payload["trust_classes"]}

    assert "pgp_block_present_not_verified" in classes
    assert "not a solve or authenticity proof" in classes["primary_signed_or_hashable"]
    assert payload["local_file_hash_proves_originality"] is False
    assert payload["raw_archive_files_committed"] is False
