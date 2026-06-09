from __future__ import annotations

from test_stage5du_common import ensure_stage5du_built, load_yaml


def test_stage5du_source_lock_register_represents_required_thread_folders() -> None:
    ensure_stage5du_built()
    register = load_yaml("data/source-harvester/stage5du-community-thread-source-lock-register.yaml")
    roots = {record["source_root_id"]: record for record in register["source_roots"]}

    expected = {
        "big_gaps_found_in_liber_primus",
        "cribbing_page15",
        "mobius_totient_first_page_theory",
        "potential_crib_red_runes_pages_54_55",
        "red_runes_possible_koan_connection",
        "star_artifacts_in_lp_page_images",
    }
    assert set(roots) == expected
    assert all(record["source_status"] == "local_ignored_metadata_locked" for record in roots.values())
    assert all(record["source_root_exists"] is True for record in roots.values())
    assert all(record["messages_txt_present"] is True for record in roots.values())


def test_stage5du_file_inventory_is_metadata_only() -> None:
    ensure_stage5du_built()
    inventory = load_yaml("data/source-harvester/stage5du-community-thread-file-inventory.yaml")
    assert inventory["file_count"] == 234
    assert inventory["image_file_count"] == 148
    assert inventory["python_file_count"] == 39
    assert inventory["spreadsheet_file_count"] == 2
    assert inventory["raw_third_party_files_committed"] is False
    assert inventory["community_code_executed_now"] is False


def test_stage5du_canonical_page_root_crosslink_records_local_metadata_only() -> None:
    ensure_stage5du_built()
    crosslink = load_yaml("data/source-harvester/stage5du-canonical-lp-page-image-root-crosslink.yaml")
    assert crosslink["canonical_page_image_root_exists"] is True
    assert crosslink["canonical_page_count_observed"] == 75
    assert crosslink["image_forensics_performed"] is False
    assert crosslink["ocr_performed"] is False
