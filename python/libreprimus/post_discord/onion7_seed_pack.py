"""Stage 3S bounded Onion 7 explicit numeric seed-pack executor."""

from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import Any

import yaml

from libreprimus.bounded_execution.caesar_affine import labels_by_index
from libreprimus.bounded_execution.candidate_writer import write_candidate_outputs, write_jsonl
from libreprimus.bounded_execution.input_slice_loader import load_input_slice
from libreprimus.bounded_execution.models import BoundedCandidateRecord, BoundedRunSummary, InputSlice
from libreprimus.bounded_execution.vigenere_key_list import DEFAULT_CALIBRATION_SUMMARY, load_calibration_summary
from libreprimus.paths import repo_root
from libreprimus.post_discord.models import (
    DEFAULT_MANIFEST,
    DEFAULT_OUTPUT_DIR,
    EXPERIMENT_ID,
    MODULUS,
    PRIME_ORDER_TABLE,
    RAW_TABLE,
    SUPPORTED_DIRECTIONS,
    SUPPORTED_RESET_MODES,
    SUPPORTED_ROUTES,
    SUPPORTED_VALUE_SPACES,
    TRANSFORM_FAMILY,
    TRANSFORM_ID,
    DeferredOnion7Candidate,
    Onion7Input,
    Onion7Manifest,
)
from libreprimus.scoring.calibration import classify_score
from libreprimus.scoring.crib_checks import crib_check
from libreprimus.scoring.minimal_triage import score_text
from libreprimus.scoring.validation import validate_crib_check_result, validate_minimal_triage_score
from libreprimus.solved_fixtures.direct_translation import normalize_plaintext
from libreprimus.solved_fixtures.models import to_jsonable

DEFAULT_CORPUS_SLICE = {
    "slice_id": "stage3a-page-candidate-018-reviewable-slice",
    "slice_kind": "future_unsolved_page_candidate",
    "review_required": True,
    "source": "rtkd-master-v0-candidate",
    "corpus_candidate_id": "rtkd-master-v0-candidate",
    "selector": {
        "selector_kind": "corpus_page_candidate_token_range",
        "page_candidate_id": "page-candidate-018",
        "candidate_local_page_index": 18,
        "start_token_index": 5283,
        "end_token_index": 5402,
        "expected_rune_token_count": 87,
        "raw_unsolved_text_included": False,
    },
    "metadata_paths": [
        {
            "path": "data/normalized/corpus-candidates/rtkd-master-v0-candidate/page_candidates.jsonl",
            "role": "generated_ignored_page_candidate_metadata",
        },
        {
            "path": "data/normalized/corpus-candidates/rtkd-master-v0-candidate/tokens.jsonl",
            "role": "generated_ignored_token_metadata",
        },
    ],
    "raw_unsolved_text_included": False,
}


def validate_manifest_file(path: Path) -> Onion7Manifest:
    """Load and validate the Stage 3S target manifest without executing it."""
    return load_onion7_manifest(path)


