from __future__ import annotations

from pathlib import Path

import yaml

from libreprimus.gematria_expansion_candidate_mapping.candidate_inventory import build_candidate_inventory


def test_stage5q_candidate_inventory_excludes_exact_stage5l_pack(tmp_path: Path) -> None:
    out = tmp_path / "inventory.yaml"
    records = build_candidate_inventory(candidate_inventory_out=out, out_dir=tmp_path / "reports")
    statuses = [record["candidate_status"] for record in records]

    assert statuses.count("already_consumed_control") == 5
    assert statuses.count("candidate_for_mapping") == 3
    assert statuses.count("blocked_requires_separate_kernel_contract") == 2
    assert all(record["cuda_execution_performed"] is False for record in records)
    assert all(record["new_cuda_kernels_added"] == 0 for record in records)

    fixture_ids = {record["fixture_id"] for record in records if record["candidate_status"] == "candidate_for_mapping"}
    assert fixture_ids == {"p57-parable", "some-wisdom", "the-loss-of-divinity"}
    assert yaml.safe_load(out.read_text(encoding="utf-8"))["records"] == records


def test_stage5q_candidate_inventory_blocks_original_transform_families(tmp_path: Path) -> None:
    records = build_candidate_inventory(candidate_inventory_out=tmp_path / "inventory.yaml", out_dir=tmp_path)
    blocked = [record for record in records if record["candidate_status"] == "blocked_requires_separate_kernel_contract"]

    assert {record["source_transform_family"] for record in blocked} == {
        "rotated_reverse_gematria",
        "vigenere_explicit_key",
    }
    assert all(record["requires_cuda_execution"] is False for record in blocked)
    assert all(record["requires_unsolved_page_input"] is False for record in blocked)
