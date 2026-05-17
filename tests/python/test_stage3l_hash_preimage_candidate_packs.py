from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.hash_preimage.candidate_packs import expand_candidate_pack, load_candidate_packs
from libreprimus.hash_preimage.validation import load_cookie_targets, validate_candidate_packs

REPO = Path(__file__).resolve().parents[2]
PACK_DIR = REPO / "data/observations/web/hash-preimage-candidate-packs"
COOKIES = REPO / "data/observations/web/cookie-hash-records-v0.yaml"


def test_cookie_records_load_and_are_hex64() -> None:
    targets = load_cookie_targets(COOKIES)

    assert len(targets) == 2
    assert all(len(target.cookie_value) == 64 for target in targets)
    assert all(all(ch in "0123456789abcdef" for ch in target.cookie_value) for target in targets)


def test_candidate_packs_validate() -> None:
    count, errors = validate_candidate_packs(PACK_DIR)

    assert count == 2
    assert errors == []


def test_candidate_pack_safety_flags() -> None:
    for pack_path in PACK_DIR.glob("*.yaml"):
        payload = yaml.safe_load(pack_path.read_text(encoding="utf-8"))
        assert payload["algorithm"] == "sha256"
        assert payload["generated_from_external_dictionary"] is False
        assert payload["cuda_enabled"] is False
        assert payload["no_solve_claim"] is True


def test_candidate_pack_counts_are_under_bounds() -> None:
    packs = load_candidate_packs(PACK_DIR)
    expanded = {pack["pack_id"]: expand_candidate_pack(pack) for pack in packs}

    assert expanded["hist_cookie_literal_pack_v1"].total_generated_before_dedup == 288
    assert len(expanded["hist_cookie_literal_pack_v1"].candidates) == 249
    assert expanded["hist_cookie_base29_numeric_pack_v1"].total_generated_before_dedup == 1680
    assert len(expanded["hist_cookie_base29_numeric_pack_v1"].candidates) == 1560
