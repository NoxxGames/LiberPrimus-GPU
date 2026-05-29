from test_stage5by_common import load_yaml


def test_stage5by_record_family_equivalence_map_exists() -> None:
    payload = load_yaml("data/project-state/stage5by-record-family-name-equivalence-map.yaml")
    families = {record["record_family"] for record in payload["equivalence_records"]}
    assert payload["record_family_name_equivalence_map_created"] is True
    assert "stage5bw_inactive_sidecar_proposal" in families
    assert "stage5bw_manifest_supersession_preflight" in families
    assert "stage5bw_source_digest_index" in families
    assert "stage5bw_stage5bd_plan_preservation" in families