def run_onion7_seed_pack(
    *,
    manifest_path: Path = Path(DEFAULT_MANIFEST),
    out_dir: Path = Path(DEFAULT_OUTPUT_DIR),
    top_k: int = 25,
    calibration_summary_path: Path = DEFAULT_CALIBRATION_SUMMARY,
) -> BoundedRunSummary:
    """Execute the bounded Stage 3S Onion 7 seed pack."""
    start = perf_counter()
    manifest = load_onion7_manifest(manifest_path)
    input_data = load_onion7_input(manifest.payload)
    labels = labels_by_index(repo_root() / "data/profiles/gematria/gematria-primus-v0.json")
    calibration = load_calibration_summary(calibration_summary_path)
    thresholds = dict(calibration.get("thresholds", {}))
    warnings = list(input_data.warnings)
    warnings.extend(f"value_space_source:{key}={value}" for key, value in sorted(manifest.table_sources.items()))
    if not calibration:
        warnings.append("stage3c_calibration_summary_missing; calibrated label falls back to current thresholds.")

    run_id = f"stage3s-{manifest.experiment_id.lower()}-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}"
    records: list[BoundedCandidateRecord] = []
    deferred: list[DeferredOnion7Candidate] = []
    candidate_index = 0
    for value_space in manifest.value_spaces:
        table = manifest.tables.get(value_space)
        for route in manifest.routes:
            for direction in manifest.directions:
                for reset_mode in manifest.reset_modes:
                    if table is None:
                        deferred.append(
                            DeferredOnion7Candidate(candidate_index, value_space, route, direction, reset_mode, "value_space_unavailable")
                        )
                        candidate_index += 1
                        continue
                    if reset_mode == "line" and not input_data.has_line_metadata:
                        deferred.append(
                            DeferredOnion7Candidate(candidate_index, value_space, route, direction, reset_mode, "line_reset_metadata_missing")
                        )
                        candidate_index += 1
                        continue
                    route_values = route_sequence(table, route)
                    if direction == "reverse":
                        route_values = list(reversed(route_values))
                    mode_warnings = [] if input_data.has_token_break_metadata else ["token_break_metadata_missing_flat_mode_used"]
                    records.append(
                        build_candidate_record(
                            run_id=run_id,
                            manifest_id=manifest.experiment_id,
                            candidate_index=candidate_index,
                            input_slice_id=input_data.input_slice.slice_id,
                            token_records=input_data.token_records,
                            labels=labels,
                            value_space=value_space,
                            route=route,
                            direction=direction,
                            reset_mode=reset_mode,
                            numeric_sequence=route_values,
                            thresholds=thresholds,
                            warnings=warnings + mode_warnings,
                        )
                    )
                    candidate_index += 1

    if candidate_index != manifest.expected_candidate_count:
        raise ValueError(f"Candidate loop drifted: expected {manifest.expected_candidate_count}, got {candidate_index}.")
    if len(records) + len(deferred) != manifest.expected_candidate_count:
        raise ValueError("Executed plus deferred candidate count does not equal expected Stage 3S count.")

    ranked = sorted(
        records,
        key=lambda record: (
            float(record.score_summary.get("length_normalized_score", record.score_summary["total_score"])),
            float(record.score_summary["total_score"]),
            int(record.crib_hit_count or 0),
            -record.candidate_index,
        ),
        reverse=True,
    )
    top_records = ranked[:top_k]
    if not top_records:
        raise ValueError("No Stage 3S candidates executed.")
    top = top_records[0]
    deferred_payloads = [to_jsonable(item) for item in deferred]
    if deferred:
        warnings.extend(
            f"{item.reason}:value_space={item.value_space}:route={item.route}:direction={item.direction}:reset={item.reset_mode}"
            for item in deferred
        )
    elapsed_ms = round((perf_counter() - start) * 1000, 3)
    confidence_distribution = confidence_distribution_for(records)

    result_store_preview = {
        "record_type": "bounded_result_store_preview",
        "run_id": run_id,
        "policy_id": "stage3s-standing-operator-policy",
        "queue_item_id": manifest.experiment_id,
        "expected_candidate_count": manifest.expected_candidate_count,
        "executed_candidate_count": len(records),
        "deferred_candidate_count": len(deferred),
        "top_candidate_index": top.candidate_index,
        "top_value_space": top.value_space,
        "top_route": top.route,
        "top_direction": top.direction,
        "top_reset_mode": top.reset_mode,
        "top_score": top.score_summary["total_score"],
        "top_length_normalized_score": top.score_summary.get("length_normalized_score"),
        "top_calibrated_confidence_label": top.calibrated_confidence_label,
        "confidence_distribution": confidence_distribution,
        "deferred_candidates": deferred_payloads,
        "import_enabled": False,
        "generated_outputs_ignored": True,
    }
    summary = BoundedRunSummary(
        record_type="bounded_experiment_run_summary",
        run_id=run_id,
        queue_item_id=manifest.experiment_id,
        input_slice_id=input_data.input_slice.slice_id,
        input_length=input_data.input_slice.input_length,
        candidate_count=len(records),
        caesar_candidate_count=0,
        affine_candidate_count=0,
        top_k_count=len(top_records),
        top_candidate={
            "candidate_index": top.candidate_index,
            "transform_family": top.transform_family,
            "transform_id": top.transform_id,
            "transform_parameters": top.transform_parameters,
            "value_space": top.value_space,
            "route": top.route,
            "direction": top.direction,
            "reset_mode": top.reset_mode,
            "numeric_sequence_mod29": top.numeric_sequence_mod29,
            "sequence_signature_sha256": top.sequence_signature_sha256,
            "total_score": top.score_summary["total_score"],
            "length_normalized_score": top.score_summary.get("length_normalized_score"),
            "confidence_label": top.score_summary.get("confidence_label"),
            "calibrated_confidence_label": top.calibrated_confidence_label,
            "crib_hits": top.crib_hits,
            "output_sha256": top.output_sha256,
        },
        output_paths={},
        generated_outputs_ignored=True,
        result_store_preview=result_store_preview,
        search_performed=True,
        scoring_used=True,
        cuda_used=False,
        canonical_corpus_active=False,
        page_boundaries_final=False,
        solve_claim=False,
        trusted_as_canonical=False,
        warnings=warnings + [f"elapsed_ms={elapsed_ms}"],
        expected_candidate_count=manifest.expected_candidate_count,
        executed_candidate_count=len(records),
        deferred_candidate_count=len(deferred),
        reset_modes=manifest.reset_modes,
        directions=manifest.directions,
        confidence_distribution=confidence_distribution,
        onion7_candidate_count=len(records),
        value_spaces=manifest.value_spaces,
        routes=manifest.routes,
    )
    paths = write_candidate_outputs(out_dir, records, top_records, summary, warnings)
    score_details_path = write_jsonl(paths["summary"].parent / "calibrated_scores.jsonl", score_details(records, calibration))
    paths["calibrated_scores"] = score_details_path
    if deferred:
        paths["deferred_candidates"] = write_jsonl(paths["summary"].parent / "deferred_candidates.jsonl", deferred_payloads)
    summary = replace(summary, output_paths={key: str(path) for key, path in paths.items()})
    write_candidate_outputs(out_dir, records, top_records, summary, warnings)
    write_jsonl(score_details_path, score_details(records, calibration))
    if deferred:
        write_jsonl(paths["summary"].parent / "deferred_candidates.jsonl", deferred_payloads)
    return summary


