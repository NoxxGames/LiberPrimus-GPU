from test_stage5bk_common import load_yaml


def test_stage5bk_transcriptions_are_noncanonical_source_locks() -> None:
    payload = load_yaml("data/historical-route/stage5bk-iddqd-v2-transcription-source-lock.yaml")
    assert payload["transcription_source_lock_count"] == 2
    assert payload["transcription_files_found_count"] == 2
    assert payload["trusted_as_canonical"] is False
    assert payload["transcription_bodies_committed"] is False
    assert payload["canonical_transcription_changed"] is False
