from pathlib import Path

from typer.testing import CliRunner

from libreprimus.cli import app


def test_stage5az_validate_cli_works_without_generated_outputs(tmp_path: Path) -> None:
    result = CliRunner().invoke(app, ["token-block", "validate-stage5az", "--results-dir", str(tmp_path)])

    assert result.exit_code == 0, result.output
    assert "token_block_stage5az_valid=true" in result.output
    assert "validation_error_count=0" in result.output
    assert "stage5az_generated_summary_present=False" in result.output


def test_stage5az_audit_cli_detects_duplicate(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        app,
        [
            "token-block",
            "audit-stage5az-preflight-manifests",
            "--results-dir",
            str(tmp_path),
            "--out-integrity-audit",
            str(tmp_path / "integrity.yaml"),
            "--out-family-id-audit",
            str(tmp_path / "family.yaml"),
            "--out-reference-audit",
            str(tmp_path / "reference.yaml"),
            "--out-taxonomy-policy",
            str(tmp_path / "taxonomy.yaml"),
        ],
    )

    assert result.exit_code == 0, result.output
    assert "duplicate_family_id_count_before_repair=1" in result.output
    assert "known_duplicate_family_id_found=True" in result.output