def load_onion7_manifest(path: Path) -> Onion7Manifest:
    """Load and validate the EXP-3R-003 manifest."""
    resolved = path if path.is_absolute() else repo_root() / path
    payload = yaml.safe_load(resolved.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Stage 3S manifest must be a mapping: {resolved}")
    experiment_id = str(payload.get("experiment_id", ""))
    if experiment_id != EXPERIMENT_ID:
        raise ValueError(f"Stage 3S only executes {EXPERIMENT_ID}; got {experiment_id}.")
    for field, expected in {
        "cpu_only": True,
        "cuda_enabled": False,
        "cloud_execution": False,
        "paid_services": False,
        "generated_outputs_committed": False,
        "no_solve_claim": True,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
    }.items():
        if payload.get(field) is not expected:
            raise ValueError(f"{experiment_id}: {field} must be {str(expected).lower()}.")
    cap = int(payload.get("candidate_count_cap", -1))
    if cap > 144:
        raise ValueError("EXP-3R-003 candidate cap must be <= 144.")
    generation = dict(payload.get("candidate_generation", {}))
    value_spaces = _checked_strings(generation, "value_spaces", SUPPORTED_VALUE_SPACES)
    routes = _checked_strings(generation, "routes", SUPPORTED_ROUTES)
    directions = _checked_strings(generation, "directions", SUPPORTED_DIRECTIONS)
    reset_modes = _checked_strings(generation, "reset_modes", SUPPORTED_RESET_MODES)
    expected = len(value_spaces) * len(routes) * len(directions) * len(reset_modes)
    if expected > cap:
        raise ValueError(f"EXP-3R-003 candidate count {expected} exceeds cap {cap}.")
    declared = int(generation.get("candidate_count_estimate", expected))
    if declared != expected:
        raise ValueError(f"EXP-3R-003 candidate_count_estimate {declared} does not match {expected}.")
    tables, table_sources = load_value_space_tables(payload)
    return Onion7Manifest(
        experiment_id=experiment_id,
        description=str(payload.get("description", "")),
        candidate_count_cap=cap,
        payload=payload,
        value_spaces=value_spaces,
        routes=routes,
        directions=directions,
        reset_modes=reset_modes,
        expected_candidate_count=expected,
        tables=tables,
        table_sources=table_sources,
    )


def load_value_space_tables(payload: dict[str, Any]) -> tuple[dict[str, list[list[int]]], dict[str, str]]:
    """Load explicit or Stage 3S-reviewed Onion 7 value-space tables."""
    raw_tables = payload.get("onion7_tables") or payload.get("value_space_tables") or {}
    source_tables = dict(raw_tables) if isinstance(raw_tables, dict) else {}
    tables: dict[str, list[list[int]]] = {}
    sources: dict[str, str] = {}
    if "raw_table" in source_tables:
        tables["raw_table"] = validate_table(source_tables["raw_table"], "raw_table")
        sources["raw_table"] = "manifest"
    else:
        tables["raw_table"] = [list(row) for row in RAW_TABLE]
        sources["raw_table"] = "stage3s_reviewed_public_table"
    if "prime_delta_table" in source_tables:
        tables["prime_delta_table"] = validate_table(source_tables["prime_delta_table"], "prime_delta_table")
        sources["prime_delta_table"] = "manifest"
    else:
        tables["prime_delta_table"] = [[abs(3301 - value) for value in row] for row in tables["raw_table"]]
        sources["prime_delta_table"] = "derived_abs_3301_minus_raw_value"
    if "prime_order_table" in source_tables:
        tables["prime_order_table"] = validate_table(source_tables["prime_order_table"], "prime_order_table")
        sources["prime_order_table"] = "manifest"
    else:
        tables["prime_order_table"] = [list(row) for row in PRIME_ORDER_TABLE]
        sources["prime_order_table"] = "stage3s_reviewed_derived_order_table"
    return tables, sources


def validate_table(value: Any, label: str) -> list[list[int]]:
    """Validate a 4x4 integer table."""
    if not isinstance(value, list) or len(value) != 4:
        raise ValueError(f"{label} must be a 4x4 table.")
    table: list[list[int]] = []
    for row in value:
        if not isinstance(row, list) or len(row) != 4:
            raise ValueError(f"{label} must be a 4x4 table.")
        table.append([int(item) for item in row])
    return table


def route_sequence(table: list[list[int]], route: str) -> list[int]:
    """Return a deterministic route sequence over a 4x4 table."""
    validate_table(table, "route_table")
    if route == "row_major":
        return [value for row in table for value in row]
    if route == "column_major":
        return [table[row][column] for column in range(4) for row in range(4)]
    if route == "reverse_row_major":
        return list(reversed(route_sequence(table, "row_major")))
    if route == "reverse_column_major":
        return list(reversed(route_sequence(table, "column_major")))
    if route == "clockwise_spiral":
        return [
            table[0][0], table[0][1], table[0][2], table[0][3],
            table[1][3], table[2][3], table[3][3], table[3][2],
            table[3][1], table[3][0], table[2][0], table[1][0],
            table[1][1], table[1][2], table[2][2], table[2][1],
        ]
    if route == "counterclockwise_spiral":
        return [
            table[0][0], table[1][0], table[2][0], table[3][0],
            table[3][1], table[3][2], table[3][3], table[2][3],
            table[1][3], table[0][3], table[0][2], table[0][1],
            table[1][1], table[2][1], table[2][2], table[1][2],
        ]
    raise ValueError(f"Unsupported Onion 7 route: {route}")


def reduce_mod29(values: list[int]) -> list[int]:
    """Reduce numeric sequence values modulo 29."""
    return [int(value) % MODULUS for value in values]


def render_onion7_candidate(
    token_records: list[dict[str, Any]],
    *,
    numeric_sequence: list[int],
    reset_mode: str,
    labels: dict[int, str],
) -> tuple[str, list[int], list[int]]:
    """Render a decrypt-subtract Onion 7 stream candidate."""
    if reset_mode not in SUPPORTED_RESET_MODES:
        raise ValueError(f"Unsupported Stage 3S reset mode: {reset_mode}")
    if not numeric_sequence:
        raise ValueError("Onion 7 numeric sequence must not be empty.")
    stream_values = reduce_mod29(numeric_sequence)
    parts: list[str] = []
    output_indices: list[int] = []
    used_stream_values: list[int] = []
    position = 0
    current_line_id: Any = object()
    for token in token_records:
        kind = str(token.get("token_kind"))
        if kind == "rune":
            line_id = _line_id(token)
            if reset_mode == "line" and line_id != current_line_id:
                position = 0
                current_line_id = line_id
            raw_index = token.get("index29")
            if not isinstance(raw_index, int) or raw_index < 0 or raw_index > 28:
                raise ValueError(f"Rune token missing valid index29 at token {token.get('token_index_global')}.")
            stream_value = stream_values[position % len(stream_values)]
            decoded_index = (raw_index - stream_value) % MODULUS
            output_indices.append(decoded_index)
            used_stream_values.append(stream_value)
            parts.append(labels[decoded_index])
            position += 1
            continue
        separator = _separator_text(token)
        if separator:
            parts.append(separator)
    return normalize_plaintext(parts), output_indices, used_stream_values


def sequence_signature(value_space: str, route: str, direction: str, reset_mode: str, numeric_sequence: list[int]) -> str:
    """Hash candidate stream identity without raw output text."""
    payload = {
        "experiment_id": EXPERIMENT_ID,
        "value_space": value_space,
        "route": route,
        "direction": direction,
        "reset_mode": reset_mode,
        "numeric_sequence": numeric_sequence,
        "numeric_sequence_mod29": reduce_mod29(numeric_sequence),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def build_candidate_record(
    *,
    run_id: str,
    manifest_id: str,
    candidate_index: int,
    input_slice_id: str,
    token_records: list[dict[str, Any]],
    labels: dict[int, str],
    value_space: str,
    route: str,
    direction: str,
    reset_mode: str,
    numeric_sequence: list[int],
    thresholds: dict[str, float],
    warnings: list[str],
) -> BoundedCandidateRecord:
    """Build and score one Stage 3S candidate record."""
    text, output_indices, used_stream_values = render_onion7_candidate(
        token_records,
        numeric_sequence=numeric_sequence,
        reset_mode=reset_mode,
        labels=labels,
    )
    signature = sequence_signature(value_space, route, direction, reset_mode, numeric_sequence)
    mod29_sequence = reduce_mod29(numeric_sequence)
    score = validate_minimal_triage_score(score_text(text))
    crib_payload = validate_crib_check_result(crib_check(text, candidate_id=f"{manifest_id}-{candidate_index}"))
    calibrated_label = classify_score(score, crib_payload, thresholds)
    calibration_position = {
        "length_normalized_score": score.get("length_normalized_score"),
        "calibrated_confidence_label": calibrated_label,
        "thresholds": thresholds,
        "score_source": "stage3c_calibrated_minimal_triage",
    }
    score["calibrated_confidence_label"] = calibrated_label
    score["crib_hit_count"] = crib_payload["crib_hit_count"]
    score["crib_hits"] = crib_payload["crib_hits"]
    score["no_solve_claim"] = True
    transform_parameters = {
        "experiment_id": EXPERIMENT_ID,
        "value_space": value_space,
        "route": route,
        "direction": direction,
        "reset_mode": reset_mode,
        "numeric_sequence": numeric_sequence,
        "numeric_sequence_mod29": mod29_sequence,
        "sequence_signature_sha256": signature,
        "stream_repeats": True,
        "decrypt_subtract": True,
        "broad_number_search_enabled": False,
        "speculative_interpretations_enabled": False,
    }
    return BoundedCandidateRecord(
        record_type="bounded_candidate_record",
        run_id=run_id,
        queue_item_id=manifest_id,
        transform_family=TRANSFORM_FAMILY,
        transform_id=TRANSFORM_ID,
        transform_parameters=transform_parameters,
        candidate_index=candidate_index,
        input_slice_id=input_slice_id,
        output_normalized_text=text,
        output_preview=text[:160],
        output_sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
        score_summary=score,
        ranking_features={
            "total_score": score["total_score"],
            "length_normalized_score": score.get("length_normalized_score", score["total_score"]),
            "confidence_label": score.get("confidence_label", "noisy"),
            "calibrated_confidence_label": calibrated_label,
            "common_word_hit_count": score["common_word_hit_count"],
            "crib_hit_count": crib_payload["crib_hit_count"],
            "latin_letter_count": score["latin_letter_count"],
            "entropy": score["entropy"],
            "value_space": value_space,
            "route": route,
            "direction": direction,
            "reset_mode": reset_mode,
            "sequence_signature_sha256": signature,
            "output_index_count": len(output_indices),
            "first_stream_values_mod29": used_stream_values[:16],
        },
        search_performed=True,
        scoring_used=True,
        cuda_used=False,
        canonical_corpus_active=False,
        page_boundaries_final=False,
        solve_claim=False,
        trusted_as_canonical=False,
        warnings=warnings,
        calibrated_confidence_label=calibrated_label,
        crib_hits=crib_payload["crib_hits"],
        crib_hit_count=crib_payload["crib_hit_count"],
        calibration_position=calibration_position,
        direction=direction,
        reset_mode=reset_mode,
        stream_signature_sha256=signature,
        experiment_id=EXPERIMENT_ID,
        manifest_id=manifest_id,
        value_space=value_space,
        route=route,
        numeric_sequence=numeric_sequence,
        numeric_sequence_mod29=mod29_sequence,
        sequence_signature_sha256=signature,
    )


def load_onion7_input(payload: dict[str, Any]) -> Onion7Input:
    """Load the reviewable input slice and associated token metadata."""
    item = {"corpus_slice": payload.get("corpus_slice") or DEFAULT_CORPUS_SLICE}
    input_slice = load_input_slice(item)
    token_records = _load_token_records(item, input_slice)
    rune_tokens = [token for token in token_records if str(token.get("token_kind")) == "rune"]
    has_token_break_metadata = any(str(token.get("token_kind")) != "rune" for token in token_records)
    has_line_metadata = bool(rune_tokens) and all(_line_id(token) is not None for token in rune_tokens)
    warnings = [warning for warning in input_slice.warnings if warning != "flat_rune_index_stream_no_separator_context"]
    if not has_token_break_metadata:
        warnings.append("token_break_metadata_missing_flat_mode_used")
    if not has_line_metadata:
        warnings.append("line_reset_metadata_missing")
    return Onion7Input(
        input_slice=input_slice,
        token_records=token_records,
        transformable_count=len(rune_tokens),
        has_token_break_metadata=has_token_break_metadata,
        has_line_metadata=has_line_metadata,
        warnings=warnings,
    )


def confidence_distribution_for(records: list[BoundedCandidateRecord]) -> dict[str, int]:
    """Count calibrated confidence labels."""
    distribution: dict[str, int] = {}
    for record in records:
        label = record.calibrated_confidence_label or str(record.score_summary.get("confidence_label", "unlabeled"))
        distribution[label] = distribution.get(label, 0) + 1
    return dict(sorted(distribution.items()))


def score_details(records: list[BoundedCandidateRecord], calibration: dict[str, Any]) -> list[dict[str, Any]]:
    """Return per-candidate calibrated score details."""
    return [
        {
            "record_type": "stage3s_calibrated_score_detail",
            "run_id": record.run_id,
            "experiment_id": EXPERIMENT_ID,
            "candidate_index": record.candidate_index,
            "value_space": record.value_space,
            "route": record.route,
            "direction": record.direction,
            "reset_mode": record.reset_mode,
            "sequence_signature_sha256": record.sequence_signature_sha256,
            "score_summary": record.score_summary,
            "calibrated_confidence_label": record.calibrated_confidence_label,
            "crib_hits": record.crib_hits,
            "calibration_position": record.calibration_position,
            "calibration_id": calibration.get("calibration_id", "missing-stage3c-calibration-summary"),
            "solve_claim": False,
            "cuda_used": False,
        }
        for record in records
    ]


def _load_token_records(item: dict[str, Any], input_slice: InputSlice) -> list[dict[str, Any]]:
    selector = dict(dict(item.get("corpus_slice", {})).get("selector", {}))
    inline_tokens = selector.get("token_records")
    if isinstance(inline_tokens, list):
        return [dict(token) for token in inline_tokens if isinstance(token, dict)]
    tokens_path = input_slice.source_metadata.get("tokens_path")
    start = input_slice.source_metadata.get("start_token_index")
    end = input_slice.source_metadata.get("end_token_index")
    if tokens_path and start is not None and end is not None:
        return _load_token_range(Path(str(tokens_path)), int(start), int(end))
    return [
        {
            "token_kind": "rune",
            "index29": value,
            "token_index_global": position,
            "synthetic_flat_token": True,
        }
        for position, value in enumerate(input_slice.index29_values)
    ]


def _load_token_range(path: Path, start: int, end: int) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        index = int(payload["token_index_global"])
        if index < start:
            continue
        if index > end:
            break
        records.append(payload)
    if not records:
        raise ValueError("Stage 3S token metadata path did not yield selector records.")
    return records


def _checked_strings(generation: dict[str, Any], field: str, supported: tuple[str, ...]) -> list[str]:
    values = [str(value) for value in generation.get(field, [])]
    if not values:
        raise ValueError(f"EXP-3R-003 candidate_generation.{field} must not be empty.")
    unknown = sorted(set(values) - set(supported))
    if unknown:
        raise ValueError(f"Unsupported EXP-3R-003 {field}: {unknown}")
    return values


def _line_id(token: dict[str, Any]) -> Any:
    for field in ("logical_line_index", "physical_line_number", "line_index"):
        value = token.get(field)
        if value is not None:
            return value
    return None


def _separator_text(token: dict[str, Any]) -> str:
    kind = str(token.get("token_kind"))
    if kind == "word_separator":
        return " "
    if kind == "clause_separator":
        return ". "
    if kind in {"line_separator", "physical_newline"}:
        return "\n"
    if kind in {"paragraph_separator", "segment_separator", "chapter_separator", "page_separator_or_marker", "whitespace"}:
        return " "
    if kind == "numeric_literal":
        return str(token.get("raw_text", ""))
    if kind == "unknown_symbol":
        return str(token.get("raw_text", ""))
    return ""
