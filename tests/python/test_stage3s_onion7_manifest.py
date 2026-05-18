from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.post_discord.onion7_seed_pack import load_onion7_manifest

REPO = Path(__file__).resolve().parents[2]
MANIFEST = REPO / "experiments/manifests/post-discord/EXP-3R-003-onion7-raw-prime-order-seed-pack-a.yaml"


def test_stage3s_manifest_validates_and_stays_bounded() -> None:
    manifest = load_onion7_manifest(MANIFEST)

    assert manifest.experiment_id == "EXP-3R-003"
    assert manifest.candidate_count_cap <= 144
    assert manifest.expected_candidate_count == 72
    assert manifest.payload["execution_enabled"] is False
    assert manifest.payload["cuda_enabled"] is False
    assert manifest.payload["no_solve_claim"] is True


def test_stage3s_default_tables_are_4x4(tmp_path: Path) -> None:
    payload = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    copied = tmp_path / "manifest.yaml"
    copied.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    manifest = load_onion7_manifest(copied)

    assert set(manifest.tables) == {"raw_table", "prime_delta_table", "prime_order_table"}
    for table in manifest.tables.values():
        assert len(table) == 4
    assert all(len(row) == 4 for row in table)
    assert manifest.tables["raw_table"][0] == [3258, 3222, 3152, 3038]
    assert manifest.tables["prime_delta_table"][0] == [43, 79, 149, 263]
