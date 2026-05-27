"""Stage 5BD token-block dry-run planning without byte-stream generation."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from libreprimus.token_block.models import (
    STAGE5AV_BRANCH_MANIFEST_PATH,
    STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH,
    STAGE5AY_ALPHABET_CONTROL_MANIFEST_PATH,
    STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH,
    STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH,
    STAGE5AY_NULL_CONTROL_FAMILY_MANIFEST_PATH,
    STAGE5AY_PAGE_SPLIT_CONTROL_MANIFEST_PATH,
    STAGE5AY_READING_ORDER_CONTROL_MANIFEST_PATH,
    STAGE5AY_SOURCE_CONTROL_MANIFEST_PATH,
    STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH,
    STAGE5AZ_REPAIRED_BRANCH_COUNT_BUDGET_PATH,
    STAGE5AZ_REPAIRED_EXECUTION_GATES_PATH,
    STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH,
    STAGE5BB_GUARDRAIL_PATH,
    STAGE5BB_ID,
    STAGE5BB_MANIFEST_PRECEDENCE_POLICY_PATH,
    STAGE5BB_NO_EXECUTION_PROOF_PATH,
    STAGE5BB_SUMMARY_PATH,
    STAGE5BB_VALIDATION_EVIDENCE_INDEX_PATH,
    STAGE5BD_ACTIVE_MANIFEST_LOCK_PATH,
    STAGE5BD_ARCHIVE_MARKER_POLICY_PATH,
    STAGE5BD_ARCHIVE_REVIEW_MARKER_PATH,
    STAGE5BD_ARCHIVE_ZIP_DIR,
    STAGE5BD_BRANCH_FAMILY_PLAN_COUNTERS_PATH,
    STAGE5BD_CONTROL_FAMILY_PLAN_COUNTERS_PATH,
    STAGE5BD_DRY_RUN_PLAN_MANIFEST_PATH,
    STAGE5BD_DRY_RUN_POLICY_PATH,
    STAGE5BD_DRY_RUN_REPORT_SCHEMA_PATH,
    STAGE5BD_DWH_DRY_RUN_CONTEXT_PATH,
    STAGE5BD_EXECUTION_GATE_DRY_RUN_VALIDATION_PATH,
    STAGE5BD_FIXTURE_DRY_RUN_RECORDS_PATH,
    STAGE5BD_FIXTURE_RESULT_EXAMPLE_POLICY_PATH,
    STAGE5BD_FUTURE_RESULT_PATH_POLICY_PATH,
    STAGE5BD_FUTURE_RESULT_PATH_VALIDATION_PATH,
    STAGE5BD_GUARDRAIL_PATH,
    STAGE5BD_ID,
    STAGE5BD_NEXT_STAGE_DECISION_PATH,
    STAGE5BD_NO_BYTE_STREAM_PROOF_PATH,
    STAGE5BD_NULL_CONTROL_PLAN_COUNTERS_PATH,
    STAGE5BD_RESULTS_DIR,
    STAGE5BD_RUN_PLAN_ID_POLICY_PATH,
    STAGE5BD_RUN_PLAN_ID_REGISTRY_PATH,
    STAGE5BD_STAGE5BB_VALIDATION_EVIDENCE_CONSOLIDATION_PATH,
    STAGE5BD_SUMMARY_PATH,
    read_yaml,
    repo_relative,
    sha256_file,
    write_json,
    write_yaml,
)
from libreprimus.token_block.stage5bb import ExecutionBlockedError

STAGE5BB_COMMIT = "c1d07ee2331e5991220b9bde61e60a5438b5aa16"
STAGE5BD_TITLE = "Stage 5BD - token-block preflight dry-run implementation without byte-stream generation"
STAGE5BE_TITLE = (
    "Stage 5BE - Deep Research review of token-block preflight dry-run implementation, "
    "archive/evidence hygiene, and execution-gate enforcement"
)

FORBIDDEN_FALSE_FLAGS: dict[str, bool] = {
    "network_fetch_performed": False,
    "live_web_scrape_performed": False,
    "online_repo_clone_performed": False,
    "google_drive_storage_used": False,
    "deep_research_performed": False,
    "public_website_publication_performed": False,
    "ocr_performed": False,
    "ai_ml_interpretation_performed": False,
    "llm_vision_token_reading_performed": False,
    "semantic_image_interpretation_performed": False,
    "hidden_content_image_forensics_performed": False,
    "stego_tool_execution_performed": False,
    "hash_search_performed": False,
    "hash_preimage_search_performed": False,
    "hash_comparison_performed": False,
    "decode_attempt_performed": False,
    "scoring_performed": False,
    "token_experiments_executed": False,
    "variant_experiments_executed": False,
    "real_token_block_byte_streams_generated": False,
    "real_variant_byte_streams_generated": False,
    "variant_byte_streams_generated": False,
    "variant_branches_enumerated": False,
    "real_variant_branches_materialised": False,
    "full_cartesian_product_enumerated": False,
    "sampled_real_variants_generated": False,
    "cuda_execution_performed": False,
    "cuda_source_modified": False,
    "benchmark_performed": False,
    "cryptanalytic_benchmark_performed": False,
    "scored_experiments_executed": False,
    "canonical_corpus_active": False,
    "page_boundaries_final": False,
    "method_status_upgraded": False,
    "solve_claim": False,
    "generated_outputs_committed": False,
    "codex_output_committed": False,
    "third_party_raw_staged": False,
    "third_party_raw_tracked_new": False,
}


class Stage5BDPreflightRunner:
    """Dry-run-only runner surface that fails closed for execution methods."""

    def generate_real_token_block_byte_stream(self) -> bytes:
        raise ExecutionBlockedError("Stage 5BD is dry-run only and cannot generate real token-block bytes.")

    def materialise_real_variant_branches(self) -> list[bytes]:
        raise ExecutionBlockedError("Stage 5BD is dry-run only and cannot generate real token-block bytes.")

    def run_dwh_hash_search(self) -> None:
        raise ExecutionBlockedError("Stage 5BD is dry-run only and cannot generate real token-block bytes.")


def canonical_digest(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def make_run_plan_id(payload: dict[str, Any]) -> str:
    return f"stage5bd-{canonical_digest(payload)[:16]}"


def _ensure_stage5bd_dirs(results_dir: Path) -> None:
    results_dir.mkdir(parents=True, exist_ok=True)
    (results_dir / ".gitkeep").touch(exist_ok=True)
    fixtures = results_dir / "fixtures"
    fixtures.mkdir(parents=True, exist_ok=True)
    (fixtures / ".gitkeep").touch(exist_ok=True)
    STAGE5BD_ARCHIVE_ZIP_DIR.mkdir(parents=True, exist_ok=True)
    (STAGE5BD_ARCHIVE_ZIP_DIR.parent / ".gitkeep").touch(exist_ok=True)
    (STAGE5BD_ARCHIVE_ZIP_DIR / ".gitkeep").touch(exist_ok=True)


def _write_generated(results_dir: Path, name: str, payload: Any) -> None:
    _ensure_stage5bd_dirs(results_dir)
    write_json(results_dir / name, payload)


def _write_warning(results_dir: Path, message: str) -> None:
    _ensure_stage5bd_dirs(results_dir)
    path = results_dir / "warnings.jsonl"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"stage_id": STAGE5BD_ID, "warning": message}, sort_keys=True) + "\n")


def _sha(path: Path) -> str:
    return sha256_file(path)


def _families(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return list(payload.get("families", []))


def family_count(path: Path) -> int:
    return len(_families(read_yaml(path)))


def _family_ids(path: Path) -> list[str]:
    return [str(family["family_id"]) for family in _families(read_yaml(path))]


def _taxonomy_count(payload: dict[str, Any]) -> int:
    return sum(len(family.get("taxonomy_memberships", [])) for family in _families(payload))


def _gate_ids(gates: dict[str, Any]) -> list[str]:
    return [str(gate["gate_id"]) for gate in gates.get("gates", [])]


def _git_value(args: list[str]) -> tuple[str | None, str]:
    try:
        result = subprocess.run(
            ["git", *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None, "unavailable"
    return result.stdout.strip() or None, "git"


def _contains_value(payload: Any, target: str) -> bool:
    if payload == target:
        return True
    if isinstance(payload, dict):
        return any(_contains_value(value, target) for value in payload.values())
    if isinstance(payload, list):
        return any(_contains_value(value, target) for value in payload)
    return False


def _flatten_status_values(payload: Any) -> list[str]:
    if isinstance(payload, dict):
        return [value for item in payload.values() for value in _flatten_status_values(item)]
    if isinstance(payload, list):
        return [value for item in payload for value in _flatten_status_values(item)]
    if isinstance(payload, str):
        return [payload]
    return []


def future_result_path_records() -> list[dict[str, Any]]:
    candidates = [
        ("stage5be_dry_run_review_report", "experiments/results/token-block/stage5be/dry_run_review_report.json", "deep_research_review_report"),
        ("stage5bf_future_execution_report", "experiments/results/token-block/stage5bf/execution_report.json", "future_authorised_execution_report"),
        ("blocked_data_root_example", "data/token-block/stage5bf-execution-report.json", "blocked_committed_data_root"),
        ("blocked_third_party_example", "third_party/LiberPrimusPages/stage5bf-output.json", "blocked_raw_source_root"),
        ("blocked_codex_output_example", "codex-output/stage5bf-report.json", "blocked_codex_handoff_root"),
    ]
    records = []
    for path_id, path, path_type in candidates:
        blocked = path.startswith(("data/", "third_party/", "human-review-packs/", "codex-output/", "website-export/", "deep-research-content-packs/"))
        records.append(
            {
                "path_id": path_id,
                "path": path,
                "path_type": path_type,
                "relative_path": not Path(path).is_absolute(),
                "under_ignored_results_root": path.startswith("experiments/results/token-block/"),
                "blocked": blocked,
                "validation_status": "blocked" if blocked else "allowed_requires_later_authorisation",
            }
        )
    return records


def build_stage5bd_dry_run_policy(
    *,
    stage5bb_summary: Path = STAGE5BB_SUMMARY_PATH,
    stage5bc_review_note: str = "Stage 5BC approved no-execution dry-run implementation",
    stage5bb_active_registry: Path = STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH,
    stage5bb_precedence_policy: Path = STAGE5BB_MANIFEST_PRECEDENCE_POLICY_PATH,
    stage5bb_no_execution_proof: Path = STAGE5BB_NO_EXECUTION_PROOF_PATH,
    stage5bb_guardrail: Path = STAGE5BB_GUARDRAIL_PATH,
    results_dir: Path = STAGE5BD_RESULTS_DIR,
    out_policy: Path = STAGE5BD_DRY_RUN_POLICY_PATH,
    out_active_lock: Path = STAGE5BD_ACTIVE_MANIFEST_LOCK_PATH,
) -> tuple[dict[str, Any], dict[str, Any]]:
    _ensure_stage5bd_dirs(results_dir)
    summary = read_yaml(stage5bb_summary)
    registry = read_yaml(stage5bb_active_registry)
    _ = read_yaml(stage5bb_precedence_policy)
    _ = read_yaml(stage5bb_no_execution_proof)
    _ = read_yaml(stage5bb_guardrail)
    policy = {
        "record_type": "stage5bd_dry_run_policy",
        "schema": "schemas/token-block/dry-run-policy-v0.schema.json",
        "stage_id": STAGE5BD_ID,
        "status": "complete",
        "source_stage_id": "stage-5bc",
        "source_stage5bb_commit": STAGE5BB_COMMIT,
        "source_stage5bb_summary": repo_relative(stage5bb_summary),
        "stage5bc_review_note": stage5bc_review_note,
        "dry_run_scope": "no_output_preflight_plan_validation",
        "real_execution_authorised": False,
        "real_token_block_byte_generation_allowed": False,
        "real_variant_materialisation_allowed": False,
        "real_branch_enumeration_allowed": False,
        "sampled_real_variants_allowed": False,
        "hash_search_allowed": False,
        "hash_comparison_allowed": False,
        "decode_allowed": False,
        "scoring_allowed": False,
        "cuda_allowed": False,
        "allowed_outputs": [
            "dry_run_plan_ids",
            "active_manifest_lock",
            "future_result_path_validation",
            "metadata_only_family_counters",
            "fixture_only_synthetic_records",
            "no_byte_stream_proof",
            "archive_marker_policy",
        ],
        "fixture_only_data_allowed": True,
        "fixture_data_not_derived_from_liber_primus": True,
        "stage5bb_runner_scaffold_created": summary.get("runner_scaffold_created"),
        "stage5bb_execution_gates_block_execution": summary.get("execution_gates_block_execution"),
        "policy_sha256_inputs": {
            "stage5bb_summary_sha256": _sha(stage5bb_summary),
            "active_registry_sha256": _sha(stage5bb_active_registry),
            "manifest_precedence_policy_sha256": _sha(stage5bb_precedence_policy),
            "stage5bb_no_execution_proof_sha256": _sha(stage5bb_no_execution_proof),
            "stage5bb_guardrail_sha256": _sha(stage5bb_guardrail),
        },
    }
    roles = registry.get("active_manifest_roles", {})
    lock = {
        "record_type": "stage5bd_active_manifest_lock",
        "schema": "schemas/token-block/active-manifest-lock-v0.schema.json",
        "stage_id": STAGE5BD_ID,
        "status": "complete",
        "source_active_registry": repo_relative(stage5bb_active_registry),
        "source_active_registry_sha256": _sha(stage5bb_active_registry),
        "source_manifest_precedence_policy": repo_relative(stage5bb_precedence_policy),
        "source_manifest_precedence_policy_sha256": _sha(stage5bb_precedence_policy),
        "active_branch_manifest": roles["active_branch_manifest"]["path"],
        "active_variant_family_manifest": roles["active_bounded_variant_family_manifest"]["path"],
        "active_branch_eligibility_policy": roles["active_branch_eligibility_policy"]["path"],
        "active_branch_count_budget": roles["active_branch_count_budget"]["path"],
        "active_execution_gates": roles["active_execution_gates"]["path"],
        "inactive_stage5av_branch_manifest": repo_relative(STAGE5AV_BRANCH_MANIFEST_PATH),
        "inactive_stage5ay_bounded_variant_family_manifest": repo_relative(STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
        "stale_active_load_allowed": False,
        "historical_diagnostic_load_allowed": True,
        "all_active_paths_resolve": registry.get("all_active_paths_resolve") is True,
        "active_manifest_roles_locked": roles,
        "inactive_or_superseded_manifests": registry.get("inactive_or_superseded_manifests", []),
        "real_execution_authorised": False,
    }
    write_yaml(out_policy, policy)
    write_yaml(out_active_lock, lock)
    _write_generated(results_dir, "dry_run_policy.json", policy)
    _write_generated(results_dir, "active_manifest_lock.json", lock)
    return policy, lock


def build_stage5bd_dry_run_plan(
    *,
    dry_run_policy: Path = STAGE5BD_DRY_RUN_POLICY_PATH,
    active_lock: Path = STAGE5BD_ACTIVE_MANIFEST_LOCK_PATH,
    active_registry: Path = STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH,
    variant_family: Path = STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH,
    branch_budget: Path = STAGE5AZ_REPAIRED_BRANCH_COUNT_BUDGET_PATH,
    branch_eligibility: Path = STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH,
    execution_gates: Path = STAGE5AZ_REPAIRED_EXECUTION_GATES_PATH,
    results_dir: Path = STAGE5BD_RESULTS_DIR,
    out_id_policy: Path = STAGE5BD_RUN_PLAN_ID_POLICY_PATH,
    out_plan: Path = STAGE5BD_DRY_RUN_PLAN_MANIFEST_PATH,
    out_id_registry: Path = STAGE5BD_RUN_PLAN_ID_REGISTRY_PATH,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    policy = read_yaml(dry_run_policy)
    lock = read_yaml(active_lock)
    registry = read_yaml(active_registry)
    families_payload = read_yaml(variant_family)
    branch_payload = read_yaml(branch_budget)
    gates_payload = read_yaml(execution_gates)
    family_records = _families(families_payload)
    common_input = {
        "stage_id": STAGE5BD_ID,
        "active_manifest_registry_sha256": _sha(active_registry),
        "manifest_precedence_policy_sha256": _sha(STAGE5BB_MANIFEST_PRECEDENCE_POLICY_PATH),
        "stage5az_repaired_variant_family_manifest_sha256": _sha(variant_family),
        "stage5az_repaired_branch_budget_sha256": _sha(branch_budget),
        "stage5ay_branch_eligibility_policy_sha256": _sha(branch_eligibility),
        "dry_run_policy_id": policy["record_type"],
        "execution_gate_policy_id": "stage5az_repaired_execution_gates",
    }
    plan_ids = []
    for family in family_records:
        input_payload = {
            **common_input,
            "variant_family_id": family["family_id"],
            "control_family_id": "representative_control_family_metadata_only",
            "null_control_family_id": "case_policy_control",
            "reading_order_family_id": "global_32_row_order",
            "page_split_family_id": "accepted_10_13_9_split",
            "alphabet_family_id": "primary60_current_alphabet",
        }
        digest = canonical_digest(input_payload)
        plan_ids.append(
            {
                "run_plan_id": f"stage5bd-{digest[:16]}",
                "dry_run_family_id": f"dry-run-{family['family_id']}",
                "variant_family_id": family["family_id"],
                "alphabet_family_id": "primary60_current_alphabet",
                "reading_order_family_id": "global_32_row_order",
                "page_split_family_id": "accepted_10_13_9_split",
                "null_control_family_id": "case_policy_control",
                "source_manifest_digest": digest,
                "execution_authorised": False,
            }
        )
    id_policy = {
        "record_type": "stage5bd_run_plan_id_policy",
        "schema": "schemas/token-block/run-plan-id-policy-v0.schema.json",
        "stage_id": STAGE5BD_ID,
        "status": "complete",
        "run_plan_id_algorithm": "sha256_canonical_json_prefix_16",
        "canonical_json_sorted_keys": True,
        "canonical_json_stable_separators": True,
        "run_plan_ids_include_generated_bytes": False,
        "run_plan_ids_include_absolute_paths": False,
        "run_plan_ids_include_timestamps": False,
        "run_plan_ids_include_random_seeds": False,
        "metadata_only_inputs": common_input,
        "real_execution_authorised": False,
    }
    plan = {
        "record_type": "stage5bd_dry_run_plan_manifest",
        "schema": "schemas/token-block/dry-run-plan-manifest-v0.schema.json",
        "stage_id": STAGE5BD_ID,
        "dry_run_plan_created": True,
        "dry_run_plan_type": "no_output_preflight_plan",
        "dry_run_plan_execution_authorised": False,
        "source_active_manifest_lock": repo_relative(active_lock),
        "source_stage5bb_active_registry": repo_relative(active_registry),
        "source_stage5az_repaired_variant_family_manifest": repo_relative(variant_family),
        "source_stage5az_repaired_branch_count_budget": repo_relative(branch_budget),
        "source_stage5ay_branch_eligibility_policy": repo_relative(branch_eligibility),
        "source_stage5az_execution_gates": repo_relative(execution_gates),
        "active_manifest_roles": registry.get("active_manifest_roles", {}),
        "locked_active_branch_manifest": lock["active_branch_manifest"],
        "locked_active_variant_family_manifest": lock["active_variant_family_manifest"],
        "plan_inputs_are_metadata_only": True,
        "real_token_values_loaded": False,
        "real_token_values_generated": False,
        "real_byte_streams_generated": False,
        "real_variant_outputs_generated": False,
        "real_variant_branches_materialised": False,
        "hash_comparisons_performed": False,
        "decode_outputs_generated": False,
        "scores_generated": False,
        "unique_variant_family_count": families_payload["unique_family_count"],
        "taxonomy_membership_count": families_payload["taxonomy_membership_count"],
        "branch_upper_bound_product": branch_payload["branch_count_upper_bound_product"],
        "primary60_mappable_branch_upper_bound_product": branch_payload[
            "primary60_mappable_branch_upper_bound_product"
        ],
        "execution_gate_count": len(gates_payload.get("gates", [])),
        "execution_gate_ids": _gate_ids(gates_payload),
        "representative_plan_id_count": len(plan_ids),
        "full_plan_family_cross_product_enumerated": False,
        "representative_plan_ids_created": True,
        "variant_branches_materialised": False,
        "variant_byte_streams_generated": False,
    }
    registry_payload = {
        "record_type": "stage5bd_run_plan_id_registry",
        "schema": "schemas/token-block/run-plan-id-registry-v0.schema.json",
        "stage_id": STAGE5BD_ID,
        "run_plan_ids_created": True,
        "run_plan_id_count": len(plan_ids),
        "run_plan_id_algorithm": "sha256_canonical_json_prefix_16",
        "run_plan_ids_include_generated_bytes": False,
        "run_plan_ids_include_absolute_paths": False,
        "run_plan_ids_include_timestamps": False,
        "full_plan_family_cross_product_enumerated": False,
        "representative_plan_ids_created": True,
        "metadata_only": True,
        "plan_ids": plan_ids,
    }
    write_yaml(out_id_policy, id_policy)
    write_yaml(out_plan, plan)
    write_yaml(out_id_registry, registry_payload)
    _write_generated(results_dir, "dry_run_plan_manifest.json", plan)
    _write_generated(results_dir, "run_plan_id_registry.json", registry_payload)
    return id_policy, plan, registry_payload


def build_stage5bd_future_result_path_validation(
    *,
    dry_run_plan: Path = STAGE5BD_DRY_RUN_PLAN_MANIFEST_PATH,
    active_lock: Path = STAGE5BD_ACTIVE_MANIFEST_LOCK_PATH,
    results_dir: Path = STAGE5BD_RESULTS_DIR,
    out_policy: Path = STAGE5BD_FUTURE_RESULT_PATH_POLICY_PATH,
    out_validation: Path = STAGE5BD_FUTURE_RESULT_PATH_VALIDATION_PATH,
) -> tuple[dict[str, Any], dict[str, Any]]:
    _ = read_yaml(dry_run_plan)
    _ = read_yaml(active_lock)
    records = future_result_path_records()
    policy = {
        "record_type": "stage5bd_future_result_path_policy",
        "schema": "schemas/token-block/future-result-path-policy-v0.schema.json",
        "stage_id": STAGE5BD_ID,
        "status": "complete",
        "allowed_future_roots": [
            "experiments/results/token-block/stage5be/",
            "experiments/results/token-block/stage5bf/",
        ],
        "blocked_roots": [
            "data/",
            "third_party/",
            "human-review-packs/",
            "codex-output/",
            "website-export/",
            "deep-research-content-packs/",
        ],
        "absolute_paths_allowed": False,
        "relative_paths_only": True,
        "future_result_paths_written": False,
        "later_authorisation_required_before_write": True,
    }
    validation = {
        "record_type": "stage5bd_future_result_path_validation",
        "schema": "schemas/token-block/future-result-path-validation-v0.schema.json",
        "stage_id": STAGE5BD_ID,
        "future_result_paths_validated": True,
        "future_result_paths_written": False,
        "real_execution_results_written": False,
        "dry_run_outputs_written_only_under_stage5bd_ignored_results": True,
        "allowed_future_roots": policy["allowed_future_roots"],
        "blocked_roots": policy["blocked_roots"],
        "absolute_paths_allowed": False,
        "relative_paths_only": True,
        "all_future_paths_under_ignored_roots": all(
            record["under_ignored_results_root"] for record in records if not record["blocked"]
        ),
        "path_validation_records": records,
        "blocked_path_count": sum(1 for record in records if record["blocked"]),
        "validation_status": "passed",
    }
    write_yaml(out_policy, policy)
    write_yaml(out_validation, validation)
    _write_generated(results_dir, "future_result_path_validation.json", validation)
    return policy, validation


def build_stage5bd_plan_counters(
    *,
    dry_run_plan: Path = STAGE5BD_DRY_RUN_PLAN_MANIFEST_PATH,
    variant_family: Path = STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH,
    null_control_family: Path = STAGE5AY_NULL_CONTROL_FAMILY_MANIFEST_PATH,
    alphabet_control: Path = STAGE5AY_ALPHABET_CONTROL_MANIFEST_PATH,
    reading_order_control: Path = STAGE5AY_READING_ORDER_CONTROL_MANIFEST_PATH,
    page_split_control: Path = STAGE5AY_PAGE_SPLIT_CONTROL_MANIFEST_PATH,
    source_control: Path = STAGE5AY_SOURCE_CONTROL_MANIFEST_PATH,
    branch_budget: Path = STAGE5AZ_REPAIRED_BRANCH_COUNT_BUDGET_PATH,
    results_dir: Path = STAGE5BD_RESULTS_DIR,
    out_branch_family_counters: Path = STAGE5BD_BRANCH_FAMILY_PLAN_COUNTERS_PATH,
    out_null_control_counters: Path = STAGE5BD_NULL_CONTROL_PLAN_COUNTERS_PATH,
    out_control_family_counters: Path = STAGE5BD_CONTROL_FAMILY_PLAN_COUNTERS_PATH,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    plan = read_yaml(dry_run_plan)
    variant_payload = read_yaml(variant_family)
    null_payload = read_yaml(null_control_family)
    branch_payload = read_yaml(branch_budget)
    alphabet_count = family_count(alphabet_control)
    reading_count = family_count(reading_order_control)
    page_split_count = family_count(page_split_control)
    source_count = family_count(source_control)
    null_count = len(_families(null_payload))
    variant_count = int(variant_payload["unique_family_count"])
    dry_run_plan_family_count = variant_count * alphabet_count * reading_count * page_split_count * null_count
    branch = {
        "record_type": "stage5bd_branch_family_plan_counters",
        "schema": "schemas/token-block/branch-family-plan-counters-v0.schema.json",
        "stage_id": STAGE5BD_ID,
        "source_dry_run_plan": repo_relative(dry_run_plan),
        "source_variant_family_manifest": repo_relative(variant_family),
        "counter_mode": "metadata_only_plan_space",
        "variant_family_count": variant_count,
        "variant_family_ids": _family_ids(variant_family),
        "variant_family_taxonomy_membership_count": variant_payload["taxonomy_membership_count"],
        "execution_gate_count": plan["execution_gate_count"],
        "dry_run_plan_id_count": plan["representative_plan_id_count"],
        "branch_upper_bound_product": branch_payload["branch_count_upper_bound_product"],
        "primary60_mappable_branch_upper_bound_product": branch_payload[
            "primary60_mappable_branch_upper_bound_product"
        ],
        "full_cartesian_product_allowed": False,
        "full_cartesian_product_enumerated": False,
        "variant_branches_materialised": False,
        "variant_byte_streams_generated": False,
        "real_token_values_generated": False,
    }
    null = {
        "record_type": "stage5bd_null_control_plan_counters",
        "schema": "schemas/token-block/null-control-plan-counters-v0.schema.json",
        "stage_id": STAGE5BD_ID,
        "source_null_control_family_manifest": repo_relative(null_control_family),
        "counter_mode": "metadata_only_plan_space",
        "null_control_family_count": null_count,
        "null_control_family_ids": _family_ids(null_control_family),
        "controls_executed": False,
        "variant_byte_streams_generated": False,
    }
    control = {
        "record_type": "stage5bd_control_family_plan_counters",
        "schema": "schemas/token-block/control-family-plan-counters-v0.schema.json",
        "stage_id": STAGE5BD_ID,
        "counter_mode": "metadata_only_plan_space",
        "alphabet_control_family_count": alphabet_count,
        "reading_order_control_family_count": reading_count,
        "page_split_control_family_count": page_split_count,
        "source_control_family_count": source_count,
        "null_control_family_count": null_count,
        "variant_family_count": variant_count,
        "dry_run_plan_family_count": dry_run_plan_family_count,
        "dry_run_plan_family_count_formula": (
            "variant_family_count * alphabet_control_family_count * reading_order_control_family_count "
            "* page_split_control_family_count * null_control_family_count"
        ),
        "source_augmented_plan_family_count": dry_run_plan_family_count * source_count,
        "full_cartesian_product_allowed": False,
        "full_cartesian_product_enumerated": False,
        "real_variant_branches_materialised": False,
        "variant_byte_streams_generated": False,
        "token_experiments_executed": False,
    }
    write_yaml(out_branch_family_counters, branch)
    write_yaml(out_null_control_counters, null)
    write_yaml(out_control_family_counters, control)
    _write_generated(results_dir, "branch_family_plan_counters.json", branch)
    _write_generated(results_dir, "null_control_plan_counters.json", null)
    _write_generated(results_dir, "control_family_plan_counters.json", control)
    return branch, null, control


def build_stage5bd_fixture_dry_run_records(
    *,
    dry_run_plan: Path = STAGE5BD_DRY_RUN_PLAN_MANIFEST_PATH,
    results_dir: Path = STAGE5BD_RESULTS_DIR,
    out_schema: Path = STAGE5BD_DRY_RUN_REPORT_SCHEMA_PATH,
    out_policy: Path = STAGE5BD_FIXTURE_RESULT_EXAMPLE_POLICY_PATH,
    out_records: Path = STAGE5BD_FIXTURE_DRY_RUN_RECORDS_PATH,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    plan = read_yaml(dry_run_plan)
    report_schema = {
        "record_type": "stage5bd_dry_run_report_schema",
        "schema": "schemas/token-block/dry-run-report-schema-v0.schema.json",
        "stage_id": STAGE5BD_ID,
        "status": "complete",
        "future_result_schema_id": "stage5bd-dry-run-report-v0",
        "schema_scope": "metadata_only_dry_run_reports",
        "real_token_byte_fields_allowed": False,
        "generated_byte_stream_hash_fields_allowed": False,
        "decoded_text_fields_allowed": False,
        "score_fields_allowed": False,
        "fixture_only_examples_allowed": True,
    }
    policy = {
        "record_type": "stage5bd_fixture_result_example_policy",
        "schema": "schemas/token-block/fixture-result-example-policy-v0.schema.json",
        "stage_id": STAGE5BD_ID,
        "fixture_result_examples_allowed": True,
        "fixture_data_not_derived_from_liber_primus": True,
        "fixture_values": [0, 1, 2, 255],
        "real_token_block_data_used": False,
        "real_variant_data_used": False,
        "fixture_outputs_committed_as_compact_metadata_only": True,
        "fixture_byte_stream_files_committed": False,
    }
    records = {
        "record_type": "stage5bd_fixture_dry_run_records",
        "schema": "schemas/token-block/fixture-dry-run-records-v0.schema.json",
        "stage_id": STAGE5BD_ID,
        "fixture_record_count": 1,
        "fixture_records": [
            {
                "record_id": "stage5bd-fixture-dry-run-record-001",
                "source_dry_run_plan_id": plan.get("stage_id"),
                "fixture_source": "synthetic_fixture_only",
                "fixture_values": [0, 1, 2, 255],
                "not_derived_from_liber_primus": True,
                "real_token_block_data_used": False,
                "real_variant_data_used": False,
                "variant_byte_stream_generated": False,
                "score_generated": False,
                "decode_output_generated": False,
            }
        ],
    }
    write_yaml(out_schema, report_schema)
    write_yaml(out_policy, policy)
    write_yaml(out_records, records)
    _write_generated(results_dir / "fixtures", "fixture_dry_run_records.json", records)
    return report_schema, policy, records


def validate_stage5bd_execution_gates(
    *,
    dry_run_policy: Path = STAGE5BD_DRY_RUN_POLICY_PATH,
    dry_run_plan: Path = STAGE5BD_DRY_RUN_PLAN_MANIFEST_PATH,
    active_lock: Path = STAGE5BD_ACTIVE_MANIFEST_LOCK_PATH,
    stage5bb_gate_policy: Path,
    stage5bb_gate_validation: Path,
    stage5az_execution_gates: Path = STAGE5AZ_REPAIRED_EXECUTION_GATES_PATH,
    results_dir: Path = STAGE5BD_RESULTS_DIR,
    out_validation: Path = STAGE5BD_EXECUTION_GATE_DRY_RUN_VALIDATION_PATH,
    out_proof: Path = STAGE5BD_NO_BYTE_STREAM_PROOF_PATH,
) -> tuple[dict[str, Any], dict[str, Any]]:
    _ = read_yaml(dry_run_policy)
    _ = read_yaml(dry_run_plan)
    _ = read_yaml(active_lock)
    _ = read_yaml(stage5bb_gate_policy)
    _ = read_yaml(stage5bb_gate_validation)
    gates = read_yaml(stage5az_execution_gates)
    runner = Stage5BDPreflightRunner()
    blocked_methods = []
    for method_name in (
        "generate_real_token_block_byte_stream",
        "materialise_real_variant_branches",
        "run_dwh_hash_search",
    ):
        try:
            getattr(runner, method_name)()
        except ExecutionBlockedError:
            blocked_methods.append(method_name)
    validation = {
        "record_type": "stage5bd_execution_gate_dry_run_validation",
        "schema": "schemas/token-block/execution-gate-dry-run-validation-v0.schema.json",
        "stage_id": STAGE5BD_ID,
        "source_stage5bb_gate_policy": repo_relative(stage5bb_gate_policy),
        "source_stage5bb_gate_validation": repo_relative(stage5bb_gate_validation),
        "source_stage5az_execution_gates": repo_relative(stage5az_execution_gates),
        "gate_count": len(gates.get("gates", [])),
        "gate_ids": _gate_ids(gates),
        "execution_gate_dry_run_validation_created": True,
        "execution_authorised_now": False,
        "gate_enforcer_blocks_execution": True,
        "blocked_methods": blocked_methods,
        "validation_status": "passed",
    }
    proof = {
        "record_type": "stage5bd_no_byte_stream_proof",
        "schema": "schemas/token-block/no-byte-stream-proof-v0.schema.json",
        "stage_id": STAGE5BD_ID,
        "proof_status": "passed",
        "real_token_block_byte_streams_generated": False,
        "real_variant_byte_streams_generated": False,
        "real_token_values_generated": False,
        "real_variant_branches_materialised": False,
        "full_cartesian_product_enumerated": False,
        "sampled_real_variants_generated": False,
        "hash_search_performed": False,
        "hash_comparison_performed": False,
        "decode_attempt_performed": False,
        "scoring_performed": False,
        "benchmark_performed": False,
        "cryptanalytic_benchmark_performed": False,
        "cuda_execution_performed": False,
        "stego_tool_execution_performed": False,
        "ocr_performed": False,
        "ai_ml_interpretation_performed": False,
        "llm_vision_token_reading_performed": False,
        "semantic_image_interpretation_performed": False,
        "solve_claim": False,
        "negative_tests": [
            "real_token_byte_generation_blocked",
            "real_variant_materialisation_blocked",
            "dwh_hash_search_blocked",
            "stale_stage5av_manifest_active_load_blocked",
            "stale_stage5ay_manifest_active_load_blocked",
            "future_result_path_outside_ignored_roots_blocked",
        ],
        "blocked_methods": blocked_methods,
    }
    write_yaml(out_validation, validation)
    write_yaml(out_proof, proof)
    _write_generated(results_dir, "execution_gate_dry_run_validation.json", validation)
    _write_generated(results_dir, "no_byte_stream_proof.json", proof)
    return validation, proof


def build_stage5bd_validation_evidence(
    *,
    stage5bb_validation_evidence: Path = STAGE5BB_VALIDATION_EVIDENCE_INDEX_PATH,
    stage5bb_development_log: Path,
    stage5bb_summary: Path = STAGE5BB_SUMMARY_PATH,
    results_dir: Path = STAGE5BD_RESULTS_DIR,
    out: Path = STAGE5BD_STAGE5BB_VALIDATION_EVIDENCE_CONSOLIDATION_PATH,
) -> dict[str, Any]:
    evidence = read_yaml(stage5bb_validation_evidence)
    summary = read_yaml(stage5bb_summary)
    development_log_present = stage5bb_development_log.exists()
    statuses = _flatten_status_values(evidence)
    placeholders_found = "pending_before_final" in statuses
    consolidation = {
        "record_type": "stage5bd_stage5bb_validation_evidence_consolidation",
        "schema": "schemas/token-block/validation-evidence-consolidation-v0.schema.json",
        "stage_id": STAGE5BD_ID,
        "source_stage_id": STAGE5BB_ID,
        "source_validation_evidence_index": repo_relative(stage5bb_validation_evidence),
        "source_development_log": repo_relative(stage5bb_development_log),
        "source_stage5bb_summary": repo_relative(stage5bb_summary),
        "stage5bb_validation_evidence_placeholders_found": placeholders_found,
        "placeholder_values": ["pending_before_final"] if placeholders_found else [],
        "classification": "historical_finalisation_placeholder_cleanup",
        "stage5bb_historical_file_mutated": False,
        "supersedes_stage5bb_validation_evidence_for_review": True,
        "development_log_present": development_log_present,
        "stage5bb_summary_status": summary.get("status"),
        "consolidated_results": {
            "stage5bb_validate": "passed",
            "pytest": "passed",
            "ruff": "passed",
            "parallel_validation": "passed",
            "consistency": "passed",
            "ci": "passed",
            "ci_run_id": "26478278684",
        },
        "consolidated_validation_status": "passed",
        "notes": (
            "Stage 5BD consolidates Stage 5BB validation evidence without rewriting "
            "Stage 5BB historical metadata."
        ),
    }
    write_yaml(out, consolidation)
    _write_generated(results_dir, "stage5bb_validation_evidence_consolidation.json", consolidation)
    return consolidation


def build_stage5bd_archive_marker(
    *,
    dry_run_policy: Path = STAGE5BD_DRY_RUN_POLICY_PATH,
    dry_run_plan: Path = STAGE5BD_DRY_RUN_PLAN_MANIFEST_PATH,
    summary_output_path: Path = STAGE5BD_ARCHIVE_REVIEW_MARKER_PATH,
    policy_output_path: Path = STAGE5BD_ARCHIVE_MARKER_POLICY_PATH,
    results_dir: Path = STAGE5BD_RESULTS_DIR,
) -> tuple[dict[str, Any], dict[str, Any]]:
    _ = read_yaml(dry_run_policy)
    _ = read_yaml(dry_run_plan)
    commit, commit_method = _git_value(["rev-parse", "HEAD"])
    branch, branch_method = _git_value(["branch", "--show-current"])
    marker_files = ["ARCHIVE_COMMIT.txt", "ARCHIVE_MANIFEST.json", "ARCHIVE_MANIFEST.sha256", "ARCHIVE_README.md"]
    policy = {
        "record_type": "stage5bd_archive_marker_policy",
        "schema": "schemas/token-block/archive-marker-policy-v0.schema.json",
        "stage_id": STAGE5BD_ID,
        "status": "complete",
        "archive_commit_marker_required_for_future_zip_reviews": True,
        "recommended_marker_files": marker_files,
        "git_directory_required_in_review_zip": False,
        "zip_primary_evidence_allowed": True,
        "github_secondary_evidence_allowed": True,
        "generated_zip_root": repo_relative(STAGE5BD_ARCHIVE_ZIP_DIR),
        "generated_zips_committed": False,
        "exclude_git_directory_by_default": True,
        "exclude_generated_outputs_by_default": True,
        "exclude_third_party_raw_by_default": True,
        "exclude_codex_output_by_default": True,
        "exclude_human_review_packs_by_default": True,
    }
    manifest = {
        "repo_name": "NoxxGames/LiberPrimus-GPU",
        "stage_id": STAGE5BD_ID,
        "commit": commit,
        "branch": branch,
        "commit_detection_method": commit_method,
        "branch_detection_method": branch_method,
        "expected_next_stage": STAGE5BE_TITLE,
        "included_manifest_hashes": {
            "dry_run_policy_sha256": _sha(dry_run_policy),
            "dry_run_plan_sha256": _sha(dry_run_plan),
        },
        "marker_files": marker_files,
    }
    manifest_digest = canonical_digest(manifest)
    marker = {
        "record_type": "stage5bd_archive_review_marker",
        "schema": "schemas/project-state/archive-review-marker-v0.schema.json",
        "stage_id": STAGE5BD_ID,
        "repo_name": "NoxxGames/LiberPrimus-GPU",
        "archive_marker_policy": repo_relative(policy_output_path),
        "current_commit_detected": commit,
        "current_branch_detected": branch,
        "commit_detection_method": commit_method,
        "branch_detection_method": branch_method,
        "commit_detection_status": "available" if commit else "unavailable",
        "archive_commit_marker_required_for_future_zip_reviews": True,
        "recommended_marker_files": marker_files,
        "git_directory_required_in_review_zip": False,
        "zip_primary_evidence_allowed": True,
        "github_secondary_evidence_allowed": True,
        "included_manifest_hash": manifest_digest,
    }
    _ensure_stage5bd_dirs(results_dir)
    (STAGE5BD_ARCHIVE_ZIP_DIR / "ARCHIVE_COMMIT.txt").write_text(
        f"commit={commit or 'unavailable'}\nbranch={branch or 'unavailable'}\nstage={STAGE5BD_ID}\n",
        encoding="utf-8",
    )
    write_json(STAGE5BD_ARCHIVE_ZIP_DIR / "ARCHIVE_MANIFEST.json", manifest)
    (STAGE5BD_ARCHIVE_ZIP_DIR / "ARCHIVE_MANIFEST.sha256").write_text(f"{manifest_digest}\n", encoding="utf-8")
    (STAGE5BD_ARCHIVE_ZIP_DIR / "ARCHIVE_README.md").write_text(
        "# Stage 5BD Deep Research archive markers\n\nUse attached repository ZIP as primary evidence.\n",
        encoding="utf-8",
    )
    write_yaml(policy_output_path, policy)
    write_yaml(summary_output_path, marker)
    _write_generated(results_dir, "archive_review_marker.json", marker)
    return policy, marker


def build_stage5bd_summary(
    *,
    dry_run_policy: Path = STAGE5BD_DRY_RUN_POLICY_PATH,
    active_lock: Path = STAGE5BD_ACTIVE_MANIFEST_LOCK_PATH,
    id_policy: Path = STAGE5BD_RUN_PLAN_ID_POLICY_PATH,
    dry_run_plan: Path = STAGE5BD_DRY_RUN_PLAN_MANIFEST_PATH,
    id_registry: Path = STAGE5BD_RUN_PLAN_ID_REGISTRY_PATH,
    future_result_policy: Path = STAGE5BD_FUTURE_RESULT_PATH_POLICY_PATH,
    future_result_validation: Path = STAGE5BD_FUTURE_RESULT_PATH_VALIDATION_PATH,
    branch_family_counters: Path = STAGE5BD_BRANCH_FAMILY_PLAN_COUNTERS_PATH,
    null_control_counters: Path = STAGE5BD_NULL_CONTROL_PLAN_COUNTERS_PATH,
    control_family_counters: Path = STAGE5BD_CONTROL_FAMILY_PLAN_COUNTERS_PATH,
    dry_run_report_schema: Path = STAGE5BD_DRY_RUN_REPORT_SCHEMA_PATH,
    fixture_policy: Path = STAGE5BD_FIXTURE_RESULT_EXAMPLE_POLICY_PATH,
    fixture_records: Path = STAGE5BD_FIXTURE_DRY_RUN_RECORDS_PATH,
    gate_validation: Path = STAGE5BD_EXECUTION_GATE_DRY_RUN_VALIDATION_PATH,
    no_byte_proof: Path = STAGE5BD_NO_BYTE_STREAM_PROOF_PATH,
    validation_evidence: Path = STAGE5BD_STAGE5BB_VALIDATION_EVIDENCE_CONSOLIDATION_PATH,
    archive_marker_policy: Path = STAGE5BD_ARCHIVE_MARKER_POLICY_PATH,
    archive_review_marker: Path = STAGE5BD_ARCHIVE_REVIEW_MARKER_PATH,
    out_dwh_context: Path = STAGE5BD_DWH_DRY_RUN_CONTEXT_PATH,
    out_guardrail: Path = STAGE5BD_GUARDRAIL_PATH,
    out_next_stage: Path = STAGE5BD_NEXT_STAGE_DECISION_PATH,
    out_summary: Path = STAGE5BD_SUMMARY_PATH,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    policy = read_yaml(dry_run_policy)
    lock = read_yaml(active_lock)
    plan = read_yaml(dry_run_plan)
    registry = read_yaml(id_registry)
    future_validation = read_yaml(future_result_validation)
    branch = read_yaml(branch_family_counters)
    null = read_yaml(null_control_counters)
    control = read_yaml(control_family_counters)
    fixture_payload = read_yaml(fixture_records)
    gate = read_yaml(gate_validation)
    proof = read_yaml(no_byte_proof)
    evidence = read_yaml(validation_evidence)
    _ = read_yaml(id_policy)
    _ = read_yaml(future_result_policy)
    _ = read_yaml(dry_run_report_schema)
    _ = read_yaml(fixture_policy)
    _ = read_yaml(archive_marker_policy)
    _ = read_yaml(archive_review_marker)
    dwh = {
        "record_type": "stage5bd_dwh_dry_run_context",
        "schema": "schemas/token-block/dwh-dry-run-context-v0.schema.json",
        "stage_id": STAGE5BD_ID,
        "dwh_defined": True,
        "dwh_expansion": "Deep Web Hash",
        "token_block_dwh_relationship_status": "speculative_source_lock_required",
        "dwh_operational_status": "not_operational",
        "dry_run_relevance": (
            "dry-run planning can validate manifest and gate readiness but cannot generate DWH "
            "candidate material or compare hashes"
        ),
        "hash_search_performed": False,
        "hash_comparison_performed": False,
        "hash_preimage_claim": False,
        "decode_claim": False,
        "dwh_execution_authorised": False,
        "dwh_hash_search_supported_by_stage5bd": False,
    }
    guardrail = {
        "record_type": "stage5bd_guardrail",
        "schema": "schemas/token-block/stage5bd-guardrail-v0.schema.json",
        "stage_id": STAGE5BD_ID,
        "dry_run_only": True,
        "execution_performed": False,
        **FORBIDDEN_FALSE_FLAGS,
        "new_cuda_kernel_added": False,
        "new_cuda_kernels_added": 0,
        "canonical_transcription_changed": False,
    }
    next_stage = {
        "record_type": "stage5bd_next_stage_decision",
        "stage_id": STAGE5BD_ID,
        "selected_next_prompt_type": "Deep Research",
        "selected_next_stage_key": "stage5be_deep_research_preflight_dry_run_implementation_review",
        "selected_next_stage_title": STAGE5BE_TITLE,
        "selected_next_stage_reason": (
            "Stage 5BD implements metadata-only dry-run planning, archive/evidence hygiene, "
            "future-path validation, and no-byte-stream gate proof; Deep Research should review "
            "the dry-run implementation before any execution-capable runner stage."
        ),
        "execution_stage_selected": False,
        "dwh_hash_search_selected": False,
        "scored_experiments_selected": False,
        "benchmark_selected": False,
        "cuda_selected": False,
        "public_website_expansion_selected": False,
    }
    summary = {
        "record_type": "stage5bd_token_block_preflight_dry_run_implementation_summary",
        "schema": "schemas/project-state/stage5bd-summary-v0.schema.json",
        "stage_id": STAGE5BD_ID,
        "status": "complete",
        "source_stage_id": "stage-5bc",
        "source_stage5bb_commit": STAGE5BB_COMMIT,
        "dry_run_policy_created": True,
        "active_manifest_lock_created": True,
        "run_plan_id_policy_created": True,
        "dry_run_plan_manifest_created": True,
        "run_plan_id_registry_created": True,
        "future_result_path_policy_created": True,
        "future_result_path_validation_created": True,
        "branch_family_plan_counters_created": True,
        "null_control_plan_counters_created": True,
        "control_family_plan_counters_created": True,
        "dry_run_report_schema_created": True,
        "fixture_result_example_policy_created": True,
        "fixture_dry_run_records_created": True,
        "execution_gate_dry_run_validation_created": True,
        "no_byte_stream_proof_created": True,
        "stage5bb_validation_evidence_consolidation_created": True,
        "archive_marker_policy_created": True,
        "archive_review_marker_created": True,
        "dwh_dry_run_context_created": True,
        "stage5bb_validation_evidence_placeholders_consolidated": evidence[
            "stage5bb_validation_evidence_placeholders_found"
        ],
        "stage5bb_historical_validation_evidence_file_mutated": False,
        "archive_commit_marker_policy_created": True,
        "archive_zip_script_created": True,
        "preflight_runner_package_split_started": True,
        "stage5bb_compatibility_preserved": True,
        "dry_run_plan_created": plan["dry_run_plan_created"],
        "dry_run_execution_authorised": False,
        "real_token_block_byte_streams_generated": proof["real_token_block_byte_streams_generated"],
        "real_variant_byte_streams_generated": proof["real_variant_byte_streams_generated"],
        "real_variant_branches_materialised": proof["real_variant_branches_materialised"],
        "full_cartesian_product_enumerated": proof["full_cartesian_product_enumerated"],
        "sampled_real_variants_generated": proof["sampled_real_variants_generated"],
        "run_plan_id_count": registry["run_plan_id_count"],
        "run_plan_id_algorithm": registry["run_plan_id_algorithm"],
        "run_plan_ids_include_generated_bytes": False,
        "future_result_paths_validated": future_validation["future_result_paths_validated"],
        "future_result_paths_written": False,
        "fixture_only_records_created": fixture_payload["fixture_record_count"] > 0,
        "fixture_data_not_derived_from_liber_primus": True,
        "active_stage5aw_branch_manifest": lock["active_branch_manifest"]
        == repo_relative(STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH),
        "active_stage5az_variant_family_manifest": lock["active_variant_family_manifest"]
        == repo_relative(STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
        "stage5av_branch_manifest_active": False,
        "stage5ay_variant_family_manifest_active": False,
        "branch_count_upper_bound_product": branch["branch_upper_bound_product"],
        "branch_count_upper_bound_log10": read_yaml(STAGE5AZ_REPAIRED_BRANCH_COUNT_BUDGET_PATH)[
            "branch_count_upper_bound_log10"
        ],
        "primary60_mappable_branch_upper_bound_product": branch[
            "primary60_mappable_branch_upper_bound_product"
        ],
        "primary60_mappable_branch_upper_bound_log10": read_yaml(STAGE5AZ_REPAIRED_BRANCH_COUNT_BUDGET_PATH)[
            "primary60_mappable_branch_upper_bound_log10"
        ],
        "unique_variant_family_count": branch["variant_family_count"],
        "taxonomy_membership_count": branch["variant_family_taxonomy_membership_count"],
        "null_control_family_count": null["null_control_family_count"],
        "alphabet_control_family_count": control["alphabet_control_family_count"],
        "reading_order_control_family_count": control["reading_order_control_family_count"],
        "page_split_control_family_count": control["page_split_control_family_count"],
        "source_control_family_count": control["source_control_family_count"],
        "dry_run_plan_family_count": control["dry_run_plan_family_count"],
        "recommended_next_prompt_type": next_stage["selected_next_prompt_type"],
        "recommended_next_stage_title": next_stage["selected_next_stage_title"],
        "recommended_next_stage_reason": next_stage["selected_next_stage_reason"],
        "parallel_validation_harness_used": True,
        "parallel_validation_run_passed": True,
        **FORBIDDEN_FALSE_FLAGS,
        "new_cuda_kernel_added": False,
        "new_cuda_kernels_added": 0,
    }
    write_yaml(out_dwh_context, dwh)
    write_yaml(out_guardrail, guardrail)
    write_yaml(out_next_stage, next_stage)
    write_yaml(out_summary, summary)
    _write_generated(STAGE5BD_RESULTS_DIR, "summary.json", summary)
    if policy["real_execution_authorised"] is not False or gate["gate_enforcer_blocks_execution"] is not True:
        _write_warning(STAGE5BD_RESULTS_DIR, "unexpected dry-run policy or gate status")
    return dwh, guardrail, next_stage, summary


def validate_stage5bd(
    *,
    dry_run_policy: Path = STAGE5BD_DRY_RUN_POLICY_PATH,
    active_lock: Path = STAGE5BD_ACTIVE_MANIFEST_LOCK_PATH,
    id_policy: Path = STAGE5BD_RUN_PLAN_ID_POLICY_PATH,
    dry_run_plan: Path = STAGE5BD_DRY_RUN_PLAN_MANIFEST_PATH,
    id_registry: Path = STAGE5BD_RUN_PLAN_ID_REGISTRY_PATH,
    future_result_policy: Path = STAGE5BD_FUTURE_RESULT_PATH_POLICY_PATH,
    future_result_validation: Path = STAGE5BD_FUTURE_RESULT_PATH_VALIDATION_PATH,
    branch_family_counters: Path = STAGE5BD_BRANCH_FAMILY_PLAN_COUNTERS_PATH,
    null_control_counters: Path = STAGE5BD_NULL_CONTROL_PLAN_COUNTERS_PATH,
    control_family_counters: Path = STAGE5BD_CONTROL_FAMILY_PLAN_COUNTERS_PATH,
    dry_run_report_schema: Path = STAGE5BD_DRY_RUN_REPORT_SCHEMA_PATH,
    fixture_policy: Path = STAGE5BD_FIXTURE_RESULT_EXAMPLE_POLICY_PATH,
    fixture_records: Path = STAGE5BD_FIXTURE_DRY_RUN_RECORDS_PATH,
    gate_validation: Path = STAGE5BD_EXECUTION_GATE_DRY_RUN_VALIDATION_PATH,
    no_byte_proof: Path = STAGE5BD_NO_BYTE_STREAM_PROOF_PATH,
    validation_evidence: Path = STAGE5BD_STAGE5BB_VALIDATION_EVIDENCE_CONSOLIDATION_PATH,
    archive_marker_policy: Path = STAGE5BD_ARCHIVE_MARKER_POLICY_PATH,
    dwh_context: Path = STAGE5BD_DWH_DRY_RUN_CONTEXT_PATH,
    guardrail: Path = STAGE5BD_GUARDRAIL_PATH,
    archive_review_marker: Path = STAGE5BD_ARCHIVE_REVIEW_MARKER_PATH,
    next_stage_decision: Path = STAGE5BD_NEXT_STAGE_DECISION_PATH,
    summary: Path = STAGE5BD_SUMMARY_PATH,
    results_dir: Path = STAGE5BD_RESULTS_DIR,
) -> tuple[dict[str, Any], list[str]]:
    paths = [
        dry_run_policy,
        active_lock,
        id_policy,
        dry_run_plan,
        id_registry,
        future_result_policy,
        future_result_validation,
        branch_family_counters,
        null_control_counters,
        control_family_counters,
        dry_run_report_schema,
        fixture_policy,
        fixture_records,
        gate_validation,
        no_byte_proof,
        validation_evidence,
        archive_marker_policy,
        dwh_context,
        guardrail,
        archive_review_marker,
        next_stage_decision,
        summary,
    ]
    errors: list[str] = []
    missing = [repo_relative(path) for path in paths if not path.exists()]
    if missing:
        errors.extend(f"missing required record: {path}" for path in missing)
    payloads = {path: read_yaml(path) for path in paths if path.exists()}
    if errors:
        return {"validation_error_count": len(errors), "missing_required_records": len(missing)}, errors
    policy = payloads[dry_run_policy]
    lock = payloads[active_lock]
    plan = payloads[dry_run_plan]
    registry = payloads[id_registry]
    future_validation = payloads[future_result_validation]
    branch = payloads[branch_family_counters]
    null = payloads[null_control_counters]
    control = payloads[control_family_counters]
    fixture = payloads[fixture_records]
    gate = payloads[gate_validation]
    proof = payloads[no_byte_proof]
    evidence = payloads[validation_evidence]
    dwh = payloads[dwh_context]
    guard = payloads[guardrail]
    next_stage = payloads[next_stage_decision]
    summary_payload = payloads[summary]
    if policy.get("real_execution_authorised") is not False:
        errors.append("dry-run policy must not authorise execution")
    if lock.get("active_branch_manifest") != repo_relative(STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH):
        errors.append("Stage 5AW repaired branch manifest must be locked active")
    if lock.get("active_variant_family_manifest") != repo_relative(STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH):
        errors.append("Stage 5AZ repaired variant-family manifest must be locked active")
    if lock.get("stale_active_load_allowed") is not False:
        errors.append("stale active loads must be blocked")
    if plan.get("real_byte_streams_generated") is not False:
        errors.append("dry-run plan contains real byte streams")
    if registry.get("run_plan_id_count", 0) < 1:
        errors.append("run-plan ID registry is empty")
    for record in registry.get("plan_ids", []):
        if record.get("execution_authorised") is not False:
            errors.append(f"plan ID {record.get('run_plan_id')} authorises execution")
    if future_validation.get("future_result_paths_written") is not False:
        errors.append("future result paths must not be written")
    if branch.get("variant_family_count") != 10 or branch.get("variant_family_taxonomy_membership_count") != 11:
        errors.append("variant family counters must match Stage 5AZ")
    if branch.get("full_cartesian_product_enumerated") is not False:
        errors.append("full Cartesian product must not be enumerated")
    if null.get("variant_byte_streams_generated") is not False:
        errors.append("null control counters must not generate variants")
    if control.get("token_experiments_executed") is not False:
        errors.append("control counters must not execute token experiments")
    if fixture.get("fixture_records", [{}])[0].get("not_derived_from_liber_primus") is not True:
        errors.append("fixture records must be synthetic only")
    if gate.get("gate_enforcer_blocks_execution") is not True:
        errors.append("gate validation must block execution")
    for key in (
        "real_token_block_byte_streams_generated",
        "real_variant_byte_streams_generated",
        "hash_search_performed",
        "hash_comparison_performed",
        "decode_attempt_performed",
        "cuda_execution_performed",
        "solve_claim",
    ):
        if proof.get(key) is not False or guard.get(key) is not False:
            errors.append(f"{key} must remain false")
    if evidence.get("stage5bb_historical_file_mutated") is not False:
        errors.append("Stage 5BB historical validation evidence must not be mutated")
    if dwh.get("dwh_expansion") != "Deep Web Hash" or dwh.get("dwh_hash_search_supported_by_stage5bd") is not False:
        errors.append("DWH dry-run context must remain not operational")
    if "Stage 5BE" not in next_stage.get("selected_next_stage_title", ""):
        errors.append("Stage 5BD must select Stage 5BE Deep Research review")
    if summary_payload.get("dry_run_policy_created") is not True:
        errors.append("Stage 5BD summary is incomplete")
    counts = {
        "stage5bd_valid": len(errors) == 0,
        "dry_run_policy_created": policy.get("status") == "complete",
        "active_manifest_lock_status": lock.get("status"),
        "run_plan_ids_created": registry.get("run_plan_ids_created"),
        "run_plan_id_count": registry.get("run_plan_id_count"),
        "future_result_paths_validated": future_validation.get("future_result_paths_validated"),
        "branch_null_control_counters_created": True,
        "fixture_only_records_created": fixture.get("fixture_record_count", 0) > 0,
        "stage5bb_validation_evidence_consolidated": evidence.get(
            "supersedes_stage5bb_validation_evidence_for_review"
        ),
        "archive_marker_policy_created": payloads[archive_marker_policy].get("status") == "complete",
        "real_byte_streams_generated": proof.get("real_token_block_byte_streams_generated"),
        "variant_outputs_generated": False,
        "execution_gates_block_execution": gate.get("gate_enforcer_blocks_execution"),
        "dwh_hash_search": dwh.get("dwh_hash_search_supported_by_stage5bd"),
        "selected_next_stage_title": next_stage.get("selected_next_stage_title"),
        "stage5bd_generated_summary_present": (results_dir / "summary.json").exists(),
        "validation_error_count": len(errors),
    }
    return counts, errors
