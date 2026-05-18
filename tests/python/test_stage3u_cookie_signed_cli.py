from __future__ import annotations

import hashlib
from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage3u_cli_validate_manifest() -> None:
    result = CliRunner().invoke(
        app,
        [
            "post-discord",
            "validate-cookie-manifest",
            "--manifest",
            "experiments/manifests/post-discord/EXP-3R-001-cookie-sha256-signed-variants-a.yaml",
        ],
    )

    assert result.exit_code == 0
    assert "cookie_manifest_valid=true" in result.output
    assert "algorithm=sha256" in result.output


def test_stage3u_cli_run_with_synthetic_records(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.yaml"
    cookies = tmp_path / "cookies.yaml"
    manifest.write_text(
        """
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
  base_strings: [known]
  byte_variants: [raw]
  fuzzy_matching: false
  gpu_hashcat: false
""".strip()
        + "\n",
        encoding="utf-8",
    )
    cookie_761 = "0" * 64
    cookies.write_text(
        f"""
schema_id: cookie-hash-records-v0
record_count: 2
records:
  - record_type: cookie_hash_record
    cookie_id: cookie-2013-167-v0
    cookie_name: "167"
    cookie_value: "{hashlib.sha256(b"known").hexdigest()}"
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

    result = CliRunner().invoke(
        app,
        [
            "post-discord",
            "run-cookie-signed-variants",
            "--manifest",
            str(manifest),
            "--cookies",
            str(cookies),
            "--out-dir",
            str(tmp_path / "out"),
        ],
    )

    assert result.exit_code == 0
    assert "exact_match_count=1" in result.output
