from __future__ import annotations

from libreprimus.token_block.alphabets import build_alphabet_registry
from libreprimus.token_block.models import PRIMARY_ALPHABET
from libreprimus.token_block.transcription import build_transcription


def test_stage5ap_primary_alphabet_registry_records_absent_lowercase_f(tmp_path) -> None:
    transcription = tmp_path / "transcription.yaml"
    build_transcription(out=transcription)
    record = build_alphabet_registry(transcription=transcription, out=tmp_path / "alphabet.yaml")
    assert record["primary_alphabet"] == PRIMARY_ALPHABET
    assert record["primary_alphabet_length"] == 60
    assert record["observed_suffix_count"] == 59
    assert record["lowercase_f_absent"] is True
    assert record["trusted_as_canonical"] is False
