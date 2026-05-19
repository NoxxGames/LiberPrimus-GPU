from __future__ import annotations

from pathlib import Path

import yaml
from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage4g_cli_run_and_validate_with_synthetic_records(tmp_path: Path) -> None:
    records = tmp_path / "records"
    manifest = records / "manifest.yaml"
    candidate_sources = records / "sources.yaml"
    targets = records / "targets.yaml"
    out_dir = tmp_path / "out"
    summary = records / "summary.yaml"
    _write_manifest(manifest, cap=8)
    _write_sources(candidate_sources)
    _write_targets(targets)

    result = CliRunner().invoke(
        app,
        [
            "cookie-refresh",
            "run",
            "--manifest",
            str(manifest),
            "--candidate-sources",
            str(candidate_sources),
            "--cookie-targets",
            str(targets),
            "--out-dir",
            str(out_dir),
            "--summary-out",
            str(summary),
            "--allow-warnings",
        ],
    )
    assert result.exit_code == 0, result.output
    assert "source_backed_base_string_count=4" in result.output
    assert "exact_match_count=0" in result.output

    validate = CliRunner().invoke(
        app,
        [
            "cookie-refresh",
            "validate",
            "--results-dir",
            str(out_dir),
            "--summary",
            str(summary),
        ],
    )
    assert validate.exit_code == 0, validate.output
    assert "cookie_refresh_valid=true" in validate.output


def test_stage4g_cli_cap_exceeded_fails(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.yaml"
    candidate_sources = tmp_path / "sources.yaml"
    targets = tmp_path / "targets.yaml"
    _write_manifest(manifest, cap=1)
    _write_sources(candidate_sources)
    _write_targets(targets)
    result = CliRunner().invoke(
        app,
        [
            "cookie-refresh",
            "run",
            "--manifest",
            str(manifest),
            "--candidate-sources",
            str(candidate_sources),
            "--cookie-targets",
            str(targets),
            "--out-dir",
            str(tmp_path / "out"),
            "--summary-out",
            str(tmp_path / "summary.yaml"),
            "--allow-warnings",
        ],
    )
    assert result.exit_code == 1
    assert "candidate_cap_exceeded" in result.output


def _write_manifest(path: Path, *, cap: int) -> None:
    _write(
        path,
        {
            "record_type": "cookie_refresh_manifest",
            "manifest_id": "exp_stage4b_cookie_pack_v2",
            "candidate_count_upper_bound": cap,
            "source_basis": ["synthetic source-backed cookie strings"],
            "byte_variants": ["raw"],
            "algorithms": ["sha256"],
            "exact_match_only": True,
            "fuzzy_matching": False,
            "partial_matching": False,
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


def _write_sources(path: Path) -> None:
    _write(
        path,
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


def _write_targets(path: Path) -> None:
    _write(
        path,
        {
            "records": [
                {
                    "record_type": "cookie_hash_record",
                    "cookie_id": "cookie-2013-167-v0",
                    "cookie_name": "167",
                    "cookie_value": "6941f707ff39d259ff71657a79cb6b54c184d2f0455810109c1a960860bde0e6",
                    "preimage_status": "unknown",
                },
                {
                    "record_type": "cookie_hash_record",
                    "cookie_id": "cookie-2013-761-v0",
                    "cookie_name": "761",
                    "cookie_value": "7bc1e7805ccfa518920f0d94fc4e8f7dbd83287a03b337b89109cd2287befae5",
                    "preimage_status": "unknown",
                },
            ]
        },
    )


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
