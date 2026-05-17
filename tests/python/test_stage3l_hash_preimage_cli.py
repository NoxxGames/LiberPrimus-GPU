from __future__ import annotations

from pathlib import Path

import yaml
from typer.testing import CliRunner

from libreprimus.cli import app


def test_hash_preimage_validate_packs_cli() -> None:
    result = CliRunner().invoke(
        app,
        [
            "hash-preimage",
            "validate-packs",
            "--pack-dir",
            "data/observations/web/hash-preimage-candidate-packs",
        ],
    )

    assert result.exit_code == 0, result.output
    assert "candidate_pack_count=2" in result.output


def test_hash_preimage_run_cli_with_synthetic_pack(tmp_path: Path) -> None:
    digest = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
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

    result = CliRunner().invoke(
        app,
        [
            "hash-preimage",
            "run",
            "--cookies",
            str(cookies),
            "--pack-dir",
            str(pack_dir),
            "--out-dir",
            str(tmp_path / "out"),
        ],
    )

    assert result.exit_code == 0, result.output
    assert "exact_match_count=1" in result.output


def test_hash_preimage_summary_cli(tmp_path: Path) -> None:
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    (out_dir / "summary.json").write_text(
        """{
  "record_type": "hash_preimage_run_summary",
  "run_id": "synthetic",
  "generated_at_utc": "2026-05-17T00:00:00Z",
  "algorithm": "sha256",
  "target_cookie_count": 1,
  "target_cookie_ids": ["synthetic-cookie"],
  "pack_count": 1,
  "pack_ids": ["synthetic_pack"],
  "candidate_count_generated_before_dedup": 1,
  "candidate_count": 1,
  "duplicate_candidate_count": 0,
  "comparison_count": 1,
  "exact_match_count": 0,
  "output_paths": {},
  "warnings": [],
  "solve_claim": false,
  "cuda_used": false,
  "trusted_as_canonical": false
}
""",
        encoding="utf-8",
    )

    result = CliRunner().invoke(
        app,
        ["hash-preimage", "summary", "--results-dir", str(out_dir)],
    )

    assert result.exit_code == 0, result.output
    assert "solve_claim=false" in result.output
