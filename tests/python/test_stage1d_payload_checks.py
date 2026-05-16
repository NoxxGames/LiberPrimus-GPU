from libreprimus.solved_fixtures.prime_stream import evaluate_payload_checks


def _check(expected_sha: str) -> dict:
    return {
        "payload_id": "hex",
        "payload_kind": "hex_literal_block",
        "expected_payload_text": "abc123",
        "expected_payload_sha256": expected_sha,
        "payload_selector": {
            "selector_kind": "explicit_logical_line_range",
            "start_logical_line_index": 1,
            "end_logical_line_index": 1,
        },
        "preservation_policy": "preserve_exact_normalized_hex",
    }


def test_hex_payload_is_preserved_exactly_and_hashes() -> None:
    result = evaluate_payload_checks(
        [
            {"token_kind": "unknown_symbol", "raw_text": "abc", "logical_line_index": 1},
            {"token_kind": "numeric_literal", "raw_text": "123", "logical_line_index": 1},
        ],
        [_check("6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090")],
    )

    assert result[0]["match_status"] == "pass"
    assert result[0]["payload_length"] == 6


def test_payload_hash_mismatch_fails() -> None:
    result = evaluate_payload_checks(
        [{"token_kind": "numeric_literal", "raw_text": "123", "logical_line_index": 1}],
        [_check("bad")],
    )

    assert result[0]["match_status"] == "fail"


def test_missing_payload_is_pending_with_warning() -> None:
    result = evaluate_payload_checks([], [_check("bad")])

    assert result[0]["match_status"] == "pending"
    assert result[0]["warnings"]
