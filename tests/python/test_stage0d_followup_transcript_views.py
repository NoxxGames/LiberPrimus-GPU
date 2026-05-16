from pathlib import Path

from libreprimus.transcript_sources.rtkd_master import parse_rtkd_master
from libreprimus.transcript_sources.views import build_transcript_views

F = "\u16a0"
U = "\u16a2"
S = "\u16cb"
H = "\u16bb"


def _write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def test_logical_line_view_splits_slash_delimited_lines(tmp_path: Path) -> None:
    transcript = _write(tmp_path / "rtkd.txt", f"%\n{F}{U}/{S}{H}/\n")
    records, _ = parse_rtkd_master(transcript)

    views, summary = build_transcript_views(records)

    logical = views["logical_line_view"]
    assert summary.physical_line_count == 2
    assert summary.logical_line_count == 2
    assert [record.flattened_rune_sequence for record in logical] == [f"{F}{U}", f"{S}{H}"]
    assert all(not record.trusted_as_canonical for record in logical)


def test_stream_view_maps_offsets_to_physical_lines_and_columns(tmp_path: Path) -> None:
    transcript = _write(tmp_path / "rtkd.txt", f"{F}{U}/\n{S}{H}/\n")
    records, _ = parse_rtkd_master(transcript)

    views, _ = build_transcript_views(records)
    stream = views["rune_stream_view"][0]

    assert stream.flattened_rune_sequence == f"{F}{U}{S}{H}"
    assert stream.offset_map[0]["physical_line_number"] == 1
    assert stream.offset_map[2]["physical_line_number"] == 2
    assert stream.offset_map[2]["source_column"] == 1


def test_page_marker_view_preserves_raw_marker_text(tmp_path: Path) -> None:
    transcript = _write(tmp_path / "rtkd.txt", f"%\n{F}/\n")
    records, _ = parse_rtkd_master(transcript)

    views, summary = build_transcript_views(records)

    assert summary.explicit_marker_count == 1
    assert views["page_marker_view"][0].raw_marker_text == "%"
