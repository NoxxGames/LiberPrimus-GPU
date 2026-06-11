from __future__ import annotations

from test_stage5ea_common import ensure_stage5ea_built, load_yaml


def test_stage5ea_preserves_prior_stage_records_without_rewrite() -> None:
    ensure_stage5ea_built()

    for path in (
        "data/token-block/stage5ea-stage5dz-preservation.yaml",
        "data/token-block/stage5ea-stage5dy-preservation.yaml",
        "data/token-block/stage5ea-stage5dx-preservation.yaml",
        "data/token-block/stage5ea-stage5dw-preservation.yaml",
        "data/token-block/stage5ea-stage5bd-preservation.yaml",
        "data/token-block/stage5ea-active-lineage-preservation.yaml",
    ):
        record = load_yaml(path)
        assert record["preserved"] is True
        assert record["rewritten"] is False
        assert record["superseded_now"] is False
