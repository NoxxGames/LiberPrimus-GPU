from typer.testing import CliRunner

from libreprimus.cli import app


def _write_synthetic_spreadsheet(path) -> None:
    from openpyxl import Workbook

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Sheet1"
    sheet["A203"] = 200
    sheet["B203"] = "0l"
    sheet["C203"] = "lower"
    sheet["D203"] = "0l-lower"
    workbook.save(path)
    workbook.close()


def test_stage5bn_cli_validate_and_summary_work() -> None:
    runner = CliRunner()

    validate_result = runner.invoke(app, ["token-block", "validate-stage5bn"])
    assert validate_result.exit_code == 0, validate_result.output
    assert "token_block_stage5bn_valid=true" in validate_result.output
    assert "spreadsheet_supports_0l=true" in validate_result.output

    summary_result = runner.invoke(app, ["token-block", "show-stage5bn-summary"])
    assert summary_result.exit_code == 0, summary_result.output
    assert "unsupported_position_closure_status=closed_spreadsheet_support_found" in summary_result.output


def test_stage5bn_cli_build_is_deterministic(tmp_path) -> None:
    spreadsheet = tmp_path / "stage5bn-synthetic.xlsx"
    results_dir = tmp_path / "results"
    review_pack = tmp_path / "review-pack"
    output_dir = tmp_path / "records"
    _write_synthetic_spreadsheet(spreadsheet)

    result = CliRunner().invoke(
        app,
        [
            "token-block",
            "build-stage5bn-unsupported-position-review",
            "--local-spreadsheet",
            str(spreadsheet),
            "--human-review-pack-root",
            str(review_pack),
            "--results-dir",
            str(results_dir),
            "--out-target",
            str(output_dir / "target.yaml"),
            "--out-option-gap-audit",
            str(output_dir / "option-gap.yaml"),
            "--out-spreadsheet-audit",
            str(output_dir / "spreadsheet.yaml"),
            "--out-coordinate-context",
            str(output_dir / "coordinate.yaml"),
            "--out-source-evidence",
            str(output_dir / "source-evidence.yaml"),
            "--out-human-review-pack-manifest",
            str(output_dir / "review-pack.yaml"),
            "--out-proposed-addendum",
            str(output_dir / "addendum.yaml"),
            "--out-gap-closure",
            str(output_dir / "gap-closure.yaml"),
            "--out-planning-constraint-update",
            str(output_dir / "planning.yaml"),
            "--out-lineage",
            str(output_dir / "lineage.yaml"),
        ],
    )

    assert result.exit_code == 0, result.output
    assert "target_token_index_0_based=199" in result.output
    assert "stage5aw_supports_0l=false" in result.output
    assert "spreadsheet_supports_0l=true" in result.output
