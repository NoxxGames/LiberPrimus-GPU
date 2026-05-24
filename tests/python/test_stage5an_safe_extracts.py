from __future__ import annotations

import json
from pathlib import Path

from libreprimus.deep_research_export.safe_extracts import generate_safe_extracts
from test_stage5an_content_pack_builder import _write_xlsx


def test_safe_extracts_handle_text_and_xlsx_metadata(tmp_path: Path) -> None:
    source = tmp_path / "safe"
    source.mkdir()
    (source / "important_links.txt").write_text("O:\\secret\\path https://example.org\n", encoding="utf-8")
    _write_xlsx(source / "LP Excel.xlsx")
    out = tmp_path / "extracts"
    selected, findings = generate_safe_extracts([source], out)
    assert len(selected) == 2
    assert (out / "important_links.txt").read_text(encoding="utf-8").startswith("[redacted-local-path]")
    metadata = json.loads((out / "lp-excel-workbook-metadata.json").read_text(encoding="utf-8"))
    assert metadata["raw_workbook_copied"] is False
    assert metadata["sheet_count"] == 1
    assert any(record["reason"] == "local_absolute_path_redacted" for record in findings)
