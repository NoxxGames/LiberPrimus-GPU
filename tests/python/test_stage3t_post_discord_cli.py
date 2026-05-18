from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage3t_cli_validate_and_run(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.yaml"
    promoted = tmp_path / "promoted.yaml"
    visual = tmp_path / "visual.yaml"
    out_dir = tmp_path / "out"
    manifest.write_text(
        """record_type: post_discord_experiment_manifest
experiment_id: EXP-3R-004
description: synthetic
hypothesis: synthetic
candidate_count_cap: 64
execution_enabled: false
cpu_only: true
cuda_enabled: false
cloud_execution: false
paid_services: false
generated_outputs_committed: false
no_solve_claim: true
canonical_corpus_active: false
page_boundaries_final: false
claims:
  - claim_id: synthetic-gp
    source_basis: synthetic
    claim_type: gp_sum_equals
    target_span:
      rune_indices: [0, 1, 2]
    claimed_value: 10
    value_type: integer
""",
        encoding="utf-8",
    )
    promoted.write_text("records: []\n", encoding="utf-8")
    visual.write_text("records: []\n", encoding="utf-8")

    runner = CliRunner()
    result = runner.invoke(
        app,
        ["post-discord", "validate-gp-rune-manifest", "--manifest", str(manifest)],
    )
    assert result.exit_code == 0, result.output
    assert "claim_cap=64" in result.output

    result = runner.invoke(
        app,
        [
            "post-discord",
            "run-gp-rune-verifier",
            "--manifest",
            str(manifest),
            "--promoted-observations",
            str(promoted),
            "--visual-observations",
            str(visual),
            "--out-dir",
            str(out_dir),
        ],
    )
    assert result.exit_code == 0, result.output
    assert "verified_count=1" in result.output
    assert (out_dir / "gp_rune_claim_verification_records.jsonl").is_file()

    result = runner.invoke(app, ["post-discord", "gp-rune-summary", "--results-dir", str(out_dir)])
    assert result.exit_code == 0, result.output
    assert "experiment_id=EXP-3R-004" in result.output
