from test_stage5bn_common import load_yaml


def test_stage5bn_source_evidence_supports_inactive_addendum_only() -> None:
    payload = load_yaml("data/token-block/stage5bn-string4-unsupported-position-source-evidence.yaml")

    statuses = {record["evidence_class"]: record["status"] for record in payload["evidence_records"]}
    assert statuses["committed_stage5aw_metadata"] == "unsupported"
    assert statuses["local_spreadsheet_target_cell"] == "supported"
    assert statuses["local_iddqd_v2_string4"] == "supports_0l_as_string4_inferred_token"
    assert payload["evidence_supports_add_0l_as_possible_option"] is True
    assert payload["evidence_supports_external_mismatch_retained"] is False
    assert payload["human_review_required"] is False
    assert payload["raw_bodies_committed"] is False
    assert payload["generated_review_images_committed"] is False
