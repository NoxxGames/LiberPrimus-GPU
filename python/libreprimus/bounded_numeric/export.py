"""Stage 4D bounded numeric verifier orchestration."""

from __future__ import annotations

from typing import Any
from pathlib import Path

from libreprimus.bounded_numeric.delimiter_handedness import audit_delimiter_handedness, delimiter_summary
from libreprimus.bounded_numeric.gp_rune_batch import run_gp_rune_batch
from libreprimus.bounded_numeric.loaders import load_yaml_records, write_json, write_jsonl
from libreprimus.bounded_numeric.manifest_loader import load_stage4b_manifests, manifest_by_id
from libreprimus.bounded_numeric.models import (
    EXPECTED_MANIFEST_IDS,
    MANIFEST_COOKIE,
    MANIFEST_CUNEIFORM,
    MANIFEST_DELIMITER,
    MANIFEST_DOT_AMBIGUITY,
    MANIFEST_GP_RUNE,
    MANIFEST_ONION7,
    MANIFEST_VISUAL_NEGATIVE,
)
from libreprimus.bounded_numeric.no_fudge_policy import validate_no_fudge_record
from libreprimus.bounded_numeric.number_square_routes import (
    build_number_square_route_records,
    extract_raw_number_square_tables,
)
from libreprimus.bounded_numeric.visual_negative_controls import (
    audit_dot_ambiguity,
    audit_visual_negative_controls,
)


def run_bounded_numeric_pack(
    *,
    manifest_dir: Path,
    stage4b_visual: Path,
    stage4c_tasks: Path,
    stage4c_cuneiform: Path,
    stage4c_dot: Path,
    stage4c_delimiter: Path,
    stage4c_negative: Path,
    out_dir: Path,
    allow_warnings: bool = False,
) -> dict[str, Any]:
    """Run Stage 4D bounded numeric and metadata audits."""

    del stage4c_tasks
    out_dir.mkdir(parents=True, exist_ok=True)
    manifests = load_stage4b_manifests(manifest_dir)
    manifest_map = manifest_by_id(manifests)
    missing = sorted(EXPECTED_MANIFEST_IDS - set(manifest_map))
    if missing:
        raise ValueError(f"missing_stage4b_manifests:{missing}")

    visual_records = load_yaml_records(stage4b_visual)
    cuneiform_records = load_yaml_records(stage4c_cuneiform)
    dot_records = load_yaml_records(stage4c_dot)
    delimiter_records = load_yaml_records(stage4c_delimiter)
    negative_records = load_yaml_records(stage4c_negative)

    result_records: list[dict[str, Any]] = []
    negative_control_records: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    manifest_status_records: list[dict[str, Any]] = []

    gp_records = run_gp_rune_batch(manifest_map[MANIFEST_GP_RUNE], visual_records)
    result_records.extend(gp_records)
    manifest_status_records.append(_manifest_status(manifest_map[MANIFEST_GP_RUNE], _status_from_records(gp_records), len(gp_records)))

    delimiter_records_out = audit_delimiter_handedness(manifest_map[MANIFEST_DELIMITER], delimiter_records)
    result_records.extend(delimiter_records_out)
    manifest_status_records.append(_manifest_status(manifest_map[MANIFEST_DELIMITER], "audited", len(delimiter_records_out)))

    dot_records_out = audit_dot_ambiguity(manifest_map[MANIFEST_DOT_AMBIGUITY], dot_records)
    result_records.extend(dot_records_out)
    manifest_status_records.append(_manifest_status(manifest_map[MANIFEST_DOT_AMBIGUITY], "audited", len(dot_records_out)))

    raw_tables = extract_raw_number_square_tables(visual_records)
    number_square_records = build_number_square_route_records(manifest_map[MANIFEST_ONION7], raw_tables)
    result_records.extend(number_square_records)
    number_square_status = _status_from_records(number_square_records)
    manifest_status_records.append(_manifest_status(manifest_map[MANIFEST_ONION7], number_square_status, len(number_square_records)))
    if number_square_status == "skipped_missing_raw_values":
        warnings.append({"warning": "number_square_raw_values_missing_source_lock"})

    negative_control_records = audit_visual_negative_controls(manifest_map[MANIFEST_VISUAL_NEGATIVE], negative_records)
    manifest_status_records.append(_manifest_status(manifest_map[MANIFEST_VISUAL_NEGATIVE], "audited", len(negative_control_records)))

    cuneiform_status, cuneiform_record = _cuneiform_status_record(manifest_map[MANIFEST_CUNEIFORM], cuneiform_records)
    result_records.append(cuneiform_record)
    manifest_status_records.append(_manifest_status(manifest_map[MANIFEST_CUNEIFORM], cuneiform_status, 0))

    cookie_record = _deferred_record(
        manifest_map[MANIFEST_COOKIE],
        status="deferred_not_stage4d",
        audit_type="cookie_pack_v2",
        notes="Cookie pack v2 is explicitly out of scope for Stage 4D.",
    )
    result_records.append(cookie_record)
    manifest_status_records.append(_manifest_status(manifest_map[MANIFEST_COOKIE], "deferred_not_stage4d", 0))

    record_errors = _record_errors(result_records)
    if record_errors and not allow_warnings:
        raise ValueError("; ".join(record_errors))
    warnings.extend({"warning": item} for item in record_errors)

    paths = {
        "result_records": write_jsonl(out_dir / "result_records.jsonl", result_records),
        "manifest_status_records": write_jsonl(out_dir / "manifest_status_records.jsonl", manifest_status_records),
        "negative_control_records": write_jsonl(out_dir / "negative_control_records.jsonl", negative_control_records),
        "warnings": write_jsonl(out_dir / "warnings.jsonl", warnings),
    }
    summary = _summary(
        manifest_dir=manifest_dir,
        out_dir=out_dir,
        manifests=manifests,
        result_records=result_records,
        manifest_status_records=manifest_status_records,
        negative_control_records=negative_control_records,
        delimiter_records=delimiter_records_out,
        raw_tables=raw_tables,
        output_paths={key: str(path.as_posix()) for key, path in paths.items()},
    )
    paths["summary"] = write_json(out_dir / "summary.json", summary)
    summary["output_paths"]["summary"] = paths["summary"].as_posix()
    write_json(out_dir / "summary.json", summary)
    return summary


