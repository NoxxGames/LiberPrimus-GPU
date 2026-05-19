from __future__ import annotations

from libreprimus.cookie_refresh.byte_variants import apply_byte_variant


def test_stage4g_byte_variants_are_deterministic() -> None:
    text = "Dir/Name File.txt"
    assert apply_byte_variant(text, "raw") == text
    assert apply_byte_variant(text, "lower") == "dir/name file.txt"
    assert apply_byte_variant(text, "upper") == "DIR/NAME FILE.TXT"
    assert apply_byte_variant(text, "trailing_lf") == "Dir/Name File.txt\n"
    assert apply_byte_variant(text, "trailing_crlf") == "Dir/Name File.txt\r\n"
    assert apply_byte_variant(text, "compact_no_spaces") == "Dir/NameFile.txt"
    assert apply_byte_variant(text, "quoted") == '"Dir/Name File.txt"'
    assert apply_byte_variant(text, "url_encoded") == "Dir%2FName%20File.txt"
    assert apply_byte_variant(text, "filename_only") == "Name File.txt"
    assert apply_byte_variant(text, "basename_no_extension") == "Name File"
    assert apply_byte_variant(text, "slash_wrapped") == "/Dir/Name File.txt/"
    assert apply_byte_variant(text, "tmp_path_variant") == "/tmp/Name File.txt"
