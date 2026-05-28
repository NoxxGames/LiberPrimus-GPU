from libreprimus.token_block.stage5bo import _build_errata_records


def _record(case_id: str, index: int, token: str, notes: str) -> dict[str, object]:
    return {
        "challenge_id": case_id,
        "token_index_0_based": index,
        "canonical_token": token,
        "reviewer_notes": notes,
    }


def test_stage5bo_diff_preserves_case_and_character_distinctions() -> None:
    original = {
        "records": [
            _record("stage5at-token-case-198", 198, "1j", "reviewed; possible_tokens=1I|1j"),
            _record("stage5at-token-case-199", 199, "0I", "reviewed; possible_tokens=0I|0j|OI|Oj"),
        ]
    }
    corrected = {
        "records": [
            _record("stage5at-token-case-198", 198, "1j", "reviewed; possible_tokens=1i|1j"),
            _record("stage5at-token-case-199", 199, "0I", "reviewed; possible_tokens=0I|0l|OI|Ol"),
        ]
    }

    records = _build_errata_records(original, corrected)
    by_case = {record["case_id"]: record for record in records}

    assert by_case["stage5at-token-case-198"]["added_tokens"] == ["1i"]
    assert by_case["stage5at-token-case-198"]["removed_tokens"] == ["1I"]
    assert by_case["stage5at-token-case-199"]["corrected_possible_tokens"] == ["0I", "0l", "OI", "Ol"]
    assert by_case["stage5at-token-case-199"]["added_tokens"] == ["0l", "Ol"]
    assert by_case["stage5at-token-case-199"]["removed_tokens"] == ["0j", "Oj"]


def test_stage5bo_duplicate_cleanup_counts_as_possible_token_errata() -> None:
    original = {"records": [_record("stage5at-token-case-042", 42, "0S", "reviewed; possible_tokens=0S|0S|OS|OS")]}
    corrected = {"records": [_record("stage5at-token-case-042", 42, "0S", "reviewed; possible_tokens=0S|OS")]}

    [record] = _build_errata_records(original, corrected)

    assert record["original_possible_tokens"] == ["0S", "OS"]
    assert record["original_possible_token_fragments"] == ["0S", "0S", "OS", "OS"]
    assert record["corrected_possible_token_fragments"] == ["0S", "OS"]
    assert record["possible_tokens_changed"] is True
    assert record["errata_classification"] == "operator_possible_tokens_typo"
