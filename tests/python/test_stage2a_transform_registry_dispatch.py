import pytest

from libreprimus.transforms.dispatch import dispatch_transform
from libreprimus.transforms.registry import load_registry


def _rune(index: int, label: str = "F") -> dict:
    return {"token_index_global": 0, "logical_line_index": 0, "token_kind": "rune", "index29": index, "latin_label": label}


def test_dispatch_known_reference_transforms() -> None:
    registry = load_registry()

    direct = dispatch_transform(
        registry=registry,
        transform_id="direct_translation",
        tokens=[_rune(0)],
        parameters={},
    )
    reverse = dispatch_transform(
        registry=registry,
        transform_id="reverse_gematria",
        tokens=[_rune(0)],
        parameters={},
    )
    assert direct.decoded_normalized_plaintext == "F"
    assert reverse.decoded_normalized_plaintext == "EA"
    rotated = dispatch_transform(
        registry=registry,
        transform_id="rotated_reverse_gematria",
        tokens=[_rune(0)],
        parameters={"rotation": 3},
    )
    assert rotated.decoded_index_formula == "decoded_index = (28 - cipher_index + 3) mod 29"
    vigenere = dispatch_transform(
        registry=registry,
        transform_id="vigenere_explicit_key",
        tokens=[_rune(1, "U")],
        parameters={"key_text": "U", "direction": "decrypt_subtract"},
    )
    assert vigenere.decoded_normalized_plaintext == "F"
    prime = dispatch_transform(
        registry=registry,
        transform_id="prime_minus_one_stream",
        tokens=[_rune(1, "U")],
        parameters={"prime_start_index": 0, "direction": "forward", "stream_value": "prime_minus_one_mod29"},
    )
    assert prime.decoded_normalized_plaintext == "F"


def test_phi_alias_dispatches_to_prime_minus_one() -> None:
    result = dispatch_transform(
        registry=load_registry(),
        transform_id="phi_prime_stream",
        tokens=[_rune(1, "U")],
        parameters={"prime_start_index": 0, "direction": "forward", "stream_value": "prime_minus_one_mod29"},
    )

    assert result.transform_id == "phi_prime_stream"
    assert result.canonical_transform_id == "prime_minus_one_stream"
    assert result.search_performed is False
    assert result.cuda_used is False
    assert result.scoring_used is False


def test_dispatch_rejects_unknown_missing_params_and_execution_flags() -> None:
    registry = load_registry()

    with pytest.raises(KeyError):
        dispatch_transform(registry=registry, transform_id="unknown", tokens=[_rune(0)], parameters={})
    with pytest.raises(Exception):
        dispatch_transform(
            registry=registry,
            transform_id="rotated_reverse_gematria",
            tokens=[_rune(0)],
            parameters={},
        )
    with pytest.raises(ValueError):
        dispatch_transform(
            registry=registry,
            transform_id="direct_translation",
            tokens=[_rune(0)],
            parameters={"search_enabled": True},
        )
    with pytest.raises(ValueError):
        dispatch_transform(
            registry=registry,
            transform_id="direct_translation",
            tokens=[_rune(0)],
            parameters={"cuda_enabled": True},
        )
