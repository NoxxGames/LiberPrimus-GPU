from __future__ import annotations

from libreprimus.token_block.stage5ec import validate_stage5ec_source_browser_loadability
from test_stage5ec_common import ensure_stage5ec_built, load_yaml


def test_stage5ec_source_browser_loadability_has_zero_errors() -> None:
    ensure_stage5ec_built()
    result = validate_stage5ec_source_browser_loadability()
    summary = load_yaml("data/project-state/stage5ec-source-browser-loadability-summary.yaml")

    assert result.validation_error_count == 0
    assert summary["source_browser_validation_error_count"] == 0
    assert summary["spurious_root_image_paths_after"] == 0
    assert summary["spurious_root_document_paths_after"] == 0
    assert summary["duplicate_present_missing_path_pairs_after"] == 0
