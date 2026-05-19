from __future__ import annotations

from libreprimus.stego_positive_controls.fixture_classifier import classify_audio_fixture, classify_outguess_fixture


def test_stage4n_classifier_identifies_lp_outguessed() -> None:
    record = {"fixture_id": "case", "artifact_type": "lp_outguessed", "source_path": "lp_outguessed/"}
    assert classify_outguess_fixture(record) == "lp_outguessed_reference"


def test_stage4n_classifier_identifies_audio_candidate() -> None:
    record = {"fixture_id": "stage4f-iddqd-761-mp3-instar", "source_path": "2013/02/761.MP3"}
    assert classify_audio_fixture(record) == "mp3_instar_candidate"


def test_stage4n_classifier_identifies_image_fixture() -> None:
    record = {"fixture_id": "case", "artifact_type": "image_fixture_candidate", "source_path": "2016/01/4gq25.jpg"}
    assert classify_outguess_fixture(record) == "image_fixture_candidate"
