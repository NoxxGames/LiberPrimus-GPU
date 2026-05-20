"""Validation for Stage 3Y research-synthesis records."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.paths import repo_root
from libreprimus.research_synthesis.loader import load_all_record_sets, resolve_repo_path
from libreprimus.research_synthesis.models import (
    ALLOWED_METHOD_STATUSES,
    DEFAULT_DATA_DIR,
    DEFAULT_STAGED_PLAN,
    RECORD_SET_SPECS,
    REQUIRED_METHOD_FAMILIES,
)


def validate_research_synthesis(
    data_dir: Path = DEFAULT_DATA_DIR,
    staged_plan: Path = DEFAULT_STAGED_PLAN,
) -> tuple[dict[str, Any], list[str]]:
    """Validate research-synthesis records and staged-plan guardrails."""

    errors: list[str] = []
    summary: dict[str, Any] = {
        "data_dir": str(data_dir),
        "staged_plan": str(staged_plan),
        "record_counts": {},
        "method_status_counts": {},
    }

    staged_plan_path = resolve_repo_path(staged_plan)
    if not staged_plan_path.is_file():
        errors.append(f"staged_plan_missing: {staged_plan_path}")
    else:
        staged_text = staged_plan_path.read_text(encoding="utf-8").lower()
        _require_text(errors, staged_text, ("stage 3w", "complete"), "staged_plan_stage3w_complete")
        _require_text(errors, staged_text, ("stage 3x", "complete"), "staged_plan_stage3x_complete")
        _require_text(errors, staged_text, ("stage 3y", "complete"), "staged_plan_stage3y_complete")
        _require_text(errors, staged_text, ("stage 3z",), "staged_plan_stage3z_present")
        _require_text(
            errors,
            staged_text,
            ("stage 4a", "discord research-bundle", "deep research"),
            "staged_plan_stage4a_discord_research_bundle",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 4b", "source-lock", "visual observation"),
            "staged_plan_stage4b_source_lock_visual_observation",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 4c", "cuneiform", "dot"),
            "staged_plan_stage4c_cuneiform_dot",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 4d", "bounded numeric verifier"),
            "staged_plan_stage4d_bounded_numeric_verifier",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 4e", "source-lock delta audit"),
            "staged_plan_stage4e_source_delta_audit",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 4f", "outguess", "audio"),
            "staged_plan_stage4f_outguess_audio",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 4g", "cookie", "exact"),
            "staged_plan_stage4g_cookie_exact",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 4h", "cpu batch"),
            "staged_plan_stage4h_cpu_batch",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 4i", "scorer", "calibration", "complete"),
            "staged_plan_stage4i_scorer_calibration_complete",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 4j", "observation review", "complete"),
            "staged_plan_stage4j_observation_review_complete",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 4k", "source-lock", "complete"),
            "staged_plan_stage4k_source_lock_complete",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 4l", "reviewed observation promotion ledger"),
            "staged_plan_stage4l_promotion_ledger_next",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 4l", "reviewed observation promotion ledger", "complete"),
            "staged_plan_stage4l_promotion_ledger_complete",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 4m", "image source-variant", "compression preflight", "complete"),
            "staged_plan_stage4m_image_preflight_complete",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 4n", "outguess", "audio", "positive-control", "complete"),
            "staged_plan_stage4n_outguess_audio_complete",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 4o", "cpu batch", "adapter expansion"),
            "staged_plan_stage4o_cpu_batch_adapter_present",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 4o", "cpu batch", "adapter expansion", "complete"),
            "staged_plan_stage4o_cpu_batch_adapter_complete",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 4p", "result-store", "score-summary"),
            "staged_plan_stage4p_result_store_score_summary_next",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 4p", "result-store", "score-summary", "complete"),
            "staged_plan_stage4p_result_store_score_summary_complete",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 4q", "cpu benchmark", "parity planning", "complete"),
            "staged_plan_stage4q_cpu_benchmark_parity_complete",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 5a", "cuda planning", "parity scaffolding"),
            "staged_plan_stage5a_cuda_planning_next",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 5a", "cuda planning", "parity scaffolding", "complete"),
            "staged_plan_stage5a_cuda_planning_complete",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 5b", "cuda parity harness skeleton"),
            "staged_plan_stage5b_cuda_parity_harness_next",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 5b", "cuda parity harness skeleton", "complete"),
            "staged_plan_stage5b_cuda_parity_harness_complete",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 5c", "cuda build", "device-detection scaffold", "complete"),
            "staged_plan_stage5c_cuda_build_device_detection_complete",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 5d", "native c++ cpu batch backend", "deterministic threading baseline", "complete"),
            "staged_plan_stage5d_native_cpp_cpu_backend_complete",
        )
        _require_text(
            errors,
            staged_text,
            ("stage 5e", "first cuda kernel contract", "cpu/native parity adapter selection", "next"),
            "staged_plan_stage5e_first_cuda_kernel_contract_next",
        )
        _require_text(errors, staged_text, ("cuda", "deferred"), "staged_plan_cuda_deferred")
        _require_text(errors, staged_text, ("canonical corpus", "inactive"), "staged_plan_canonical_inactive")
        _require_text(errors, staged_text, ("page boundaries", "reviewable"), "staged_plan_boundaries_reviewable")
        _require_text(errors, staged_text, ("update policy",), "staged_plan_update_policy")

    records_by_key: dict[str, list[dict[str, Any]]] = {}
    try:
        records_by_key = load_all_record_sets(data_dir)
    except (FileNotFoundError, ValueError) as error:
        errors.append(str(error))
        return summary, errors

    for spec in RECORD_SET_SPECS:
        records = records_by_key.get(spec.key, [])
        summary["record_counts"][spec.key] = len(records)
        schema_path = repo_root() / spec.schema_path
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            errors.append(f"schema_missing: {schema_path}")
            continue
        validator = Draft202012Validator(schema)
        for index, record in enumerate(records):
            if record.get("record_type") != spec.record_type:
                errors.append(f"{spec.filename}[{index}] record_type mismatch")
            for validation_error in validator.iter_errors(record):
                path = ".".join(str(part) for part in validation_error.path)
                errors.append(f"{spec.filename}[{index}] {path}: {validation_error.message}")

    method_records = records_by_key.get("method_families", [])
    method_ids = {str(record.get("method_family_id")) for record in method_records}
    missing_methods = REQUIRED_METHOD_FAMILIES - method_ids
    if missing_methods:
        errors.append(f"missing_method_families: {sorted(missing_methods)}")

    status_counter = Counter(str(record.get("status")) for record in method_records)
    summary["method_status_counts"] = dict(sorted(status_counter.items()))
    for record in method_records:
        method_id = str(record.get("method_family_id"))
        status = str(record.get("status"))
        if status not in ALLOWED_METHOD_STATUSES:
            errors.append(f"invalid_method_status: {method_id}={status}")
        if not record.get("reopen_conditions"):
            errors.append(f"missing_reopen_conditions: {method_id}")
        if not record.get("stop_conditions"):
            errors.append(f"missing_stop_conditions: {method_id}")
        if record.get("solve_claim") is not False:
            errors.append(f"solve_claim_not_false: {method_id}")

    retirement_records = records_by_key.get("method_retirements", [])
    for record in retirement_records:
        method_id = str(record.get("method_family_id"))
        if method_id not in method_ids:
            errors.append(f"retirement_references_missing_method: {method_id}")
        if not record.get("reopen_conditions"):
            errors.append(f"retirement_missing_reopen_conditions: {method_id}")

    direction_changes = records_by_key.get("direction_changes", [])
    stage4a_change = _find_record(direction_changes, "change_id", "stage3z-stage4-discord-bundle-priority")
    if stage4a_change is None:
        errors.append("stage3z_stage4_discord_bundle_priority_missing")
    else:
        new_direction = str(stage4a_change.get("new_direction", "")).lower()
        affected_docs = " ".join(str(item) for item in stage4a_change.get("affected_docs", [])).lower()
        if "discord research-bundle" not in new_direction or "deep research" not in new_direction:
            errors.append("stage3z_stage4_direction_missing_discord_deep_research")
        if "docs/roadmap/staged-plan.md" not in affected_docs or "roadmap.md" not in affected_docs:
            errors.append("stage3z_stage4_direction_missing_affected_docs")
    stage4b_change = _find_record(direction_changes, "change_id", "stage4b-source-lock-visual-intake-priority")
    if stage4b_change is None:
        errors.append("stage4b_source_lock_visual_intake_priority_missing")
    else:
        new_direction = str(stage4b_change.get("new_direction", "")).lower()
        if "source" not in new_direction or "visual" not in new_direction or "annotation" not in new_direction:
            errors.append("stage4b_direction_missing_source_visual_annotation")

    influence_records = records_by_key.get("deep_research_influences", [])
    if _find_record(influence_records, "report_id", "stage4a-discord-research-bundle-review") is None:
        errors.append("stage4a_discord_research_bundle_review_influence_missing")

    cuneiform_dot = _find_method(method_records, "cuneiform_dot_annotation_pack")
    if cuneiform_dot is None:
        errors.append("cuneiform_dot_annotation_pack_missing")
    else:
        stop_text = " ".join(str(item).lower() for item in cuneiform_dot.get("stop_conditions", []))
        if "seed" not in stop_text or "unreviewed" not in stop_text:
            errors.append("cuneiform_dot_annotation_pack_missing_seed_guardrail")

    bounded_numeric = _find_method(method_records, "bounded_numeric_verifier_pack")
    if bounded_numeric is None:
        errors.append("bounded_numeric_verifier_pack_missing")
    else:
        stop_text = " ".join(str(item).lower() for item in bounded_numeric.get("stop_conditions", []))
        if "no-fudge" not in stop_text or "broaden" not in stop_text:
            errors.append("bounded_numeric_verifier_pack_missing_no_fudge_guardrail")

    source_delta = _find_method(method_records, "source_delta_audit")
    if source_delta is None:
        errors.append("source_delta_audit_missing")
    else:
        stop_text = " ".join(str(item).lower() for item in source_delta.get("stop_conditions", []))
        if "blind-mirror" not in stop_text or "fonts" not in stop_text:
            errors.append("source_delta_audit_missing_raw_artifact_guardrail")

    stego_fixtures = _find_method(method_records, "stego_audio_fixture_source_lock")
    if stego_fixtures is None:
        errors.append("stego_audio_fixture_source_lock_missing")
    else:
        stop_text = " ".join(str(item).lower() for item in stego_fixtures.get("stop_conditions", []))
        if "outguess" not in stop_text or "raw image/audio/binary/font" not in stop_text:
            errors.append("stego_audio_fixture_source_lock_missing_tool_raw_guardrail")

    cpu_batch = _find_method(method_records, "cpu_batch_transform_api")
    if cpu_batch is None:
        errors.append("cpu_batch_transform_api_missing")
    else:
        stop_text = " ".join(str(item).lower() for item in cpu_batch.get("stop_conditions", []))
        if "gpu" not in stop_text or "parity" not in stop_text:
            errors.append("cpu_batch_transform_api_missing_parity_guardrail")

    scoring = _find_method(method_records, "scoring_consolidation")
    if scoring is None:
        errors.append("scoring_consolidation_missing")
    else:
        stop_text = " ".join(str(item).lower() for item in scoring.get("stop_conditions", []))
        if "solve" not in stop_text or "cuda" not in stop_text:
            errors.append("scoring_consolidation_missing_triage_cuda_guardrail")

    observation_review = _find_method(method_records, "observation_review_workflow")
    if observation_review is None:
        errors.append("observation_review_workflow_missing")
    else:
        stop_text = " ".join(
            str(item).lower() for item in observation_review.get("stop_conditions", [])
        )
        if "review-only" not in stop_text or "seed" not in stop_text or "local path" not in stop_text:
            errors.append("observation_review_workflow_missing_promotion_path_guardrail")

    source_snapshots = _find_method(method_records, "source_lock_snapshots")
    if source_snapshots is None:
        errors.append("source_lock_snapshots_missing")
    else:
        stop_text = " ".join(str(item).lower() for item in source_snapshots.get("stop_conditions", []))
        if "broad crawl" not in stop_text or "binaries/images/audio/fonts/archives" not in stop_text:
            errors.append("source_lock_snapshots_missing_allowlist_raw_guardrail")

    promotion_ledger = _find_method(method_records, "observation_promotion_ledger")
    if promotion_ledger is None:
        errors.append("observation_promotion_ledger_missing")
    else:
        stop_text = " ".join(str(item).lower() for item in promotion_ledger.get("stop_conditions", []))
        if "ready_for_manifest" not in stop_text or "control-only" not in stop_text:
            errors.append("observation_promotion_ledger_missing_manifest_control_guardrail")

    image_preflight = _find_method(method_records, "image_source_variant_compression_preflight")
    if image_preflight is None:
        errors.append("image_source_variant_compression_preflight_missing")
    else:
        stop_text = " ".join(str(item).lower() for item in image_preflight.get("stop_conditions", []))
        if "hidden-message" not in stop_text or "raw image" not in stop_text or "seed" not in stop_text:
            errors.append("image_source_variant_compression_preflight_missing_image_guardrail")

    stego_positive_controls = _find_method(method_records, "stego_audio_positive_control_readiness")
    if stego_positive_controls is None:
        errors.append("stego_audio_positive_control_readiness_missing")
    else:
        stop_text = " ".join(str(item).lower() for item in stego_positive_controls.get("stop_conditions", []))
        if "expected-output" not in stop_text or "raw artefact" not in stop_text or "tool" not in stop_text:
            errors.append("stego_audio_positive_control_readiness_missing_fixture_guardrail")

    result_unification = _find_method(method_records, "result_store_score_summary_unification")
    if result_unification is None:
        errors.append("result_store_score_summary_unification_missing")
    else:
        stop_text = " ".join(str(item).lower() for item in result_unification.get("stop_conditions", []))
        if "generated result" not in stop_text or "scorer" not in stop_text or "solve" not in stop_text:
            errors.append("result_store_score_summary_unification_missing_reporting_guardrail")

    cuda = _find_method(method_records, "cuda_gpu_acceleration")
    if cuda is None or cuda.get("status") != "deferred":
        errors.append("cuda_gpu_acceleration_not_deferred")

    cuda_planning = _find_method(method_records, "cuda_planning_parity_scaffolding")
    if cuda_planning is None:
        errors.append("cuda_planning_parity_scaffolding_missing")
    else:
        stop_text = " ".join(str(item).lower() for item in cuda_planning.get("stop_conditions", []))
        if "cuda implementation" not in stop_text or "gpu benchmark" not in stop_text or "speedup" not in stop_text:
            errors.append("cuda_planning_parity_scaffolding_missing_planning_guardrail")

    cuda_harness = _find_method(method_records, "cuda_parity_harness_skeleton")
    if cuda_harness is None:
        errors.append("cuda_parity_harness_skeleton_missing")
    else:
        stop_text = " ".join(str(item).lower() for item in cuda_harness.get("stop_conditions", []))
        if "kernel" not in stop_text or "gpu benchmark" not in stop_text or "speedup" not in stop_text:
            errors.append("cuda_parity_harness_skeleton_missing_no_kernel_guardrail")

    cuda_build = _find_method(method_records, "cuda_build_device_detection")
    if cuda_build is None:
        errors.append("cuda_build_device_detection_missing")
    else:
        stop_text = " ".join(str(item).lower() for item in cuda_build.get("stop_conditions", []))
        next_text = str(cuda_build.get("next_action", "")).lower()
        if "kernel" not in stop_text or "gpu benchmark" not in stop_text or "speedup" not in stop_text:
            errors.append("cuda_build_device_detection_missing_no_kernel_guardrail")
        if "stage 5d" not in next_text and "stage 5e" not in next_text:
            errors.append("cuda_build_device_detection_missing_stage5d_or_stage5e_next_action")

    native_cpu = _find_method(method_records, "native_cpp_cpu_backend")
    if native_cpu is None:
        errors.append("native_cpp_cpu_backend_missing")
    else:
        stop_text = " ".join(str(item).lower() for item in native_cpu.get("stop_conditions", []))
        if "cuda kernel" not in stop_text or "python worker" not in stop_text or "speedup" not in stop_text:
            errors.append("native_cpp_cpu_backend_missing_backend_guardrail")

    cookie = _find_method(method_records, "cookie_hash_sha256_packs")
    if cookie is None:
        errors.append("cookie_hash_sha256_packs_missing")
    else:
        stop_text = " ".join(str(item).lower() for item in cookie.get("stop_conditions", []))
        if "broad" not in stop_text or "new source" not in stop_text:
            errors.append("cookie_hash_sha256_pack_missing_no_broadening_guardrail")

    for key, records in records_by_key.items():
        for record in records:
            if record.get("solve_claim") is True:
                errors.append(f"{key}:{record.get('record_type')} solve_claim=true")
            if record.get("raw_outputs_committed") is True:
                errors.append(f"{key}:{record.get('record_type')} raw_outputs_committed=true")
            if record.get("generated_outputs_committed") is True:
                errors.append(f"{key}:{record.get('record_type')} generated_outputs_committed=true")

    summary["valid"] = not errors
    return summary, errors


def _require_text(errors: list[str], text: str, terms: tuple[str, ...], check_id: str) -> None:
    if not all(term in text for term in terms):
        errors.append(check_id)


def _find_method(records: list[dict[str, Any]], method_family_id: str) -> dict[str, Any] | None:
    for record in records:
        if record.get("method_family_id") == method_family_id:
            return record
    return None


def _find_record(records: list[dict[str, Any]], key: str, value: str) -> dict[str, Any] | None:
    for record in records:
        if record.get(key) == value:
            return record
    return None
