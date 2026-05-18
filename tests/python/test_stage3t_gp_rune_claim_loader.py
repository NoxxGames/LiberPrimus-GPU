from __future__ import annotations

from pathlib import Path

from libreprimus.post_discord.gp_rune_claim_verifier import run_gp_rune_verifier


def test_claim_loader_deduplicates(tmp_path: Path) -> None:
    manifest = _manifest(
        tmp_path,
        """
claims:
  - claim_id: claim-a
    source_basis: synthetic
    claim_type: rune_count_equals
    target_span:
      rune_indices: [0, 1, 2]
    claimed_value: 3
    value_type: integer
  - claim_id: claim-b
    source_basis: synthetic
    claim_type: rune_count_equals
    target_span:
      rune_indices: [0, 1, 2]
    claimed_value: 3
    value_type: integer
"""
    )
    promoted = tmp_path / "promoted.yaml"
    visual = tmp_path / "visual.yaml"
    promoted.write_text("records: []\n", encoding="utf-8")
    visual.write_text("records: []\n", encoding="utf-8")

    summary = run_gp_rune_verifier(
        manifest_path=manifest,
        promoted_observations_path=promoted,
        visual_observations_path=visual,
        out_dir=tmp_path / "out",
    )

    assert summary["claims_loaded"] == 2
    assert summary["claims_deduplicated"] == 1
    assert summary["verified_count"] == 1
    assert summary["duplicate_claim_count"] == 1


def _manifest(tmp_path: Path, extra: str = "") -> Path:
    path = tmp_path / "manifest.yaml"
    path.write_text(
        f"""record_type: post_discord_experiment_manifest
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
{extra}
""",
        encoding="utf-8",
    )
    return path
