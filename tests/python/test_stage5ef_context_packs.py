from __future__ import annotations

from pathlib import Path

from libreprimus.token_block import stage5ef
from test_stage5ef_common import ensure_stage5ef_built, load_yaml


def test_stage5ef_context_packs_are_deterministic_templates() -> None:
    ensure_stage5ef_built()

    result = stage5ef.validate_stage5ef_context_packs()
    registry = load_yaml("data/project-state/stage5ef-context-pack-registry.yaml")

    assert result.validation_error_count == 0
    assert registry["context_pack_template_count"] == 6
    for pack in registry["context_packs"]:
        text = Path(pack["path"]).read_text(encoding="utf-8")
        assert "generated_at:" not in text
        assert "timestamp:" not in text
        assert "O:\\" not in text
        assert "stage-5ef" in text
        assert "stage-5eg" in text
