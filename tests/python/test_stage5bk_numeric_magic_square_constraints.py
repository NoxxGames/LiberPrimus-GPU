from test_stage5bk_common import load_yaml


def test_stage5bk_numeric_magic_square_constraints_require_controls() -> None:
    payload = load_yaml("data/historical-route/stage5bk-numeric-and-magic-square-constraint-integration.yaml")
    assert "null_controls_required" in payload["constraints"]
    assert payload["numeric_or_magic_square_execution_performed"] is False
    assert payload["hash_search_performed"] is False
