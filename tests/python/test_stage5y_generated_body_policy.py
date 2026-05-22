from __future__ import annotations

from pathlib import Path

from libreprimus.prime_minus_one_native_reporting.generated_body_policy import build_generated_body_policy


def test_stage5y_generated_body_policy_blocks_publication(tmp_path: Path) -> None:
    records = build_generated_body_policy(generated_body_policy_out=tmp_path / "policy.yaml", out_dir=tmp_path)
    assert len(records) == 7
    assert all(record["generated_body_publication_allowed"] is False for record in records)
    assert all(record["generated_outputs_committed"] is False for record in records)
    assert all(record["codex_output_committed"] is False for record in records)
    assert any(record["policy_subject"] == "future_generated_body_publication" for record in records)
