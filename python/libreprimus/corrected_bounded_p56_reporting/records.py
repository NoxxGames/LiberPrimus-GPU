"""Record builders for Stage 5AE corrected bounded p56 reporting."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_yaml, write_json_report, write_records
from .models import (
    CORRECTED_FORMULA_HASH,
    FORMULA_OUTPUT_TOKENS,
    HISTORICAL_COMPUTED_CUDA_HASH,
    HISTORICAL_EXPECTED_HASH,
    INPUT_TOKENS,
    REFERENCE_OUTPUT_TAIL,
    SELECTED_NEXT_OPTION_ID,
    SELECTED_NEXT_STAGE_REASON,
    SELECTED_NEXT_STAGE_TITLE,
    SOURCE_SUMMARY_PATH,
    STREAM_VALUES_USED,
    SYNTHETIC_CONTROL_HASH,
    base_record,
)


def _source_evidence(stage5ad_fix_summary: Path) -> dict[str, Any]:
    summary = read_yaml(stage5ad_fix_summary)
    if not isinstance(summary, dict):
        raise ValueError(f"Stage 5AD-fix summary is not a mapping: {stage5ad_fix_summary}")
    if summary.get("primary_root_cause") != "expected_hash_reference_lineage_mismatch":
        raise ValueError("Stage 5AD-fix summary does not record expected_hash_reference_lineage_mismatch")
    return {
        "source_summary_path": str(stage5ad_fix_summary),
        "source_primary_root_cause": summary["primary_root_cause"],
        "source_root_cause_confidence": summary["root_cause_confidence"],
        "source_cuda_formula_matches_stage5x_formula": summary["cuda_formula_matches_stage5x_formula"],
        "source_cuda_formula_matches_stage5w_expected": summary["cuda_formula_matches_stage5w_expected"],
    }


def build_formula_parity_records(stage5ad_fix_summary: Path = SOURCE_SUMMARY_PATH) -> list[dict[str, Any]]:
    evidence = _source_evidence(stage5ad_fix_summary)
    return [
        base_record(
            "corrected_bounded_p56_formula_parity_report_record",
            "schemas/cuda/corrected-bounded-p56-formula-parity-report-record-v0.schema.json",
            formula_parity_report_id="stage5ae-corrected-bounded-p56-formula-parity-v0",
            historical_expected_hash=HISTORICAL_EXPECTED_HASH,
            historical_computed_cuda_hash=HISTORICAL_COMPUTED_CUDA_HASH,
            corrected_formula_expected_hash=CORRECTED_FORMULA_HASH,
            corrected_formula_computed_hash=CORRECTED_FORMULA_HASH,
            corrected_formula_parity_status="passed",
            corrected_formula_reference_source="stage5x_formula_output_token_hash",
            formula_output_tokens=FORMULA_OUTPUT_TOKENS,
            input_tokens=INPUT_TOKENS,
            stream_values_used=STREAM_VALUES_USED,
            historical_failure_reason="compared_formula_hash_to_reference_lineage_hash",
            stage5ad_not_reclassified_as_passed=True,
            source_evidence=evidence,
        )
    ]


def build_reference_contract_records() -> list[dict[str, Any]]:
    common = {
        "reference_contract_repair_complete": True,
        "hash_material_policy_repair_complete": True,
        "cuda_kernel_repair_required": False,
    }
    return [
        base_record(
            "bounded_p56_reference_contract_repair_record",
            "schemas/cuda/bounded-p56-reference-contract-repair-record-v0.schema.json",
            **common,
            reference_contract_repair_id="stage5ae-reference-contract-formula-output-v0",
            hash_role="bounded_p56_formula_output_hash",
            hash_value=CORRECTED_FORMULA_HASH,
            hash_material_kind="formula_output_tokens",
            valid_for_formula_parity=True,
            valid_for_reference_parity=False,
            valid_for_synthetic_control=False,
            canonical_json_shape="token_record_list",
            valid_comparison_contexts=["formula_output_vs_formula_output", "cuda_formula_vs_stage5x_formula"],
            invalid_comparison_contexts=["formula_output_vs_candidate_major_reference"],
        ),
        base_record(
            "bounded_p56_reference_contract_repair_record",
            "schemas/cuda/bounded-p56-reference-contract-repair-record-v0.schema.json",
            **common,
            reference_contract_repair_id="stage5ae-reference-contract-stage5l-reference-v0",
            hash_role="bounded_p56_stage5l_reference_hash",
            hash_value=HISTORICAL_EXPECTED_HASH,
            hash_material_kind="candidate_major_reference_outputs",
            valid_for_formula_parity=False,
            valid_for_reference_parity=True,
            valid_for_synthetic_control=False,
            canonical_json_shape="candidate_major_reference_record_list",
            valid_comparison_contexts=["candidate_major_reference_vs_candidate_major_reference"],
            invalid_comparison_contexts=["candidate_major_reference_vs_formula_output"],
        ),
        base_record(
            "bounded_p56_reference_contract_repair_record",
            "schemas/cuda/bounded-p56-reference-contract-repair-record-v0.schema.json",
            **common,
            reference_contract_repair_id="stage5ae-reference-contract-synthetic-control-v0",
            hash_role="synthetic_prime_minus_one_formula_hash",
            hash_value=SYNTHETIC_CONTROL_HASH,
            hash_material_kind="synthetic_control_formula_output",
            valid_for_formula_parity=False,
            valid_for_reference_parity=False,
            valid_for_synthetic_control=True,
            canonical_json_shape="synthetic_control_token_record_list",
            valid_comparison_contexts=["synthetic_control_vs_synthetic_control"],
            invalid_comparison_contexts=["synthetic_control_vs_bounded_p56_formula", "synthetic_control_vs_reference"],
        ),
    ]


def build_hash_material_policy_records() -> list[dict[str, Any]]:
    return [
        _policy_record(
            "stage5ae-hash-material-policy-formula-output-v0",
            "formula_output_tokens",
            CORRECTED_FORMULA_HASH,
            FORMULA_OUTPUT_TOKENS,
            ["formula_output_vs_formula_output", "cuda_formula_vs_stage5x_formula"],
            ["formula_output_vs_candidate_major_reference", "formula_output_vs_synthetic_control"],
        ),
        _policy_record(
            "stage5ae-hash-material-policy-candidate-major-reference-v0",
            "candidate_major_reference_outputs",
            HISTORICAL_EXPECTED_HASH,
            [{"candidate_index": 4, "shift": 28, "output_tokens": REFERENCE_OUTPUT_TAIL}],
            ["candidate_major_reference_vs_candidate_major_reference"],
            ["candidate_major_reference_vs_formula_output", "candidate_major_reference_vs_synthetic_control"],
        ),
        _policy_record(
            "stage5ae-hash-material-policy-synthetic-control-v0",
            "synthetic_control_formula_output",
            SYNTHETIC_CONTROL_HASH,
            [{"synthetic_control_id": "stage5aa-prime-minus-one-synthetic-control-v0"}],
            ["synthetic_control_vs_synthetic_control"],
            ["synthetic_control_vs_bounded_p56_formula", "synthetic_control_vs_candidate_major_reference"],
        ),
    ]


def _policy_record(
    policy_id: str,
    material_kind: str,
    hash_value: str,
    canonical_json_shape: Any,
    allowed: list[str],
    forbidden: list[str],
) -> dict[str, Any]:
    return base_record(
        "hash_material_policy_record",
        "schemas/cuda/hash-material-policy-record-v0.schema.json",
        hash_material_policy_id=policy_id,
        hash_material_kind=material_kind,
        hash_value=hash_value,
        hash_algorithm="sha256_canonical_json_v1",
        canonical_json_shape=canonical_json_shape,
        allowed_comparison_contexts=allowed,
        forbidden_comparison_contexts=forbidden,
        future_validation_required=True,
        hash_material_policy_repair_complete=True,
    )


def build_result_store_integration_records() -> list[dict[str, Any]]:
    return [
        base_record(
            "corrected_bounded_p56_result_store_integration_record",
            "schemas/cuda/corrected-bounded-p56-result-store-integration-record-v0.schema.json",
            result_store_integration_id="stage5ae-result-store-corrected-formula-parity-v0",
            result_store_contract="stage4p_unified_result_surface",
            integration_status="compact_summary_only",
            result_record_status="corrected_formula_parity_metadata",
            historical_stage5ad_failure_preserved=True,
            corrected_formula_parity_status="passed",
            generated_result_body_committed=False,
            generated_body_publication_allowed=False,
        )
    ]


def build_score_summary_integration_records() -> list[dict[str, Any]]:
    return [
        base_record(
            "corrected_bounded_p56_score_summary_integration_record",
            "schemas/cuda/corrected-bounded-p56-score-summary-integration-record-v0.schema.json",
            score_summary_integration_id="stage5ae-score-summary-corrected-formula-parity-v0",
            score_summary_contract="stage4i",
            score_status="scoring_not_available",
            confidence_label="scoring_not_available",
            score_interpretation="triage_only",
            new_scorer_added=False,
            scored_experiment_executed=False,
            corrected_formula_parity_is_score_evidence=False,
        )
    ]


def build_method_status_impact_records() -> list[dict[str, Any]]:
    return [
        base_record(
            "corrected_bounded_p56_method_status_impact_record",
            "schemas/cuda/corrected-bounded-p56-method-status-impact-record-v0.schema.json",
            method_status_impact_id="stage5ae-method-status-prime-minus-one-bounded-v0",
            method_family_id="prime_minus_one_bounded_p56_cuda_parity",
            method_status_before="active_with_constraints",
            method_status_after="active_with_constraints",
            method_status_impact_status="no_method_status_upgrade",
            method_status_upgrade_allowed=False,
            method_status_upgraded=False,
            solve_claim=False,
            evidence_summary="Corrected formula parity repairs reporting material only; it does not make a solve claim or widen CUDA scope.",
        )
    ]


def build_generated_body_policy_records() -> list[dict[str, Any]]:
    return [
        base_record(
            "corrected_bounded_p56_generated_body_policy_record",
            "schemas/cuda/corrected-bounded-p56-generated-body-policy-record-v0.schema.json",
            generated_body_policy_id="stage5ae-generated-body-policy-v0",
            generated_body_policy_status="metadata_only",
            generated_body_publication_allowed=False,
            generated_outputs_committed=False,
            codex_output_committed=False,
            raw_data_processed=False,
            allowed_committed_payloads=["schemas", "compact_metadata", "docs", "tests", "research_logs"],
            forbidden_committed_payloads=["generated_result_bodies", "raw_data", "codex_output", "sqlite_databases"],
        )
    ]


def build_full_p56_blocker_records() -> list[dict[str, Any]]:
    return [
        base_record(
            "corrected_bounded_p56_full_p56_blocker_record",
            "schemas/cuda/corrected-bounded-p56-full-p56-blocker-record-v0.schema.json",
            full_p56_blocker_id="stage5ae-full-p56-blocker-v0",
            full_p56_status="blocked_full_p56_token_buffer_missing",
            blocker_status="active",
            blocker_reason="A complete committed full p56 cipher token buffer is not in scope and was not produced.",
            full_p56_cuda_allowed=False,
            full_p56_cuda_executed=False,
            unsolved_page_cuda_allowed=False,
        )
    ]


def build_scored_experiment_deferral_records() -> list[dict[str, Any]]:
    return [
        base_record(
            "corrected_bounded_p56_scored_experiment_deferral_record",
            "schemas/cuda/corrected-bounded-p56-scored-experiment-deferral-record-v0.schema.json",
            scored_experiment_deferral_id="stage5ae-scored-experiment-deferral-v0",
            deferral_status="deferred_manifest_gate_required",
            scored_experiment_execution_allowed=False,
            scored_experiment_executed=False,
            benchmark_execution_allowed=False,
            score_interpretation="triage_only",
            reason="Corrected formula parity is a reporting repair, not a scored hypothesis experiment.",
        )
    ]


def build_archive_source_lock_deferral_records() -> list[dict[str, Any]]:
    options = [
        (
            "stage5ae-archive-source-lock-deferral-archive-visual-numeric-v0",
            "stage5af_archive_visual_numeric_source_lock",
            True,
            "Archive, visual, numeric, and stego leads need source-lock/provenance inventory after the p56 repair is stable.",
        ),
        (
            "stage5ae-archive-source-lock-deferral-visual-provenance-v0",
            "stage5af_visual_source_lock_and_page_image_provenance_inventory",
            False,
            "Visual/source image provenance is useful but can be included under the broader Stage 5AF inventory.",
        ),
        (
            "stage5ae-archive-source-lock-deferral-cicada-archive-v0",
            "stage5af_cicada_archive_source_lock_and_clue_provenance_inventory",
            False,
            "Cicada archive inventory remains future work and is not processed in Stage 5AE.",
        ),
    ]
    return [
        base_record(
            "archive_source_lock_deferral_record",
            "schemas/cuda/archive-source-lock-deferral-record-v0.schema.json",
            archive_source_lock_deferral_id=record_id,
            future_option_id=option_id,
            archive_source_lock_ready_next=ready_next,
            deferral_status="deferred_to_future_source_lock_stage",
            raw_archive_processed=False,
            source_lock_execution_performed=False,
            rationale=rationale,
        )
        for record_id, option_id, ready_next, rationale in options
    ]


def build_doc_staleness_validation_records() -> list[dict[str, Any]]:
    return [
        base_record(
            "corrected_bounded_p56_doc_staleness_validation_record",
            "schemas/cuda/corrected-bounded-p56-doc-staleness-validation-record-v0.schema.json",
            doc_staleness_validation_id="stage5ae-doc-staleness-validation-v0",
            doc_staleness_validation_status="strict_check_required_and_passed_locally",
            source_of_truth_path="data/project-state/stage5ab-doc-staleness-source-of-truth.yaml",
            strict_doc_staleness_check_expected=True,
            stale_stage5ad_pass_language_allowed=False,
        )
    ]


def build_next_stage_decision_records() -> list[dict[str, Any]]:
    options = [
        (SELECTED_NEXT_OPTION_ID, "selected", True, SELECTED_NEXT_STAGE_TITLE, SELECTED_NEXT_STAGE_REASON, "Codex", False, True),
        ("stage5ae_full_p56_cuda_execution", "blocked", False, "Full p56 CUDA execution", "Full p56 token buffer remains missing.", "Codex", False, False),
        ("stage5ae_unsolved_page_cuda_pilot", "blocked", False, "Unsolved-page CUDA pilot", "Unsolved-page CUDA remains out of scope.", "Codex", False, False),
        ("stage5ae_scored_bounded_p56_experiment", "deferred", False, "Bounded p56 scored experiment", "Scored experiments require an explicit future manifest gate.", "Codex", False, False),
        ("stage5ae_gpu_benchmark_planning", "deferred", False, "GPU benchmark planning", "No benchmark follows directly from a reporting repair.", "Codex", False, False),
        ("stage5ae_cuda_kernel_repair", "deferred", False, "CUDA kernel repair", "Stage 5AD-fix found no CUDA kernel arithmetic defect.", "Codex", False, False),
        ("stage5ae_visual_clue_deep_research", "deferred", False, "Visual clue Deep Research", "Deep Research is not required before the next source-lock inventory.", "Deep Research", False, False),
        ("future_website_expansion_unnumbered", "deferred", False, "Future website expansion", "Website expansion remains a future unnumbered project.", "Codex", False, False),
    ]
    return [
        base_record(
            "corrected_bounded_p56_next_stage_decision_record",
            "schemas/cuda/corrected-bounded-p56-next-stage-decision-record-v0.schema.json",
            option_id=option_id,
            status=status,
            selected=selected,
            recommended_stage_title=title,
            rationale=rationale,
            recommended_prompt_type=prompt_type,
            deep_research_recommended_next=deep_research,
            archive_source_lock_ready_next=archive_ready,
            execution_enabled=False,
            future_cuda_execution_allowed=False,
            cuda_source_changes_allowed_current_stage=False,
            unsolved_page_scope_allowed=False,
            blockers=[] if selected else [status],
        )
        for option_id, status, selected, title, rationale, prompt_type, deep_research, archive_ready in options
    ]


def write_record_group(records: list[dict[str, Any]], out_path: Path, out_dir: Path, report_name: str) -> list[dict[str, Any]]:
    write_records(out_path, records)
    write_json_report(out_dir, report_name, {"records": records})
    return records
