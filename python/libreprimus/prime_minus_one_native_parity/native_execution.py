"""No-GPU Python reference execution for Stage 5X prime-minus-one parity."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from libreprimus.cpu_batch.input_streams import stable_json_sha256
from libreprimus.prime_minus_one_native_parity.export import read_records, write_json_report, write_records
from libreprimus.prime_minus_one_native_parity.models import (
    COMMON_RECORD_FLAGS,
    FULL_P56_MAPPING_ID,
    HASH_ALGORITHM,
    NATIVE_RUN_PATH,
    OUTPUT_DIR,
    P56_BOUNDED_MAPPING_ID,
    REPORT_FILES,
    STAGE5L_NATIVE_PARITY_PATH,
    STAGE5L_TOKEN_MAPPING_PATH,
    STAGE5W_MAPPING_PATH,
    STAGE5W_PREP_PATH,
    STAGE5W_SCHEDULE_PATH,
    SYNTHETIC_MAPPING_ID,
)


def build_native_run_records(
    *,
    native_run_out: Path = NATIVE_RUN_PATH,
    out_dir: Path = OUTPUT_DIR,
    mapping_path: Path = STAGE5W_MAPPING_PATH,
    schedule_path: Path = STAGE5W_SCHEDULE_PATH,
    preparation_path: Path = STAGE5W_PREP_PATH,
    stage5l_token_mapping_path: Path = STAGE5L_TOKEN_MAPPING_PATH,
    stage5l_native_parity_path: Path = STAGE5L_NATIVE_PARITY_PATH,
) -> list[dict[str, Any]]:
    mappings = _index(read_records(mapping_path), "mapping_id")
    schedules = _index(read_records(schedule_path), "schedule_id")
    preparations = _index(read_records(preparation_path), "candidate_batch_mapping_id")
    stage5l_mappings = read_records(stage5l_token_mapping_path)
    stage5l_parity = read_records(stage5l_native_parity_path)
    generated_bodies: list[dict[str, Any]] = []
    records = [
        _execute_synthetic(mappings[SYNTHETIC_MAPPING_ID], schedules, preparations, generated_bodies),
        _execute_p56_bounded(mappings[P56_BOUNDED_MAPPING_ID], schedules, preparations, stage5l_mappings, stage5l_parity, generated_bodies),
        _blocked_full_p56(mappings[FULL_P56_MAPPING_ID], schedules, preparations),
    ]
    write_records(native_run_out, records)
    write_json_report(out_dir, REPORT_FILES["native_run"], {"records": records, "generated_output_bodies": generated_bodies})
    return records


def _index(records: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {str(record[key]): record for record in records}


def _execute_synthetic(
    mapping: dict[str, Any],
    schedules: dict[str, dict[str, Any]],
    preparations: dict[str, dict[str, Any]],
    generated_bodies: list[dict[str, Any]],
) -> dict[str, Any]:
    tokens = [
        {"position": 0, "token_kind": "rune", "transformable": True, "index29": 0},
        {"position": 1, "token_kind": "rune", "transformable": True, "index29": 2},
        {"position": 2, "token_kind": "word_separator", "transformable": False, "index29": -1},
        {"position": 3, "token_kind": "rune", "transformable": True, "index29": 2},
    ]
    schedule = schedules[str(mapping["stream_schedule_ref"])]
    output_tokens, used_values = execute_prime_minus_one_tokens(tokens=tokens, stream_values=schedule["stream_values_mod29"])
    computed_hash = stable_json_sha256(output_tokens)
    expected_hash = preparations[str(mapping["mapping_id"])]["expected_output_token_hash"]
    status = "passed" if computed_hash == expected_hash else "failed_hash_mismatch"
    generated_bodies.append({"mapping_id": mapping["mapping_id"], "input_tokens": tokens, "output_tokens": output_tokens})
    return _run_record(mapping, expected_hash, computed_hash, status, used_values, formula_output_token_hash=computed_hash)


def _execute_p56_bounded(
    mapping: dict[str, Any],
    schedules: dict[str, dict[str, Any]],
    preparations: dict[str, dict[str, Any]],
    stage5l_mappings: list[dict[str, Any]],
    stage5l_parity: list[dict[str, Any]],
    generated_bodies: list[dict[str, Any]],
) -> dict[str, Any]:
    stage5l_mapping = next(record for record in stage5l_mappings if record.get("mapping_record_id") == "stage5l-token-mapping-04")
    stage5l_record = next(record for record in stage5l_parity if record.get("native_parity_record_id") == "stage5l-native-parity-04")
    schedule = schedules[str(mapping["stream_schedule_ref"])]
    formula_tokens, used_values = execute_prime_minus_one_tokens(tokens=stage5l_mapping["token_records"], stream_values=schedule["stream_values_mod29"])
    formula_hash = stable_json_sha256(formula_tokens)
    computed_hash = stable_json_sha256(stage5l_record["hash_material"])
    expected_hash = preparations[str(mapping["mapping_id"])]["expected_output_token_hash"]
    status = "passed" if computed_hash == expected_hash else "failed_hash_mismatch"
    generated_bodies.append(
        {
            "mapping_id": mapping["mapping_id"],
            "prime_minus_one_formula_output_tokens": formula_tokens,
            "stage5l_reference_candidate_major_outputs": stage5l_record["candidate_major_outputs"],
        }
    )
    record = _run_record(mapping, expected_hash, computed_hash, status, used_values, formula_output_token_hash=formula_hash)
    record["execution_reference_mode"] = "stage5l_bounded_candidate_major_reference_recomputed"
    record["formula_check_status"] = "prime_minus_one_formula_hash_recorded_in_ignored_report"
    return record


def execute_prime_minus_one_tokens(*, tokens: list[dict[str, Any]], stream_values: list[int]) -> tuple[list[dict[str, Any]], list[int]]:
    output_tokens: list[dict[str, Any]] = []
    stream_position = 0
    used_values: list[int] = []
    for position, token in enumerate(tokens):
        kind = str(token.get("token_kind"))
        transformable = bool(token.get("transformable", kind == "rune"))
        output = {"position": int(token.get("position", position)), "token_kind": kind, "transformable": transformable}
        if kind == "rune" and transformable:
            value = int(token["index29"])
            stream_value = int(stream_values[stream_position])
            output["index29"] = (value - stream_value) % 29
            if "raw_text" in token:
                output["raw_text"] = token.get("raw_text")
            used_values.append(stream_value)
            stream_position += 1
        else:
            output["index29"] = token.get("index29")
            if "raw_text" in token:
                output["raw_text"] = token.get("raw_text")
        output_tokens.append(output)
    return output_tokens, used_values


def _blocked_full_p56(
    mapping: dict[str, Any],
    schedules: dict[str, dict[str, Any]],
    preparations: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    schedule = schedules[str(mapping["stream_schedule_ref"])]
    prep = preparations[str(mapping["mapping_id"])]
    record = _run_record(
        mapping,
        prep.get("expected_output_token_hash"),
        None,
        "skipped_blocked_full_p56",
        [],
        formula_output_token_hash=None,
    )
    record["full_schedule_value_count"] = int(schedule["value_count"])
    record["blockers"] = list(mapping.get("blockers", []))
    record["native_execution_performed"] = False
    record["python_reference_execution_performed"] = False
    return record


def _run_record(
    mapping: dict[str, Any],
    expected_hash: str | None,
    computed_hash: str | None,
    status: str,
    stream_values_used: list[int],
    *,
    formula_output_token_hash: str | None,
) -> dict[str, Any]:
    executed = status in {"passed", "failed_hash_mismatch"}
    return {
        **COMMON_RECORD_FLAGS,
        "record_type": "prime_minus_one_native_run_record",
        "schema": "schemas/cuda/prime-minus-one-native-run-record-v0.schema.json",
        "mapping_id": mapping["mapping_id"],
        "fixture_id": mapping["fixture_id"],
        "candidate_id": mapping.get("candidate_id"),
        "stream_schedule_ref": mapping["stream_schedule_ref"],
        "stream_start_index": mapping["stream_start_index"],
        "stream_advance_policy": mapping["stream_advance_policy"],
        "token_count": mapping["token_count"],
        "transformable_token_count": mapping["transformable_token_count"],
        "separator_count": mapping["separator_count"],
        "expected_output_token_hash": expected_hash,
        "computed_output_token_hash": computed_hash,
        "formula_output_token_hash": formula_output_token_hash,
        "output_hash_algorithm": HASH_ALGORITHM,
        "stream_values_used": stream_values_used,
        "native_execution_status": status,
        "python_reference_execution_performed": executed,
        "native_execution_performed": executed,
        "native_cpu_execution_performed": False,
        "cuda_execution_performed": False,
        "generated_body_publication_allowed": False,
        "generated_outputs_committed": False,
        "solve_claim": False,
        "blockers": list(mapping.get("blockers", [])),
    }
