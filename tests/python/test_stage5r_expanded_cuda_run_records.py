from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from libreprimus.gematria_expanded_solved_fixture_cuda.run_records import build_run_records


def _records(path: str) -> list[dict[str, object]]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))["records"]


def _write(path: Path, records: list[dict[str, object]]) -> None:
    path.write_text(yaml.safe_dump({"records": records}, sort_keys=False), encoding="utf-8")


def test_stage5r_builds_exact_three_stage5q_mapped_candidates(tmp_path: Path) -> None:
    out = tmp_path / "run.yaml"
    records = build_run_records(run_records_out=out, out_dir=tmp_path / "reports")

    assert len(records) == 3
    assert {record["fixture_id"] for record in records} == {"p57-parable", "some-wisdom", "the-loss-of-divinity"}
    assert all(record["source_transform_family"] == "direct_translation" for record in records)
    assert all(record["cuda_run_status"] == "pending" for record in records)
    assert all(record["cuda_run_attempted"] is False for record in records)
    assert all(record["consumed_controls_excluded"] is True for record in records)
    assert all(record["blocked_original_family_fixtures_excluded"] is True for record in records)
    assert yaml.safe_load(out.read_text(encoding="utf-8"))["records"] == records


def test_stage5r_rejects_consumed_controls_as_new_inputs(tmp_path: Path) -> None:
    inventory = _records("data/cuda/stage5q-gematria-expansion-candidate-inventory.yaml")
    mapping = _records("data/cuda/stage5q-gematria-expansion-token-mapping.yaml")
    consumed = next(record for record in inventory if record["candidate_status"] == "already_consumed_control")
    mutated_mapping = []
    for record in mapping:
        item = dict(record)
        if item.get("mapping_status") == "mapped" and item["fixture_id"] == "p57-parable":
            item["candidate_inventory_id"] = consumed["candidate_inventory_id"]
        mutated_mapping.append(item)
    inventory_path = tmp_path / "inventory.yaml"
    mapping_path = tmp_path / "mapping.yaml"
    _write(inventory_path, inventory)
    _write(mapping_path, mutated_mapping)

    with pytest.raises(ValueError):
        build_run_records(candidate_inventory=inventory_path, token_mapping=mapping_path, run_records_out=tmp_path / "run.yaml", out_dir=tmp_path)


def test_stage5r_rejects_blocked_original_family_fixtures(tmp_path: Path) -> None:
    inventory = _records("data/cuda/stage5q-gematria-expansion-candidate-inventory.yaml")
    mapping = _records("data/cuda/stage5q-gematria-expansion-token-mapping.yaml")
    mutated_inventory = []
    for record in inventory:
        item = dict(record)
        if item["candidate_status"] == "candidate_for_mapping" and item["fixture_id"] == "some-wisdom":
            item["source_transform_family"] = "vigenere_explicit_key"
        mutated_inventory.append(item)
    inventory_path = tmp_path / "inventory.yaml"
    mapping_path = tmp_path / "mapping.yaml"
    _write(inventory_path, mutated_inventory)
    _write(mapping_path, mapping)

    with pytest.raises(ValueError):
        build_run_records(candidate_inventory=inventory_path, token_mapping=mapping_path, run_records_out=tmp_path / "run.yaml", out_dir=tmp_path)
