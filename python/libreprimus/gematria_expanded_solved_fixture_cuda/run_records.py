"""Build Stage 5R expanded solved-fixture CUDA run records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.gematria_expanded_solved_fixture_cuda.export import read_record_set, write_record_set, write_report
from libreprimus.gematria_expanded_solved_fixture_cuda.models import (
    COMMON_POLICY_FLAGS,
    EXPECTED_FIXTURE_IDS,
    OUTPUT_DIR,
    RUN_RECORDS_PATH,
    RUN_REPORT,
    STAGE5Q_CANDIDATE_INVENTORY,
    STAGE5Q_NATIVE_PARITY,
    STAGE5Q_TOKEN_MAPPING,
)


def build_run_records(
    *,
    candidate_inventory: Path = STAGE5Q_CANDIDATE_INVENTORY,
    token_mapping: Path = STAGE5Q_TOKEN_MAPPING,
    native_parity: Path = STAGE5Q_NATIVE_PARITY,
    run_records_out: Path = RUN_RECORDS_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    inventory = read_record_set(candidate_inventory)
    mappings = read_record_set(token_mapping)
    native_records = read_record_set(native_parity)
    inventory_by_id = {str(record["candidate_inventory_id"]): record for record in inventory}
    native_by_mapping = {str(record["token_mapping_record_id"]): record for record in native_records}
    mapped = [record for record in mappings if record.get("mapping_status") == "mapped"]
    _validate_exact_scope(mapped=mapped, inventory_by_id=inventory_by_id)
    records = [
        _build_record(
            index=index,
            mapping=mapping,
            inventory_record=inventory_by_id[str(mapping["candidate_inventory_id"])],
            native=native_by_mapping[str(mapping["token_mapping_record_id"])],
        )
        for index, mapping in enumerate(sorted(mapped, key=lambda item: EXPECTED_FIXTURE_IDS.index(str(item["fixture_id"]))))
    ]
    write_record_set(run_records_out, records)
    write_report(out_dir, RUN_REPORT, {"records": records})
    return records


def _validate_exact_scope(*, mapped: list[dict[str, Any]], inventory_by_id: dict[str, dict[str, Any]]) -> None:
    fixture_ids = tuple(sorted(str(record["fixture_id"]) for record in mapped))
    if fixture_ids != tuple(sorted(EXPECTED_FIXTURE_IDS)):
        raise ValueError(f"Stage 5R requires exactly {EXPECTED_FIXTURE_IDS}; got {fixture_ids}")
    for record in mapped:
        inventory = inventory_by_id.get(str(record["candidate_inventory_id"]))
        if inventory is None:
            raise ValueError(f"Missing inventory record for {record['candidate_inventory_id']}")
        if inventory.get("candidate_status") != "candidate_for_mapping":
            raise ValueError(f"Stage 5R cannot use non-mapped candidate: {record['fixture_id']}")
        if inventory.get("already_consumed_by_stage5l_5m_5o") is True:
            raise ValueError(f"Stage 5R cannot use consumed control as a new candidate: {record['fixture_id']}")
        if inventory.get("source_transform_family") != "direct_translation":
            raise ValueError(f"Stage 5R cannot use original-family fixture: {record['fixture_id']}")


def _build_record(
    *,
    index: int,
    mapping: dict[str, Any],
    inventory_record: dict[str, Any],
    native: dict[str, Any],
) -> dict[str, Any]:
    if native.get("native_parity_status") != "prepared":
        raise ValueError(f"Native parity is not prepared for {mapping['fixture_id']}")
    record = {
        "record_type": "gematria_expanded_solved_fixture_cuda_run_record",
        "run_record_id": f"stage5r-expanded-cuda-run-{index:02d}",
        "candidate_inventory_id": mapping["candidate_inventory_id"],
        "token_mapping_record_id": mapping["token_mapping_record_id"],
        "native_parity_record_id": native["native_parity_record_id"],
        "result_store_preflight_source_stage5q": f"stage5q-result-store-preflight-{index:02d}",
        "fixture_id": mapping["fixture_id"],
        "candidate_id": mapping["candidate_id"],
        "source_input_stream_id": mapping["source_input_stream_id"],
        "source_transform_family": mapping["source_transform_family"],
        "candidate_class": inventory_record["candidate_class"],
        "token_values": mapping["token_values"],
        "transformable_mask": mapping["transformable_mask"],
        "token_kinds": mapping["token_kinds"],
        "token_records": mapping["token_records"],
        "token_count": mapping["token_count"],
        "transformable_token_count": mapping["transformable_token_count"],
        "candidate_shifts": native["candidate_shifts"],
        "candidate_ordering": native["candidate_ordering"],
        "expected_native_output_token_hash": native["output_token_hash"],
        "stage5q_native_output_token_hash": native["output_token_hash"],
        "cuda_build_status": "pending",
        "cuda_run_status": "pending",
        "cuda_run_attempted": False,
        "cuda_output_token_hash": None,
        "stage5r_cuda_output_token_hash": None,
        "cuda_native_hash_match": None,
        "cuda_status_codes": [],
        "cuda_output_token_values": [],
        "failure_reason": "",
        "warnings": [],
        "cuda_execution_performed": False,
        "solved_fixture_cuda_used": False,
        "stage5s_ready": False,
    }
    record.update(COMMON_POLICY_FLAGS)
    return record
