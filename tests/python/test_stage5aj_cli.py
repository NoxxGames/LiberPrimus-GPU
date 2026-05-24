from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from PIL import Image
from typer.testing import CliRunner

from libreprimus.source_harvester.cli import app


runner = CliRunner()


def _workbook(path: Path, sheet_name: str) -> None:
    workbook = Workbook()
    workbook.active.title = sheet_name
    workbook.active["A1"] = "ᚠ"
    workbook.save(path)


def test_stage5aj_cli_builds_and_validates_synthetic_pipeline(tmp_path: Path) -> None:
    source_root = tmp_path / "UsefulFilesAndIdeas"
    source_root.mkdir()
    _workbook(source_root / "LP Excel.xlsx", "LP Delimiters")
    _workbook(source_root / "tranlsations_decryptions.xlsx", "Prime Sums")
    (source_root / "important_links.txt").write_text("PAGE 56: https://uncovering-cicada.fandom.com/wiki/PAGE_56\n", encoding="utf-8")
    (source_root / "ideas.txt").write_text("Brown Corpus: https://archive.org/details/BrownCorpus\n", encoding="utf-8")
    Image.new("RGB", (2, 2), "white").save(source_root / "GematrriaPrimus.jpg")

    out = tmp_path / "results"
    bundle_root = tmp_path / "research-inputs" / "stage5aj"
    paths = {name: tmp_path / f"{name}.yaml" for name in ("inventory", "xlsx", "links", "extension", "cards", "content", "scraper", "redaction", "fidelity", "categories", "website", "deep", "readiness", "missing", "guardrail", "decision", "summary")}
    commands = [
        ["inventory-usefulfiles", "--source-root", str(source_root), "--results-dir", str(out), "--out", str(paths["inventory"])],
        ["extract-xlsx-metadata", "--source-root", str(source_root), "--results-dir", str(out), "--out", str(paths["xlsx"])],
        ["parse-important-links", "--source-root", str(source_root), "--existing-manifest", "data/source-harvester/stage5af-cicada-source-manifest.yaml", "--results-dir", str(out), "--out", str(paths["links"]), "--out-manifest-extension", str(paths["extension"])],
        ["build-usefulfiles-source-cards", "--inventory", str(paths["inventory"]), "--xlsx-summary", str(paths["xlsx"]), "--important-links", str(paths["links"]), "--manifest-extension", str(paths["extension"]), "--out-source-card-summary", str(paths["cards"]), "--out-content-index-summary", str(paths["content"]), "--results-dir", str(out)],
        ["build-scraper-capture-policy", "--out", str(paths["scraper"]), "--results-dir", str(out)],
        ["build-redaction-policy", "--out", str(paths["redaction"]), "--results-dir", str(out)],
        ["build-extraction-fidelity-policy", "--out", str(paths["fidelity"]), "--results-dir", str(out)],
        ["build-stage5aj-new-clue-categories", "--out", str(paths["categories"])],
        ["update-deep-research-packs", "--usefulfiles-inventory", str(paths["inventory"]), "--source-card-summary", str(paths["cards"]), "--content-index-summary", str(paths["content"]), "--bundle-root", str(bundle_root), "--results-dir", str(out), "--out-website-update", str(paths["website"]), "--out-deep-research-update", str(paths["deep"]), "--out-readiness", str(paths["readiness"]), "--out-missing-source-plan", str(paths["missing"])],
        ["build-stage5aj-guardrail", "--source-root", str(source_root), "--results-dir", str(out), "--out", str(paths["guardrail"])],
        ["build-stage5aj-next-stage-decision", "--summary-inputs", str(paths["readiness"]), "--summary-inputs", str(paths["missing"]), "--out", str(paths["decision"])],
        ["build-stage5aj-summary", "--inventory", str(paths["inventory"]), "--manifest-extension", str(paths["extension"]), "--source-card-summary", str(paths["cards"]), "--content-index-summary", str(paths["content"]), "--xlsx-summary", str(paths["xlsx"]), "--important-links", str(paths["links"]), "--new-clue-categories", str(paths["categories"]), "--fidelity-policy", str(paths["fidelity"]), "--redaction-policy", str(paths["redaction"]), "--scraper-policy", str(paths["scraper"]), "--website-update", str(paths["website"]), "--deep-research-update", str(paths["deep"]), "--readiness", str(paths["readiness"]), "--missing-source-plan", str(paths["missing"]), "--guardrail", str(paths["guardrail"]), "--next-stage-decision", str(paths["decision"]), "--out", str(paths["summary"]), "--results-dir", str(out)],
    ]
    for command in commands:
        result = runner.invoke(app, command)
        assert result.exit_code == 0, result.output
    validate = runner.invoke(app, ["validate-stage5aj", "--inventory", str(paths["inventory"]), "--manifest-extension", str(paths["extension"]), "--source-card-summary", str(paths["cards"]), "--content-index-summary", str(paths["content"]), "--xlsx-summary", str(paths["xlsx"]), "--important-links", str(paths["links"]), "--new-clue-categories", str(paths["categories"]), "--fidelity-policy", str(paths["fidelity"]), "--redaction-policy", str(paths["redaction"]), "--scraper-policy", str(paths["scraper"]), "--website-update", str(paths["website"]), "--deep-research-update", str(paths["deep"]), "--readiness", str(paths["readiness"]), "--missing-source-plan", str(paths["missing"]), "--guardrail", str(paths["guardrail"]), "--next-stage-decision", str(paths["decision"]), "--summary", str(paths["summary"]), "--results-dir", str(out)])
    assert validate.exit_code == 0, validate.output
    assert "source_harvester_stage5aj_valid=true" in validate.output
