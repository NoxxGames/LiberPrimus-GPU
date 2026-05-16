from pathlib import Path

import pytest

from libreprimus.legacy_workbook.export import extract_workbook
from libreprimus.legacy_workbook.paths import find_default_workbook

EXPECTED_SHEETS = {
    "README",
    "Prime Sums",
    "A Warning",
    "Some Wisdom",
    "Welcome",
    "A Koan A Man",
    "The Loss Of",
    "A Koan During",
    "An Instruction",
    "p57 Parable",
    "p56 An End",
}


@pytest.fixture(scope="module")
def real_extraction():
    workbook_path = find_default_workbook()
    if workbook_path is None:
        pytest.skip("real legacy workbook absent")
    return extract_workbook(workbook_path)


def test_real_workbook_has_expected_sheets(real_extraction) -> None:
    assert EXPECTED_SHEETS.issubset(set(real_extraction.summary.sheet_names))


def test_real_p56_prime_minus_one_first_twenty(real_extraction) -> None:
    expected = [1, 2, 4, 6, 10, 12, 16, 18, 22, 28, 1, 7, 11, 13, 17, 23, 0, 2, 8, 12]
    observed = [
        record.cipher_minus_message_mod29
        for record in real_extraction.delta_records
        if record.sheet_name == "p56 An End"
    ][:20]
    assert observed == expected


def test_real_welcome_divinity_first_seventeen(real_extraction) -> None:
    expected = [23, 10, 1, 10, 9, 10, 16, 26, 23, 10, 1, 10, 9, 10, 16, 26, 23]
    observed = [
        record.cipher_minus_message_mod29
        for record in real_extraction.delta_records
        if record.sheet_name == "Welcome"
    ][:17]
    assert observed == expected


def test_real_direct_pages_have_zero_deltas(real_extraction) -> None:
    direct_pages = {"Some Wisdom", "The Loss Of", "An Instruction", "p57 Parable"}
    for page in direct_pages:
        records = [
            record
            for record in real_extraction.delta_records
            if record.sheet_name == page and record.cipher_minus_message_mod29 is not None
        ]
        assert records
        assert all(
            record.cipher_minus_message_mod29 == 0 and record.message_minus_cipher_mod29 == 0
            for record in records
        )


def test_real_prime_sums_have_parsed_rows(real_extraction) -> None:
    assert any(
        record.tokens
        and record.prime_values
        and record.sum is not None
        and (record.is_prime is None or isinstance(record.is_prime, bool))
        for record in real_extraction.prime_sum_records
    )


def test_real_records_are_noncanonical(real_extraction) -> None:
    assert not any(record.trusted_as_canonical for record in real_extraction.sheet_records)
    assert not any(record.trusted_as_canonical for record in real_extraction.delta_records)
    assert not any(record.trusted_as_canonical for record in real_extraction.prime_sum_records)
    assert real_extraction.summary.canonical_corpus_allowed is False
    assert real_extraction.summary.trusted_as_canonical is False
