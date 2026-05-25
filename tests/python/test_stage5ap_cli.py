from __future__ import annotations

from pathlib import Path

from PIL import Image
from typer.testing import CliRunner

from libreprimus.stego_controls.cli import app as stego_app
from libreprimus.token_block.cli import app as token_app


runner = CliRunner()


def test_stage5ap_cli_builds_and_validates_synthetic_records(tmp_path: Path) -> None:
    image_root = tmp_path / "pages"
    image_root.mkdir()
    for page in ("49", "50", "51"):
        Image.new("RGB", (3, 2), "white").save(image_root / f"{page}.jpg")
    data = tmp_path / "data"
    data.mkdir()
    results = tmp_path / "results"
    paths = {name: data / f"{name}.yaml" for name in ["source", "provenance", "transcription", "coordinates", "alphabet", "mapping", "nulls", "dwh", "toolchain", "matrix", "historical", "guardrail", "research", "decision", "summary"]}
    assert runner.invoke(token_app, ["build-stage5ap-source-lock", "--search-roots", str(image_root), "--results-dir", str(results), "--out-source-lock", str(paths["source"]), "--out-image-provenance", str(paths["provenance"])]).exit_code == 0
    assert runner.invoke(token_app, ["build-stage5ap-transcription", "--out", str(paths["transcription"]), "--coordinates-out", str(paths["coordinates"]), "--results-dir", str(results)]).exit_code == 0
    assert runner.invoke(token_app, ["build-stage5ap-alphabet-registry", "--transcription", str(paths["transcription"]), "--out", str(paths["alphabet"])]).exit_code == 0
    assert runner.invoke(token_app, ["build-stage5ap-mapping-preflight", "--transcription", str(paths["transcription"]), "--alphabet-registry", str(paths["alphabet"]), "--out", str(paths["mapping"]), "--results-dir", str(results)]).exit_code == 0
    assert runner.invoke(token_app, ["build-stage5ap-null-control-plan", "--out", str(paths["nulls"])]).exit_code == 0
    assert runner.invoke(token_app, ["build-stage5ap-dwh-context", "--out", str(paths["dwh"])]).exit_code == 0
    assert runner.invoke(stego_app, ["build-stage5ap-outguess-toolchain-readiness", "--out", str(paths["toolchain"])]).exit_code == 0
    assert runner.invoke(stego_app, ["build-stage5ap-outguess-positive-control-matrix", "--toolchain", str(paths["toolchain"]), "--out", str(paths["matrix"]), "--historical-out", str(paths["historical"]), "--results-dir", str(results)]).exit_code == 0
    assert runner.invoke(stego_app, ["build-stage5ap-outguess-guardrail", "--out", str(paths["guardrail"])]).exit_code == 0
    assert runner.invoke(token_app, [
        "build-stage5ap-summary",
        "--source-lock", str(paths["source"]),
        "--image-provenance", str(paths["provenance"]),
        "--transcription", str(paths["transcription"]),
        "--coordinates", str(paths["coordinates"]),
        "--alphabet-registry", str(paths["alphabet"]),
        "--mapping-preflight", str(paths["mapping"]),
        "--null-control-plan", str(paths["nulls"]),
        "--dwh-context", str(paths["dwh"]),
        "--outguess-toolchain", str(paths["toolchain"]),
        "--outguess-matrix", str(paths["matrix"]),
        "--outguess-historical", str(paths["historical"]),
        "--outguess-guardrail", str(paths["guardrail"]),
        "--research-summary-out", str(paths["research"]),
        "--next-stage-decision-out", str(paths["decision"]),
        "--out", str(paths["summary"]),
        "--results-dir", str(results),
    ]).exit_code == 0
    validate = runner.invoke(token_app, [
        "validate-stage5ap",
        "--source-lock", str(paths["source"]),
        "--image-provenance", str(paths["provenance"]),
        "--transcription", str(paths["transcription"]),
        "--coordinates", str(paths["coordinates"]),
        "--alphabet-registry", str(paths["alphabet"]),
        "--mapping-preflight", str(paths["mapping"]),
        "--null-control-plan", str(paths["nulls"]),
        "--dwh-context", str(paths["dwh"]),
        "--research-summary", str(paths["research"]),
        "--next-stage-decision", str(paths["decision"]),
        "--summary", str(paths["summary"]),
    ])
    assert validate.exit_code == 0, validate.output
    assert "token_block_stage5ap_valid=true" in validate.output
