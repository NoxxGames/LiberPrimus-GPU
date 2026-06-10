from __future__ import annotations

from test_stage5dz_common import ensure_stage5dz_built, run_token_block_cli


def test_stage5dz_cli_summary_and_validators() -> None:
    ensure_stage5dz_built()

    summary = run_token_block_cli("stage5dz-summary")

    assert "triangle_findings_recorded=7" in summary
    assert "page32_findings_recorded=8" in summary
    assert "overlay_count=12" in summary
    assert "recommended_next_stage_id=stage-5ea" in summary
    assert "token_block_stage5dz_valid=true" in run_token_block_cli("validate-stage5dz")
    assert "token_block_stage5dz_triangle_findings_valid=true" in run_token_block_cli(
        "validate-stage5dz-triangle-findings"
    )
    assert "token_block_stage5dz_page32_findings_valid=true" in run_token_block_cli(
        "validate-stage5dz-page32-findings"
    )
    assert "token_block_stage5dz_overlays_valid=true" in run_token_block_cli("validate-stage5dz-overlays")
