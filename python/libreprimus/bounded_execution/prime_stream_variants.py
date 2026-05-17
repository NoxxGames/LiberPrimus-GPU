"""Tiny prime stream variants used by Stage 3H reset/advance ablation."""

from __future__ import annotations

from libreprimus.solved_fixtures.prime_stream import first_n_primes

MODULUS = 29


def prime_minus_one_value(offset: int, state_position: int) -> int:
    return (prime_at(offset, state_position) - 1) % MODULUS


def prime_mod29_value(offset: int, state_position: int) -> int:
    return prime_at(offset, state_position) % MODULUS


def prime_gap_value(offset: int, state_position: int) -> int:
    current = prime_at(offset, state_position)
    following = first_n_primes(offset + state_position + 2)[offset + state_position + 1]
    return (following - current) % MODULUS


def prime_at(offset: int, state_position: int) -> int:
    index = offset + state_position
    if index < 0:
        raise ValueError("Prime stream index must be non-negative.")
    return first_n_primes(index + 1)[index]
