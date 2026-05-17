from __future__ import annotations

import hashlib
from pathlib import Path

import yaml

from libreprimus.hash_preimage.runner import run_hash_preimage, sha256_hex


def test_sha256_known_vector() -> None:
    assert sha256_hex(b"abc") == hashlib.sha256(b"abc").hexdigest()
    assert sha256_hex(b"abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_exact_match_detection_with_synthetic_cookie(tmp_path: Path) -> None:
    digest = hashlib.sha256(b"abc").hexdigest()
    cookies = tmp_path / "cookies.yaml"
    cookies.write_text(
        yaml.safe_dump(
            {
                "records": [
                    {
                        "record_type": "cookie_hash_record",
                        "cookie_id": "synthetic-cookie",
                        "cookie_name": "synthetic",
                        "cookie_value": digest,
                        "value_format": "hex64",
                        "candidate_hash_type": "unknown_256bit_hex",
                        "trusted_as_canonical": False,
                        "preimage_status": "unknown",
                    }
                ]
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    pack_dir = tmp_path / "packs"
    pack_dir.mkdir()
    (pack_dir / "pack.yaml").write_text(
        yaml.safe_dump(
            {
                "record_type": "hash_preimage_candidate_pack",
                "pack_id": "synthetic_literal_pack_v1",
                "description": "synthetic",
                "algorithm": "sha256",
                "source_class": "archived_claim",
                "candidate_groups": {"synthetic": ["abc", "ab"]},
                "byte_variants": ["raw"],
                "candidate_count_upper_bound": 10,
                "generated_from_external_dictionary": False,
                "cuda_enabled": False,
                "cloud_execution": False,
                "no_solve_claim": True,
                "trusted_as_canonical": False,
                "notes": "test",
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    summary = run_hash_preimage(cookies=cookies, pack_dir=pack_dir, out_dir=tmp_path / "out")

    assert summary["exact_match_count"] == 1
    assert summary["comparison_count"] == 2
    assert summary["solve_claim"] is False


def test_no_partial_matching(tmp_path: Path) -> None:
    full_digest = hashlib.sha256(b"abc").hexdigest()
    different_digest = full_digest[:-1] + ("0" if full_digest[-1] != "0" else "1")
    cookies = tmp_path / "cookies.yaml"
    cookies.write_text(
        yaml.safe_dump(
            {
                "records": [
                    {
                        "record_type": "cookie_hash_record",
                        "cookie_id": "synthetic-cookie",
                        "cookie_name": "synthetic",
                        "cookie_value": different_digest,
                        "value_format": "hex64",
                        "candidate_hash_type": "unknown_256bit_hex",
                        "trusted_as_canonical": False,
                        "preimage_status": "unknown",
                    }
                ]
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    pack_dir = tmp_path / "packs"
    pack_dir.mkdir()
    (pack_dir / "pack.yaml").write_text(
        yaml.safe_dump(
            {
                "record_type": "hash_preimage_candidate_pack",
                "pack_id": "synthetic_literal_pack_v1",
                "description": "synthetic",
                "algorithm": "sha256",
                "source_class": "archived_claim",
                "candidate_groups": {"synthetic": ["abc"]},
                "byte_variants": ["raw"],
                "candidate_count_upper_bound": 10,
                "generated_from_external_dictionary": False,
                "cuda_enabled": False,
                "cloud_execution": False,
                "no_solve_claim": True,
                "trusted_as_canonical": False,
                "notes": "test",
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    summary = run_hash_preimage(cookies=cookies, pack_dir=pack_dir, out_dir=tmp_path / "out")

    assert summary["exact_match_count"] == 0
