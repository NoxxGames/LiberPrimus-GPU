from __future__ import annotations

from pathlib import Path

from libreprimus.token_block.stage5dz import SOURCE_HARVESTER_PATHS
from test_stage5dz_common import ensure_stage5dz_built, load_yaml


def test_stage5dz_handoff_uses_codex_output_and_not_codex_output() -> None:
    ensure_stage5dz_built()

    handoff = load_yaml(SOURCE_HARVESTER_PATHS["codex_handoff_policy"])
    noncommit = load_yaml(SOURCE_HARVESTER_PATHS["raw_source_noncommit_proof"])

    assert handoff["canonical_codex_handoff_root"] == "codex-output"
    assert handoff["codex_output_used"] is False
    assert not Path("codex_output").exists()
    assert noncommit["raw_source_files_committed"] is False
    assert noncommit["generated_outputs_committed"] is False
