from test_stage5bj_crosswalk_closure import load_yaml


def test_boards_thread_local_archive_equivalent_is_metadata_only() -> None:
    payload = load_yaml("data/historical-route/stage5bj-boards-thread-crosswalk.yaml")

    assert payload["thread_found"] is True
    assert payload["thread_crosswalk_status"] == "route_equivalent_archive_doc_found"
    assert payload["primary_archive_path"].endswith("Pages 49 to 51 and 256 Byte Strings.docx")
    assert payload["primary_archive_sha256"]
    assert payload["raw_archive_files_committed"] is False
    assert payload["thread_body_committed"] is False
    assert payload["future_token_block_execution_remains_blocked"] is True
    assert payload["solve_claim"] is False
