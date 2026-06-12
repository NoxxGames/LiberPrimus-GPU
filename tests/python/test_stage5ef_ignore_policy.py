from __future__ import annotations

import subprocess

from test_stage5ef_common import ensure_stage5ef_built, load_yaml


def test_stage5ef_raw_and_codex_outputs_remain_uncommitted() -> None:
    ensure_stage5ef_built()

    proof = load_yaml("data/source-harvester/stage5ef-raw-source-noncommit-proof.yaml")
    ignored = subprocess.run(
        ["git", "check-ignore", "-q", "codex-output/stage5ef-codex-completion.md"],
        check=False,
    )

    assert proof["raw_source_files_committed"] is False
    assert proof["raw_third_party_files_committed"] is False
    assert proof["generated_outputs_committed"] is False
    assert proof["codex_output_committed"] is False
    assert ignored.returncode == 0
