import pytest

from libreprimus.legacy_pastebin.export import extract_legacy_pastebin
from libreprimus.legacy_pastebin.loader import find_default_input
from libreprimus.legacy_pastebin.models import SOURCE_LOCAL_FILENAME


@pytest.fixture(scope="module")
def real_extraction():
    input_path = find_default_input()
    if input_path is None:
        pytest.skip("real local Pastebin TXT source absent")
    return extract_legacy_pastebin(input_path)


def test_real_source_has_many_line_pairs(real_extraction) -> None:
    assert real_extraction.summary.line_pair_count > 100


def test_real_source_records_are_noncanonical(real_extraction) -> None:
    assert all(not record.trusted_as_canonical for record in real_extraction.line_pairs)
    assert real_extraction.summary.canonical_corpus_allowed is False
    assert real_extraction.summary.page_boundary_status == "not_finalized"


def test_real_source_mappings_validate_with_documented_alias_warnings(real_extraction) -> None:
    ratio = sum(1 for record in real_extraction.line_pairs if record.validated_prime_mapping) / len(
        real_extraction.line_pairs
    )
    assert ratio >= 0.95
    assert real_extraction.summary.unknown_prime_value_count == 0


def test_real_source_first_pair_matches_known_values(real_extraction) -> None:
    first = real_extraction.line_pairs[0]
    assert first.rune_words == ["ᛋᚻᛖᚩᚷᛗᛡᚠ", "ᛋᚣᛖᛝᚳ"]
    assert first.prime_words == [[53, 23, 67, 7, 17, 71, 107, 2], [53, 103, 67, 79, 13]]
    assert first.decimal_index_words == [[15, 8, 18, 3, 6, 19, 27, 0], [15, 26, 18, 21, 5]]


def test_real_source_detects_noncanonical_parable_anchor(real_extraction) -> None:
    assert real_extraction.anchors
    assert any(anchor.page_label_candidate == "57.jpg" for anchor in real_extraction.anchors)
    assert all(anchor.canonical_page_boundary is False for anchor in real_extraction.anchors)


def test_real_source_preserves_empty_pairs(real_extraction) -> None:
    assert real_extraction.summary.empty_pair_count >= 1
    assert any(record.empty_pair for record in real_extraction.line_pairs)


def test_real_source_records_local_filename(real_extraction) -> None:
    assert real_extraction.summary.source_local_filename == SOURCE_LOCAL_FILENAME
    assert all(record.source_local_filename == SOURCE_LOCAL_FILENAME for record in real_extraction.line_pairs)
