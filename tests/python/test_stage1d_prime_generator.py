from libreprimus.solved_fixtures.prime_stream import (
    first_n_primes,
    phi_prime_stream,
    phi_prime_value,
    prime_minus_one_stream,
)


def test_first_twenty_primes_match_reference_sequence() -> None:
    assert first_n_primes(20) == [
        2,
        3,
        5,
        7,
        11,
        13,
        17,
        19,
        23,
        29,
        31,
        37,
        41,
        43,
        47,
        53,
        59,
        61,
        67,
        71,
    ]


def test_phi_prime_is_prime_minus_one_for_prime_inputs() -> None:
    for prime in first_n_primes(20):
        assert phi_prime_value(prime) == prime - 1


def test_prime_minus_one_and_phi_prime_streams_are_equivalent() -> None:
    assert prime_minus_one_stream(100) == phi_prime_stream(100)


def test_first_twenty_stream_values_mod29_match_stage1d_reference() -> None:
    assert [value % 29 for value in prime_minus_one_stream(20)] == [
        1,
        2,
        4,
        6,
        10,
        12,
        16,
        18,
        22,
        28,
        1,
        7,
        11,
        13,
        17,
        23,
        0,
        2,
        8,
        12,
    ]