def _summary(
    *,
    manifest_dir: Path,
    out_dir: Path,
    manifests: list[dict[str, Any]],
    result_records: list[dict[str, Any]],
    manifest_status_records: list[dict[str, Any]],
    negative_control_records: list[dict[str, Any]],
    delimiter_records: list[dict[str, Any]],
    raw_tables: list[list[list[int]]],
    output_paths: dict[str, str],
) -> dict[str, Any]:
    status_counts: dict[str, int] = {}
    for record in manifest_status_records:
        status = str(record.get("status"))
        status_counts[status] = status_counts.get(status, 0) + 1
    delimiter_counts = delimiter_summary(delimiter_records)
    return {
        "run_id": "stage4d-bounded-numeric",
        "manifest_dir": manifest_dir.as_posix(),
        "results_dir": out_dir.as_posix(),
        "manifests_discovered": len(manifests),
        "manifests_executed": sum(1 for record in manifest_status_records if record.get("status") == "audited"),
        "manifests_deferred": sum(1 for record in manifest_status_records if str(record.get("status")).startswith(("deferred", "skipped"))),
        "manifest_status_counts": dict(sorted(status_counts.items())),
        "gp_rune_claims_verified": sum(1 for record in result_records if str(record.get("status")).startswith("verified_claim_verified")),
        "gp_rune_claims_skipped": sum(1 for record in result_records if record.get("status") == "skipped_no_exact_claims"),
        "delimiter_observations_audited": delimiter_counts["delimiter_observations_audited"],
        "number_square_candidates_executed": sum(1 for record in result_records if record.get("status") == "executed_no_fudge_route"),
        "number_square_candidates_skipped": sum(1 for record in result_records if record.get("status") == "skipped_missing_raw_values"),
        "raw_number_square_tables_loaded": len(raw_tables),
        "visual_negative_controls_audited": len(negative_control_records),
        "dot_ambiguity_audits": sum(1 for record in result_records if record.get("audit_type") == "dot_ambiguity_audit"),
        "cuneiform_deferred": any(record.get("status") == "deferred_needs_human_annotation" for record in result_records),
        "cookie_pack_deferred": any(record.get("status") == "deferred_not_stage4d" and record.get("audit_type") == "cookie_pack_v2" for record in result_records),
        "result_records_count": len(result_records),
        "negative_control_records_count": len(negative_control_records),
        "no_fudge_policy": True,
        "solve_claim": False,
        "cuda_used": False,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "raw_outputs_committed": False,
        "generated_outputs_committed": False,
        "output_paths": output_paths,
    }


