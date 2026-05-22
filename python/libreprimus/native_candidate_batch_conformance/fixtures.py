"""Stage 5V conformance fixtures and Python reference adapter."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from libreprimus.native_candidate_batch_conformance.export import write_record_set, write_report
from libreprimus.native_candidate_batch_conformance.models import COMMON_FLAGS, CONFORMANCE_FIXTURES_PATH, OUTPUT_DIR, REPORT_FILES


def canonical_hash(payload: Any) -> str:
    """Return a deterministic SHA-256 hash for a JSON-compatible payload."""

    data = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def apply_shift_mod29(tokens: list[int], mask: list[bool], shift: int) -> list[int]:
    """Apply the only Stage 5U fully defined transform to transformable tokens."""

    output: list[int] = []
    for token, transformable in zip(tokens, mask, strict=True):
        if transformable:
            output.append((token + shift) % 29)
        else:
            output.append(token)
    return output


def candidate_major_shift_outputs(record: dict[str, Any]) -> list[dict[str, Any]]:
    outputs: list[dict[str, Any]] = []
    for candidate in record.get("candidates", []):
        shift = int(candidate["shift_value"])
        output_tokens = apply_shift_mod29(
            list(record["token_values"]),
            list(record["transformable_mask"]),
            shift,
        )
        outputs.append(
            {
                "candidate_id": candidate["candidate_id"],
                "transform_family": "shift_mod29",
                "output_ordering": "candidate_major_then_token_position",
                "output_token_values": output_tokens,
                "output_token_hash": canonical_hash(output_tokens),
            }
        )
    return outputs


def fixture_definitions() -> list[dict[str, Any]]:
    """Return raw-data-free Stage 5V fixtures."""

    records: list[dict[str, Any]] = []
    single = {
        **COMMON_FLAGS,
        "record_type": "candidate_batch_conformance_fixture_record",
        "schema": "schemas/cuda/candidate-batch-conformance-fixture-record-v0.schema.json",
        "fixture_id": "stage5v-shift-single-fixture",
        "fixture_kind": "shift_mod29_execution",
        "source_contract_ids": ["stage5u-shift-mod29-transform-parameter-contract-v0"],
        "token_values": [0, 1, -1, 28],
        "token_kind": ["rune", "rune", "separator", "rune"],
        "transformable_mask": [True, True, False, True],
        "separator_positions": [2],
        "fixture_offsets": [0],
        "fixture_lengths": [4],
        "candidate_ordering": "candidate_major",
        "output_ordering": "candidate_major_then_token_position",
        "candidates": [{"candidate_id": "stage5v-shift-03", "shift_value": 3}],
        "execution_status": "executed_python_reference",
        "shape_only": False,
        "raw_data_free": True,
        "no_gpu_safe": True,
        "generated_body_publication_allowed": False,
    }
    single_outputs = candidate_major_shift_outputs(single)
    single["expected_outputs"] = single_outputs
    single["expected_output_token_hash"] = canonical_hash(single_outputs)
    records.append(single)

    multi = {
        **COMMON_FLAGS,
        "record_type": "candidate_batch_conformance_fixture_record",
        "schema": "schemas/cuda/candidate-batch-conformance-fixture-record-v0.schema.json",
        "fixture_id": "stage5v-shift-multi-candidate-fixture",
        "fixture_kind": "candidate_major_shift_mod29_execution",
        "source_contract_ids": ["stage5u-candidate-ordering-contract-v0"],
        "token_values": [2, 5, -1, 8],
        "token_kind": ["rune", "rune", "separator", "rune"],
        "transformable_mask": [True, True, False, True],
        "separator_positions": [2],
        "fixture_offsets": [0],
        "fixture_lengths": [4],
        "candidate_ordering": "candidate_major",
        "output_ordering": "candidate_major_then_token_position",
        "candidates": [
            {"candidate_id": "stage5v-shift-00", "shift_value": 0},
            {"candidate_id": "stage5v-shift-01", "shift_value": 1},
            {"candidate_id": "stage5v-shift-03", "shift_value": 3},
            {"candidate_id": "stage5v-shift-13", "shift_value": 13},
            {"candidate_id": "stage5v-shift-28", "shift_value": 28},
        ],
        "execution_status": "executed_python_reference",
        "shape_only": False,
        "raw_data_free": True,
        "no_gpu_safe": True,
        "generated_body_publication_allowed": False,
    }
    multi_outputs = candidate_major_shift_outputs(multi)
    multi["expected_outputs"] = multi_outputs
    multi["expected_output_token_hash"] = canonical_hash(multi_outputs)
    records.append(multi)

    variable = {
        **COMMON_FLAGS,
        "record_type": "candidate_batch_conformance_fixture_record",
        "schema": "schemas/cuda/candidate-batch-conformance-fixture-record-v0.schema.json",
        "fixture_id": "stage5v-variable-length-fixture-pack",
        "fixture_kind": "variable_length_shift_mod29_execution",
        "source_contract_ids": ["stage5u-variable-length-token-buffer-contract-v0"],
        "token_values": [4, -1, 7, 10, 11, -1, 12, 0],
        "token_kind": ["rune", "separator", "rune", "rune", "rune", "separator", "rune", "rune"],
        "transformable_mask": [True, False, True, True, True, False, True, True],
        "separator_positions": [1, 5],
        "fixture_offsets": [0, 3, 6],
        "fixture_lengths": [3, 3, 2],
        "candidate_ordering": "candidate_major",
        "output_ordering": "candidate_major_then_token_position",
        "candidates": [{"candidate_id": "stage5v-shift-01", "shift_value": 1}],
        "execution_status": "executed_python_reference",
        "shape_only": False,
        "raw_data_free": True,
        "no_gpu_safe": True,
        "generated_body_publication_allowed": False,
    }
    variable_outputs = candidate_major_shift_outputs(variable)
    variable["expected_outputs"] = variable_outputs
    variable["expected_output_token_hash"] = canonical_hash(variable_outputs)
    records.append(variable)

    records.extend(
        [
            {
                **COMMON_FLAGS,
                "record_type": "candidate_batch_conformance_fixture_record",
                "schema": "schemas/cuda/candidate-batch-conformance-fixture-record-v0.schema.json",
                "fixture_id": "stage5v-key-schedule-shape-fixture",
                "fixture_kind": "key_schedule_shape_only",
                "source_contract_ids": ["stage5u-vigenere-key-schedule-contract-v0"],
                "token_values": [0, 1, 2],
                "token_kind": ["rune", "rune", "rune"],
                "transformable_mask": [True, True, True],
                "separator_positions": [],
                "fixture_offsets": [0],
                "fixture_lengths": [3],
                "key_schedule_tokens": [1, 2, 3, 5, 8],
                "key_reset_policy": "explicit_reset_points_required_before_execution",
                "key_advance_policy": "skip_separators_shape_declared",
                "candidate_ordering": "candidate_major",
                "output_ordering": "candidate_major_then_token_position",
                "candidates": [{"candidate_id": "stage5v-key-shape-only", "key_schedule_ref": 0}],
                "execution_status": "shape_only_pending_family_contract",
                "shape_only": True,
                "raw_data_free": True,
                "no_gpu_safe": True,
                "blockers": ["family_specific_vigenere_execution_contract_pending"],
            },
            {
                **COMMON_FLAGS,
                "record_type": "candidate_batch_conformance_fixture_record",
                "schema": "schemas/cuda/candidate-batch-conformance-fixture-record-v0.schema.json",
                "fixture_id": "stage5v-stream-schedule-shape-fixture",
                "fixture_kind": "stream_schedule_shape_only",
                "source_contract_ids": ["stage5u-prime-minus-one-stream-schedule-v0"],
                "token_values": [0, 2, 4, 6],
                "token_kind": ["rune", "rune", "rune", "rune"],
                "transformable_mask": [True, True, True, True],
                "separator_positions": [],
                "fixture_offsets": [0],
                "fixture_lengths": [4],
                "stream_schedule_values": [1, 2, 4, 6, 10],
                "stream_start_index": 0,
                "stream_advance_policy": "skip_separators_shape_declared",
                "candidate_ordering": "candidate_major",
                "output_ordering": "candidate_major_then_token_position",
                "candidates": [{"candidate_id": "stage5v-stream-shape-only", "stream_schedule_ref": 0}],
                "execution_status": "shape_only_pending_family_contract",
                "shape_only": True,
                "raw_data_free": True,
                "no_gpu_safe": True,
                "blockers": ["family_specific_prime_stream_execution_contract_pending"],
            },
            {
                **COMMON_FLAGS,
                "record_type": "candidate_batch_conformance_fixture_record",
                "schema": "schemas/cuda/candidate-batch-conformance-fixture-record-v0.schema.json",
                "fixture_id": "stage5v-score-vector-fixture",
                "fixture_kind": "score_vector_shape_only",
                "source_contract_ids": ["stage5u-score-vector-contract-v0"],
                "token_values": [3, 1, 4],
                "token_kind": ["rune", "rune", "rune"],
                "transformable_mask": [True, True, True],
                "separator_positions": [],
                "fixture_offsets": [0],
                "fixture_lengths": [3],
                "score_vector_components": [
                    "candidate_id",
                    "score_status",
                    "confidence_label",
                    "score_value",
                    "component_scores",
                    "scorer_id",
                    "calibration_profile_id",
                ],
                "score_interpretation": "triage_only",
                "candidate_ordering": "candidate_major",
                "output_ordering": "candidate_major_then_token_position",
                "candidates": [{"candidate_id": "stage5v-score-vector-shape"}],
                "execution_status": "shape_only_no_transform_execution",
                "shape_only": True,
                "raw_data_free": True,
                "no_gpu_safe": True,
            },
            {
                **COMMON_FLAGS,
                "record_type": "candidate_batch_conformance_fixture_record",
                "schema": "schemas/cuda/candidate-batch-conformance-fixture-record-v0.schema.json",
                "fixture_id": "stage5v-topk-tie-policy-fixture",
                "fixture_kind": "topk_tie_policy_shape_only",
                "source_contract_ids": ["stage5u-topk-output-contract-v0"],
                "token_values": [9, 2, 6],
                "token_kind": ["rune", "rune", "rune"],
                "transformable_mask": [True, True, True],
                "separator_positions": [],
                "fixture_offsets": [0],
                "fixture_lengths": [3],
                "topk_k": 3,
                "topk_tie_policy": "score_desc_candidate_id_asc",
                "synthetic_scores": [
                    {"candidate_id": "cand-b", "score_value": 0.75},
                    {"candidate_id": "cand-a", "score_value": 0.75},
                    {"candidate_id": "cand-c", "score_value": 0.5},
                ],
                "candidate_ordering": "candidate_major",
                "output_ordering": "candidate_major_then_token_position",
                "candidates": [{"candidate_id": "stage5v-topk-shape"}],
                "execution_status": "shape_only_no_transform_execution",
                "shape_only": True,
                "raw_data_free": True,
                "no_gpu_safe": True,
            },
        ]
    )
    return records


def build_conformance_fixtures(
    *,
    conformance_fixtures_out: Path = CONFORMANCE_FIXTURES_PATH,
    out_dir: Path = OUTPUT_DIR,
) -> list[dict[str, Any]]:
    records = fixture_definitions()
    write_record_set(conformance_fixtures_out, records)
    write_report(out_dir, REPORT_FILES["conformance_fixture"], {"records": records, "count": len(records)})
    return records


def run_python_reference_conformance(
    *,
    fixtures: list[dict[str, Any]],
    out_dir: Path = OUTPUT_DIR,
) -> dict[str, Any]:
    executed = [record for record in fixtures if record["execution_status"] == "executed_python_reference"]
    results: list[dict[str, Any]] = []
    for record in executed:
        actual_outputs = candidate_major_shift_outputs(record)
        actual_hash = canonical_hash(actual_outputs)
        expected_hash = str(record["expected_output_token_hash"])
        results.append(
            {
                "fixture_id": record["fixture_id"],
                "candidate_count": len(record.get("candidates", [])),
                "token_count": len(record["token_values"]),
                "status": "passed" if actual_hash == expected_hash else "failed",
                "output_token_hash": actual_hash,
                "expected_output_token_hash": expected_hash,
                "output_ordering": record["output_ordering"],
                "generated_body_committed": False,
            }
        )
    report = {
        "record_type": "native_candidate_batch_adapter_execution_report",
        "stage_id": "stage-5v",
        "python_reference_adapter_implemented": True,
        "cpp_reference_adapter_implemented": False,
        "native_cpu_execution_performed": False,
        "executed_conformance_fixture_count": len(executed),
        "passed_count": sum(1 for result in results if result["status"] == "passed"),
        "results": results,
        "cuda_execution_performed": False,
        "gpu_benchmark_performed": False,
        "solve_claim": False,
    }
    write_report(out_dir, REPORT_FILES["native_adapter"], report)
    return report
