from __future__ import annotations

from libreprimus.token_block.possible_token_parser import parse_possible_token_notes


def test_stage5aw_parser_extracts_case013_tokens_without_prose() -> None:
    parsed = parse_possible_token_notes(
        "reviewed; possible_tokens=04|O4 row overlay supports ?4 but prefix remains ambiguous"
    )
    assert parsed.possible_tokens == ["04", "O4", "?4"]
    assert "extracted_token_prefix_from_prose_segment" in parsed.cleanup_warnings
    assert "extracted_visual_placeholder_from_prose" in parsed.cleanup_warnings


def test_stage5aw_parser_extracts_case025_tokens_without_prose() -> None:
    parsed = parse_possible_token_notes(
        "reviewed; possible_tokens=3I|3l row overlay supports 3? but suffix remains ambiguous"
    )
    assert parsed.possible_tokens == ["3I", "3l", "3?"]
    assert "extracted_token_prefix_from_prose_segment" in parsed.cleanup_warnings
    assert "extracted_visual_placeholder_from_prose" in parsed.cleanup_warnings
