from __future__ import annotations

from pathlib import Path

from libreprimus.source_harvester.community_claims import build_community_claim_records


def test_stage5ak_claim_records_are_not_execution_ready(tmp_path: Path) -> None:
    result = build_community_claim_records(
        source_root=tmp_path / "community-facts",
        claim_policy_out=tmp_path / "policy.yaml",
        claim_records_out=tmp_path / "claims.yaml",
        correction_log_out=tmp_path / "corrections.yaml",
        clue_categories_out=tmp_path / "categories.yaml",
        results_dir=tmp_path / "results",
    )

    claims = result["claims"]["records"]
    assert result["claims"]["claim_record_count"] == 12
    assert result["claims"]["execution_ready_count"] == 0
    assert result["claims"]["website_publication_allowed_count"] == 0
    assert all(record["execution_ready"] is False for record in claims)
    assert all(record["solve_claim"] is False for record in claims)
    assert all(record["website_publication_allowed"] is False for record in claims)
    assert any(record["requires_null_controls"] is True for record in claims)


def test_stage5ak_correction_log_records_known_arithmetic_correction(tmp_path: Path) -> None:
    result = build_community_claim_records(
        source_root=tmp_path / "community-facts",
        claim_policy_out=tmp_path / "policy.yaml",
        claim_records_out=tmp_path / "claims.yaml",
        correction_log_out=tmp_path / "corrections.yaml",
        clue_categories_out=tmp_path / "categories.yaml",
        results_dir=tmp_path / "results",
    )

    corrections = result["corrections"]["records"]
    assert result["corrections"]["correction_record_count"] == 4
    assert any(record["correction_id"] == "stage5ak-correction-13136-plus-256" for record in corrections)
    assert all(record["execution_ready"] is False for record in corrections)
    assert all(record["solve_claim"] is False for record in corrections)
