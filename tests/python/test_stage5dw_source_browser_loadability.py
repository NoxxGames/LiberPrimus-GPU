from __future__ import annotations

from libreprimus.token_block.stage5dw import validate_stage5dw_source_browser_loadability
from test_stage5dw_common import ensure_stage5dw_built, load_yaml


def test_stage5dw_source_browser_loadability_and_path_invariants() -> None:
    ensure_stage5dw_built()
    result = validate_stage5dw_source_browser_loadability()
    payload = load_yaml("data/project-state/stage5dw-source-browser-loadability-summary.yaml")

    assert result.validation_error_count == 0
    assert payload["source_browser_validation_error_count"] == 0
    assert payload["spurious_root_image_paths_after"] == 0
    assert payload["spurious_root_document_paths_after"] == 0
    assert payload["duplicate_present_missing_path_pairs_after"] == 0
