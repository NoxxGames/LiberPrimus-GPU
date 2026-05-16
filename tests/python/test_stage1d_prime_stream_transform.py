from pathlib import Path

from libreprimus.solved_fixtures.prime_stream import decode_prime_minus_one_stream


def _chain(skip_rule: dict | None = None) -> list[dict]:
    params = {
        "prime_start_index": 0,
        "direction": "forward",
        "stream_value": "prime_minus_one_mod29",
        "advance_on": "enciphered_rune_tokens_only",
        "equivalent_aliases": ["phi_prime_stream"],
    }
    if skip_rule is not None:
        params["skip_rule"] = skip_rule
    return [{"name": "prime_minus_one_stream", "params": params}]


def test_prime_stream_decrypt_formula_and_advancement_rules() -> None:
    result = decode_prime_minus_one_stream(
        [
            {"token_kind": "rune", "index29": 1, "token_index_global": 0},
            {"token_kind": "word_separator", "raw_text": "-", "token_index_global": 1},
            {"token_kind": "numeric_literal", "raw_text": "7", "token_index_global": 2},
            {"token_kind": "rune", "index29": 3, "token_index_global": 3},
        ],
        transform_chain=_chain(),
    )

    assert result["decoded_normalized_plaintext"] == "F 7U"
    assert result["prime_values_used_count"] == 2
    assert result["first_prime_values"][:2] == [2, 3]
    assert "prime_i" in result["decoded_index_formula"]


def test_payload_tokens_do_not_advance_stream() -> None:
    result = decode_prime_minus_one_stream(
        [
            {"token_kind": "rune", "index29": 1, "token_index_global": 0, "logical_line_index": 0},
            {"token_kind": "numeric_literal", "raw_text": "abc123", "token_index_global": 1, "logical_line_index": 1},
            {"token_kind": "rune", "index29": 3, "token_index_global": 2, "logical_line_index": 2},
        ],
        transform_chain=_chain(),
        payload_checks=[
            {
                "payload_id": "payload",
                "payload_kind": "hex_literal_block",
                "expected_payload_text": "abc123",
                "expected_payload_sha256": "6ca13d52ca70c883e0f0bb101e425a89e8624de51db2d2392593af6a84118090",
                "payload_selector": {
                    "selector_kind": "explicit_logical_line_range",
                    "start_logical_line_index": 1,
                    "end_logical_line_index": 1,
                },
                "preservation_policy": "preserve_exact_normalized_hex",
            }
        ],
    )

    assert result["decoded_normalized_plaintext"] == "FU"
    assert result["stream_values_used_count"] == 2
    assert result["payload_check_results"][0]["match_status"] == "pass"


def test_cleartext_f_skip_is_fixture_declared_and_does_not_advance_stream() -> None:
    rule = {
        "name": "cleartext_f_pass_through",
        "cleartext_pass_through_rune_indices": [0],
        "advance_stream_on_skip": False,
    }
    result = decode_prime_minus_one_stream(
        [
            {"token_kind": "rune", "index29": 0, "token_index_global": 10},
            {"token_kind": "word_separator", "raw_text": "-", "token_index_global": 11},
            {"token_kind": "rune", "index29": 1, "token_index_global": 12},
        ],
        transform_chain=_chain(rule),
    )

    assert result["decoded_normalized_plaintext"] == "F F"
    assert result["skip_rule_applied_count"] == 1
    assert result["prime_values_used_count"] == 1


def test_skip_rule_not_applied_unless_declared() -> None:
    result = decode_prime_minus_one_stream(
        [{"token_kind": "rune", "index29": 0, "token_index_global": 0}],
        transform_chain=_chain(),
    )

    assert result["decoded_normalized_plaintext"] == "EA"
    assert result["skip_rule_applied_count"] == 0


def test_no_search_or_cuda_behaviour_is_exposed() -> None:
    source = Path("python/libreprimus/solved_fixtures/prime_stream.py").read_text(encoding="utf-8").lower()
    assert "cuda" not in source
    assert "score" not in source
    assert "offset search" not in source
