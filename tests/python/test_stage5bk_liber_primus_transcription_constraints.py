from test_stage5bk_common import load_yaml


def test_stage5bk_liber_primus_transcription_constraints_keep_corpus_inactive() -> None:
    payload = load_yaml("data/historical-route/stage5bk-liber-primus-transcription-constraint-integration.yaml")
    assert "trusted_as_canonical_false" in payload["constraints"]
    assert payload["canonical_corpus_active"] is False
    assert payload["canonical_transcription_changed"] is False
