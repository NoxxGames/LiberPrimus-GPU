from __future__ import annotations

import json
from pathlib import Path

from tests.python.test_stage3u_cookie_signed_runner import _cookie_records, _manifest

from libreprimus.post_discord.cookie_signed_variant_pack import run_cookie_signed_variant_pack


def test_exact_match_records_only_exact_matches(tmp_path: Path) -> None:
    summary = run_cookie_signed_variant_pack(
        manifest_path=_manifest(tmp_path, base="known"),
        cookies_path=_cookie_records(tmp_path, "known"),
        out_dir=tmp_path / "out",
    )
    matches_path = Path(summary["output_paths"]["exact_matches"])
    records = [json.loads(line) for line in matches_path.read_text(encoding="utf-8").splitlines()]

    assert len(records) == 1
    assert records[0]["exact_match"] is True
    assert records[0]["solve_claim"] is False
    assert records[0]["cuda_used"] is False
