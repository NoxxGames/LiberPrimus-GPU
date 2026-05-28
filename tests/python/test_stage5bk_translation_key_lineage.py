from test_stage5bk_common import load_yaml


def test_stage5bk_translation_key_lineage_creates_no_manifest() -> None:
    payload = load_yaml("data/historical-route/stage5bk-iddqd-v2-translation-key-lineage.yaml")
    assert payload["lineage_record_count"] == 4
    assert payload["lineage_files_found_count"] == 4
    assert payload["translation_or_key_bodies_committed"] is False
    assert payload["solver_manifest_created"] is False
    assert "keys_divinity_and_firfumferenfe_lineage_reference" in payload["compact_key_facts"]
