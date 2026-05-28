from test_stage5bk_common import load_yaml


def test_stage5bk_book_code_constraints_are_reference_only() -> None:
    payload = load_yaml("data/historical-route/stage5bk-book-code-and-text-reference-constraint-integration.yaml")
    assert "source_text_edition_required" in payload["constraints"]
    assert payload["book_code_execution_performed"] is False
    assert payload["decode_attempt_performed"] is False
