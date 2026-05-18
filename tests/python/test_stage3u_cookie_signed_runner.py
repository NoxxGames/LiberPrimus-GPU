from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from libreprimus.post_discord.cookie_signed_variant_pack import (
    CookieManifest,
    apply_byte_variant,
    expand_candidates,
    run_cookie_signed_variant_pack,
    validate_results,
)


def test_byte_variants_are_deterministic() -> None:
    assert apply_byte_variant("A b", "raw") == "A b"
    assert apply_byte_variant("A b", "lower") == "a b"
    assert apply_byte_variant("A b", "upper") == "A B"
    assert apply_byte_variant("A b", "trailing_lf") == "A b\n"
    assert apply_byte_variant("A b", "trailing_crlf") == "A b\r\n"
    assert apply_byte_variant("A b", "leading_space") == " A b"
    assert apply_byte_variant("A b", "trailing_space") == "A b "
    assert apply_byte_variant("A b", "wrapped_space") == " A b "
    assert apply_byte_variant("A b", "compact_no_spaces") == "Ab"
    assert apply_byte_variant("A b", "compact_upper") == "AB"
    assert apply_byte_variant("A b", "compact_lower") == "ab"
    assert apply_byte_variant("A b", "quoted") == '"A b"'


def test_candidate_dedup_counts_duplicates() -> None:
    manifest = CookieManifest(
        experiment_id="EXP-3R-001",
        candidate_cap=10,
        algorithm="sha256",
        base_strings=("ABC",),
        byte_variants=("raw", "upper"),
        payload={"source_basis": ["synthetic"]},
    )

    candidates, duplicate_count = expand_candidates(manifest)

    assert len(candidates) == 1
    assert duplicate_count == 1


def test_candidate_cap_exceeded_fails(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.yaml"
    cookies = _cookie_records(tmp_path, "missing")
    manifest.write_text(
        """
record_type: post_discord_experiment_manifest
experiment_id: EXP-3R-001
candidate_count_cap: 1
execution_enabled: false
cpu_only: true
cuda_enabled: false
cloud_execution: false
paid_services: false
generated_outputs_committed: false
no_solve_claim: true
canonical_corpus_active: false
page_boundaries_final: false
source_basis: [synthetic]
candidate_generation:
  algorithm: sha256
  base_strings: [one, two]
  byte_variants: [raw]
  fuzzy_matching: false
  gpu_hashcat: false
""".strip()
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="candidate_cap_exceeded"):
        run_cookie_signed_variant_pack(manifest_path=manifest, cookies_path=cookies, out_dir=tmp_path / "out")


def test_exact_match_and_summary_schema(tmp_path: Path) -> None:
    manifest = _manifest(tmp_path, base="known")
    cookies = _cookie_records(tmp_path, "known")

    summary = run_cookie_signed_variant_pack(manifest_path=manifest, cookies_path=cookies, out_dir=tmp_path / "out")
    validation_summary, errors = validate_results(tmp_path / "out")

    assert errors == []
    assert validation_summary["exact_match_count"] == 1
    assert summary["exact_match_count"] == 1
    assert summary["comparison_count"] == 2
    assert summary["no_solve_claim"] is True


def test_no_partial_or_fuzzy_matching(tmp_path: Path) -> None:
    manifest = _manifest(tmp_path, base="known")
    digest = hashlib.sha256(b"known").hexdigest()
    partial = digest[:-1] + ("0" if digest[-1] != "0" else "1")
    cookies = _cookie_records_with_value(tmp_path, partial)

    summary = run_cookie_signed_variant_pack(manifest_path=manifest, cookies_path=cookies, out_dir=tmp_path / "out")

    assert summary["exact_match_count"] == 0
    assert summary["fuzzy_matching"] is False
    assert summary["partial_matching"] is False


def _manifest(tmp_path: Path, *, base: str) -> Path:
    path = tmp_path / "manifest.yaml"
    path.write_text(
        f"""
record_type: post_discord_experiment_manifest
experiment_id: EXP-3R-001
candidate_count_cap: 10
execution_enabled: false
cpu_only: true
cuda_enabled: false
cloud_execution: false
paid_services: false
generated_outputs_committed: false
no_solve_claim: true
canonical_corpus_active: false
page_boundaries_final: false
source_basis: [synthetic]
candidate_generation:
  algorithm: sha256
  base_strings: [{base}]
  byte_variants: [raw]
  fuzzy_matching: false
  gpu_hashcat: false
""".strip()
        + "\n",
        encoding="utf-8",
    )
    return path


def _cookie_records(tmp_path: Path, preimage: str) -> Path:
    return _cookie_records_with_value(tmp_path, hashlib.sha256(preimage.encode("utf-8")).hexdigest())


def _cookie_records_with_value(tmp_path: Path, cookie_167: str) -> Path:
    path = tmp_path / "cookies.yaml"
    cookie_761 = "0" * 64
    path.write_text(
        f"""
schema_id: cookie-hash-records-v0
record_count: 2
records:
  - record_type: cookie_hash_record
    cookie_id: cookie-2013-167-v0
    cookie_name: "167"
    cookie_value: "{cookie_167}"
    preimage_status: unknown
  - record_type: cookie_hash_record
    cookie_id: cookie-2013-761-v0
    cookie_name: "761"
    cookie_value: "{cookie_761}"
    preimage_status: unknown
""".strip()
        + "\n",
        encoding="utf-8",
    )
    return path
