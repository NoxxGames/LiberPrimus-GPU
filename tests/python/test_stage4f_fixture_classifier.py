from __future__ import annotations

from libreprimus.stego_fixtures.fixture_classifier import build_audio_fixture_records, build_outguess_fixture_records


def test_stage4f_classifier_identifies_lp_outguessed() -> None:
    records = build_outguess_fixture_records([], [])
    assert any(record["source_path"] == "lp_outguessed/" for record in records)


def test_stage4f_classifier_identifies_interconnectedness_mp3() -> None:
    records = build_audio_fixture_records([])
    assert any(record["source_path"] == "2014/05/3301 - Interconnectedness.mp3" for record in records)


def test_stage4f_classifier_identifies_4gq25_image() -> None:
    records = build_outguess_fixture_records([], [])
    assert any(record["source_path"] == "2016/01/4gq25.jpg" for record in records)


def test_stage4f_classifier_keeps_no_solve_claim() -> None:
    records = [*build_outguess_fixture_records([], []), *build_audio_fixture_records([])]
    assert records
    assert all(record["solve_claim"] is False for record in records)
    assert all(record["trusted_as_canonical"] is False for record in records)
