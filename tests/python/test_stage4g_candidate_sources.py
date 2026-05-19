from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from libreprimus.cookie_refresh.candidate_sources import load_source_backed_base_strings
from libreprimus.cookie_refresh.deduplication import expand_and_deduplicate_candidates
from libreprimus.cookie_refresh.manifest_loader import load_cookie_refresh_manifest
from libreprimus.cookie_refresh.models import CandidateBaseString


def test_stage4g_loads_source_backed_cookie_base_strings(tmp_path: Path) -> None:
    candidate_sources = tmp_path / "sources.yaml"
    cookie_targets = tmp_path / "targets.yaml"
    _write(
        candidate_sources,
        {
            "records": [
                {
                    "source_id": "stage4b-cookie-source",
                    "title": "Cookie artefacts 167 and 761",
                    "notes": "source-backed public cookie strings",
                    "solve_claim": False,
                }
            ]
        },
    )
    _write(
        cookie_targets,
        {
            "records": [
                {
                    "record_type": "cookie_hash_record",
                    "cookie_id": "cookie-2013-167-v0",
                    "cookie_name": "167",
                    "cookie_value": "6941f707ff39d259ff71657a79cb6b54c184d2f0455810109c1a960860bde0e6",
                    "preimage_status": "unknown",
                }
            ]
        },
    )
    bases = load_source_backed_base_strings(candidate_sources, cookie_targets)
    assert {base.text for base in bases} >= {"167", "761"}
    assert all(base.source_basis for base in bases)


def test_stage4g_undeclared_variant_rejected(tmp_path: Path) -> None:
    manifest = _manifest(tmp_path, byte_variants=["raw", "invented"])
    with pytest.raises(ValueError, match="byte variants"):
        load_cookie_refresh_manifest(manifest)


def test_stage4g_undeclared_algorithm_rejected(tmp_path: Path) -> None:
    manifest = _manifest(tmp_path, algorithms=["sha256", "ripemd160"])
    with pytest.raises(ValueError, match="algorithms"):
        load_cookie_refresh_manifest(manifest)


def test_stage4g_fuzzy_and_partial_matching_rejected(tmp_path: Path) -> None:
    for key in ("fuzzy_matching", "partial_matching"):
        manifest = _manifest(tmp_path, **{key: True})
        with pytest.raises(ValueError, match=key):
            load_cookie_refresh_manifest(manifest)


def test_stage4g_dedup_and_cap_enforced() -> None:
    bases = [
        CandidateBaseString("base-1", "source-1", "source basis", "167"),
        CandidateBaseString("base-2", "source-2", "source basis", "167"),
    ]
    candidates, duplicates, generated_count = expand_and_deduplicate_candidates(
        bases=bases,
        byte_variants=("raw",),
        cap=1,
        previous_hashes=set(),
    )
    assert generated_count == 2
    assert len(candidates) == 1
    assert len(duplicates) == 1
    over_cap_bases = [
        CandidateBaseString("base-1", "source-1", "source basis", "167"),
        CandidateBaseString("base-2", "source-2", "source basis", "761"),
    ]
    with pytest.raises(ValueError, match="candidate_cap_exceeded"):
        expand_and_deduplicate_candidates(
            bases=over_cap_bases,
            byte_variants=("raw",),
            cap=1,
            previous_hashes=set(),
        )


def _manifest(
    tmp_path: Path,
    *,
    byte_variants: list[str] | None = None,
    algorithms: list[str] | None = None,
    fuzzy_matching: bool = False,
    partial_matching: bool = False,
) -> Path:
    path = tmp_path / f"manifest-{byte_variants}-{algorithms}-{fuzzy_matching}-{partial_matching}.yaml"
    _write(
        path,
        {
            "record_type": "cookie_refresh_manifest",
            "manifest_id": "exp_stage4b_cookie_pack_v2",
            "candidate_count_upper_bound": 384,
            "source_basis": ["synthetic source"],
            "byte_variants": byte_variants or ["raw"],
            "algorithms": algorithms or ["sha256"],
            "exact_match_only": True,
            "fuzzy_matching": fuzzy_matching,
            "partial_matching": partial_matching,
            "broad_search": False,
            "hashcat_used": False,
            "cuda_enabled": False,
            "cloud_execution": False,
            "no_solve_claim": True,
            "canonical_corpus_active": False,
            "page_boundaries_final": False,
            "generated_outputs_committed": False,
        },
    )
    return path


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
