from __future__ import annotations

from libreprimus.token_block.stage5dj import (
    _parse_id3,
    _parse_pdf,
    validate_stage5dj_761_parable,
    validate_stage5dj_mp3_metadata,
    validate_stage5dj_pdf_metadata,
)

from test_stage5dj_common import ensure_stage5dj_built, load_yaml, write_temp_yaml


def _synchsafe(value: int) -> bytes:
    return bytes(
        [
            (value >> 21) & 0x7F,
            (value >> 14) & 0x7F,
            (value >> 7) & 0x7F,
            value & 0x7F,
        ]
    )


def _text_frame(frame_id: bytes, text: str) -> bytes:
    body = b"\x03" + text.encode("utf-8")
    return frame_id + len(body).to_bytes(4, "big") + b"\x00\x00" + body


def test_stage5dj_synthetic_id3_metadata_parser(tmp_path) -> None:
    frames = (
        _text_frame(b"TIT2", "The Instar Emergence")
        + _text_frame(b"TPE1", "3301")
        + _text_frame(
            b"TXXX",
            "Parable 1,595,277,641\x00Like the instar, tunneling to the surface",
        )
    )
    mp3 = tmp_path / "synthetic.mp3"
    mp3.write_bytes(b"ID3\x03\x00\x00" + _synchsafe(len(frames)) + frames + b"\xff\xfb")

    metadata = _parse_id3(mp3)
    assert metadata["title"] == "The Instar Emergence"
    assert metadata["artist"] == "3301"
    assert metadata["parable_number"] == 1595277641
    assert metadata["metadata_extraction_status"] == "id3_header_metadata_only"


def test_stage5dj_synthetic_pdf_metadata_parser(tmp_path) -> None:
    pdf = tmp_path / "score.pdf"
    pdf.write_bytes(
        b"%PDF-1.7\n1 0 obj << /Title (Interconnected Crab Canon?) "
        b"/Creator (MuseScore Version: 3.6.2) /Producer (Qt 5.9.9) >> endobj\n"
        b"2 0 obj << /Type /Page >> endobj\n"
    )

    metadata = _parse_pdf(pdf)
    assert metadata["title"] == "Interconnected Crab Canon?"
    assert metadata["creator"] == "MuseScore Version: 3.6.2"
    assert metadata["musescore_metadata_detected"] is True


def test_stage5dj_mp3_pdf_and_parable_records_validate() -> None:
    ensure_stage5dj_built()

    assert validate_stage5dj_mp3_metadata()[1] == []
    assert validate_stage5dj_pdf_metadata()[1] == []
    assert validate_stage5dj_761_parable()[1] == []

    parable = load_yaml("data/historical-route/stage5dj-761-parable-metadata-lock.yaml")
    if parable["source_file_exists_in_local_cache"]:
        assert parable["title"] == "The Instar Emergence"
        assert parable["artist"] == "3301"
        assert parable["parable_number"] == 1595277641


def test_stage5dj_mp3_validator_rejects_audio_decode_flag(tmp_path) -> None:
    ensure_stage5dj_built()
    payload = load_yaml("data/historical-route/stage5dj-mp3-metadata-lock.yaml")
    payload["mp3_audio_decoded_now"] = True
    temp = write_temp_yaml(tmp_path / "bad.yaml", payload)

    _, errors = validate_stage5dj_mp3_metadata(record=temp)
    assert any("mp3_audio_decoded" in error for error in errors)
