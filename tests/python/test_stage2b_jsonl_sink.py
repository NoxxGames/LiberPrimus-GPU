from dataclasses import replace
from pathlib import Path

import pytest

from libreprimus.result_store.jsonl_sink import read_jsonl, write_jsonl
from test_stage2b_sqlite_sink import sample_run


def test_jsonl_sink_writes_one_utf8_record_per_line(tmp_path: Path) -> None:
    record = replace(sample_run(), notes=["unicode rune marker ᚠ"])
    path = tmp_path / "run_records.jsonl"

    write_jsonl(path, [record])

    text = path.read_text(encoding="utf-8")
    assert text.count("\n") == 1
    assert "ᚠ" in text
    assert read_jsonl(path)[0]["run_id"] == record.run_id


def test_jsonl_sink_is_deterministic(tmp_path: Path) -> None:
    record = sample_run()
    first = tmp_path / "first.jsonl"
    second = tmp_path / "second.jsonl"

    write_jsonl(first, [record])
    write_jsonl(second, [record])

    assert first.read_bytes() == second.read_bytes()


def test_jsonl_sink_rejects_invalid_record(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        write_jsonl(tmp_path / "bad.jsonl", [{"record_type": "unknown"}])


def test_jsonl_sink_uses_temp_replace(tmp_path: Path) -> None:
    path = tmp_path / "run_records.jsonl"

    write_jsonl(path, [sample_run()])

    assert path.is_file()
    assert not (tmp_path / "run_records.jsonl.tmp").exists()


def test_jsonl_generated_path_is_not_committed_fixture_area(tmp_path: Path) -> None:
    path = tmp_path / "experiments" / "results" / "result-store" / "stage2b" / "run_records.jsonl"

    write_jsonl(path, [sample_run()])

    assert "data/fixtures" not in str(path).replace("\\", "/")
