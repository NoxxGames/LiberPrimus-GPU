from libreprimus.legacy_workbook.inventory import classify_sheet
from libreprimus.legacy_workbook.models import SOURCE_ID, SheetRecord, to_jsonable
from libreprimus.legacy_workbook.prime_sums import parse_bool_like


def test_classify_known_sheets() -> None:
    assert classify_sheet("README") == "readme"
    assert classify_sheet("Prime Sums") == "prime_sums"
    assert classify_sheet("Welcome") == "solved_delta_sheet"
    assert classify_sheet("unknown") == "unknown"


def test_bool_like_values() -> None:
    assert parse_bool_like(True) == (True, "True")
    assert parse_bool_like("TRUE") == (True, "TRUE")
    assert parse_bool_like("PRAWDA") == (True, "PRAWDA")
    assert parse_bool_like("prawda") == (True, "prawda")
    assert parse_bool_like(1) == (True, "1")
    assert parse_bool_like(False) == (False, "False")
    assert parse_bool_like("FALSE") == (False, "FALSE")
    assert parse_bool_like("FAŁSZ") == (False, "FAŁSZ")
    assert parse_bool_like("FALSZ") == (False, "FALSZ")
    assert parse_bool_like(0) == (False, "0")


def test_to_jsonable_dataclass() -> None:
    record = SheetRecord(
        record_type="legacy_workbook_sheet",
        source_id=SOURCE_ID,
        workbook_sha256="abc",
        sheet_index=0,
        sheet_name="README",
        max_row=1,
        max_column=1,
        non_empty_cell_count=1,
        formula_cell_count=0,
        classification="readme",
        trusted_as_canonical=False,
        trusted_as_solved_fixture_hint=False,
    )

    payload = to_jsonable(record)
    assert payload["record_type"] == "legacy_workbook_sheet"
    assert payload["trusted_as_canonical"] is False
