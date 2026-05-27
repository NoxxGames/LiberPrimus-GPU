from test_stage5bf_local_archive_location import load_yaml


def test_stage5bf_archive_inventory_summary_keeps_full_inventory_generated() -> None:
    payload = load_yaml("data/historical-route/stage5bf-archive-source-inventory-summary.yaml")

    assert payload["total_file_count"] == 1243
    assert payload["high_priority_artifact_count"] == 1043
    assert payload["source_gap_count"] == 4
    assert payload["full_inventory_output"] == "experiments/results/historical-route/stage5bf/full_archive_file_inventory.jsonl"
    assert payload["full_inventory_committed"] is False
    assert payload["raw_archive_files_committed"] is False
