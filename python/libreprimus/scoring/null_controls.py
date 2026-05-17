"""Deterministic null and negative controls for scoring calibration."""

from __future__ import annotations

import random
from pathlib import Path
from typing import Any

import yaml

from libreprimus.paths import repo_root

DEFAULT_NULL_POLICY_PATH = repo_root() / "data/scoring/null-control-policy-v0.yaml"


def load_null_control_policy(path: Path = DEFAULT_NULL_POLICY_PATH) -> dict[str, Any]:
    resolved = path if path.is_absolute() else repo_root() / path
    payload = yaml.safe_load(resolved.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Null-control policy must be a mapping: {resolved}")
    return payload


def generate_null_control_texts(
    *,
    policy: dict[str, Any] | None = None,
    seed_text: str | None = None,
) -> list[dict[str, Any]]:
    payload = policy if policy is not None else load_null_control_policy()
    seed = int(payload.get("random_seed", 3301))
    length = int(payload.get("length", 87))
    random_count = int(payload.get("random_control_count", 200))
    shuffled_count = int(payload.get("shuffled_control_count", 50))
    alphabet = str(payload.get("alphabet", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    rng = random.Random(seed)
    controls: list[dict[str, Any]] = []
    for index in range(random_count):
        text = _random_text(rng, alphabet, length)
        controls.append(
            {
                "control_id": f"null-random-{index:03d}",
                "source": "deterministic_random_gematria_like",
                "text": text,
            }
        )
    base = seed_text or _random_text(rng, alphabet, length)
    base_chars = list(base[:length].ljust(length, "X"))
    for index in range(shuffled_count):
        shuffled = base_chars[:]
        rng.shuffle(shuffled)
        controls.append(
            {
                "control_id": f"null-shuffled-{index:03d}",
                "source": "deterministic_shuffled_stage3_candidate_like",
                "text": "".join(shuffled),
            }
        )
    return controls


def generate_negative_control_texts(length: int = 87) -> list[dict[str, Any]]:
    alphabet = "QXZJVK"
    rng = random.Random(1337)
    return [
        {
            "control_id": "negative-repeated-a",
            "source": "synthetic_repeated_character",
            "text": "A" * length,
        },
        {
            "control_id": "negative-repeated-qx",
            "source": "synthetic_repeated_impossible_bigram",
            "text": ("QX" * ((length // 2) + 1))[:length],
        },
        {
            "control_id": "negative-high-entropy-labels",
            "source": "synthetic_high_entropy_labels",
            "text": "".join(rng.choice(alphabet) for _ in range(length)),
        },
        {
            "control_id": "negative-separatorless-gibberish",
            "source": "synthetic_separatorless_gibberish",
            "text": "".join(rng.choice("BCDFGHJKLMNPQRSTVWXYZ") for _ in range(length)),
        },
    ]


def _random_text(rng: random.Random, alphabet: str, length: int) -> str:
    chars: list[str] = []
    for index in range(length):
        if index and index % 11 == 0:
            chars.append(" ")
        else:
            chars.append(rng.choice(alphabet))
    return "".join(chars)