def _manifest_status(manifest: dict[str, Any], status: str, result_count: int) -> dict[str, Any]:
    return {
        "record_type": "bounded_numeric_manifest_status",
        "manifest_id": str(manifest.get("manifest_id")),
        "status": status,
        "candidate_count_upper_bound": int(manifest.get("candidate_count_upper_bound") or 0),
        "result_count": result_count,
        "execution_enabled_source_manifest": bool(manifest.get("execution_enabled")),
        "stage4d_authorized_subset": True,
        "no_fudge_policy": True,
        "solve_claim": False,
        "cuda_used": False,
        "generated_outputs_committed": False,
        "notes": "Stage 4D status record; source Stage 4B manifest remains disabled.",
    }


def _status_from_records(records: list[dict[str, Any]]) -> str:
    statuses = {str(record.get("status")) for record in records}
    if "skipped_no_exact_claims" in statuses:
        return "skipped_no_exact_claims"
    if "skipped_missing_raw_values" in statuses:
        return "skipped_missing_raw_values"
    if statuses:
        return "audited"
    return "skipped_no_records"


def _cuneiform_status_record(manifest: dict[str, Any], cuneiform_records: list[dict[str, Any]]) -> tuple[str, dict[str, Any]]:
    ready = any(
        record.get("annotation_status") == "annotated"
        and record.get("review_status") in {"accepted", "verified"}
        and record.get("coordinate_system") != "unknown_pending_annotation"
        and record.get("usable_as_experiment_seed") is True
        for record in cuneiform_records
    )
    if ready:
        return (
            "deferred_requires_explicit_future_stage",
            _deferred_record(
                manifest,
                status="deferred_requires_explicit_future_stage",
                audit_type="cuneiform_reading_pack",
                notes="A future explicit stage is required before cuneiform seed execution.",
            ),
        )
    return (
        "deferred_needs_human_annotation",
        _deferred_record(
            manifest,
            status="deferred_needs_human_annotation",
            audit_type="cuneiform_reading_pack",
            notes="Cuneiform candidate has no accepted coordinates/readout; seed execution remains disabled.",
        ),
    )


def _deferred_record(manifest: dict[str, Any], *, status: str, audit_type: str, notes: str) -> dict[str, Any]:
    manifest_id = str(manifest.get("manifest_id"))
    return {
        "record_type": "bounded_numeric_result_record",
        "result_id": f"{manifest_id}-{status}",
        "execution_manifest_id": manifest_id,
        "audit_type": audit_type,
        "status": status,
        "candidate_count": 0,
        "cap": int(manifest.get("candidate_count_upper_bound") or 0),
        "raw_values": None,
        "derived_values": [],
        "no_fudge_policy": True,
        "solve_claim": False,
        "cuda_used": False,
        "trusted_as_canonical": False,
        "generated_outputs_committed": False,
        "notes": notes,
    }


def _record_errors(records: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for record in records:
        errors.extend(validate_no_fudge_record(record))
    return errors
