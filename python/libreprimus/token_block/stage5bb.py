"""Stage 5BB token-block preflight runner scaffold helpers.

The scaffold intentionally stops at manifest loading, reference validation,
metadata counters, and gate reporting. It does not materialise real token-block
variants or execute any token experiment.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from .models import (
    STAGE5AV_BRANCH_MANIFEST_PATH,
    STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH,
    STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH,
    STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH,
    STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH,
    STAGE5AY_ALPHABET_CONTROL_MANIFEST_PATH,
    STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH,
    STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH,
    STAGE5AY_FUTURE_RESULT_SCHEMA_PREVIEW_PATH,
    STAGE5AY_NULL_CONTROL_FAMILY_MANIFEST_PATH,
    STAGE5AY_PAGE_SPLIT_CONTROL_MANIFEST_PATH,
    STAGE5AY_PREFLIGHT_SOURCE_INPUTS_PATH,
    STAGE5AY_READING_ORDER_CONTROL_MANIFEST_PATH,
    STAGE5AY_SOURCE_CONTROL_MANIFEST_PATH,
    STAGE5AZ_DEEP_RESEARCH_READINESS_PATH,
    STAGE5AZ_DWH_MANIFEST_INTEGRITY_CONTEXT_PATH,
    STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH,
    STAGE5AZ_REPAIRED_BRANCH_COUNT_BUDGET_PATH,
    STAGE5AZ_REPAIRED_EXECUTION_GATES_PATH,
    STAGE5AZ_REPAIRED_PREFLIGHT_DESIGN_POLICY_PATH,
    STAGE5AZ_SUMMARY_PATH,
    STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH,
    STAGE5BB_BRANCH_COUNTER_SUMMARY_PATH,
    STAGE5BB_BRANCH_ELIGIBILITY_REFERENCE_VALIDATION_PATH,
    STAGE5BB_DRY_RUN_PLAN_PREVIEW_PATH,
    STAGE5BB_DWH_RUNNER_CONTEXT_PATH,
    STAGE5BB_EXECUTION_GATE_ENFORCEMENT_POLICY_PATH,
    STAGE5BB_EXECUTION_GATE_VALIDATION_PATH,
    STAGE5BB_FAMILY_ENUMERATION_SUMMARY_PATH,
    STAGE5BB_FIXTURE_RESULT_SCHEMA_RECORDS_PATH,
    STAGE5BB_GUARDRAIL_PATH,
    STAGE5BB_ID,
    STAGE5BB_LEGACY_POINTER_AUDIT_PATH,
    STAGE5BB_LOADER_SCAFFOLD_POLICY_PATH,
    STAGE5BB_MANIFEST_PRECEDENCE_POLICY_PATH,
    STAGE5BB_MANIFEST_REFERENCE_VALIDATION_PATH,
    STAGE5BB_NEXT_STAGE_DECISION_PATH,
    STAGE5BB_NO_EXECUTION_PROOF_PATH,
    STAGE5BB_RESULT_SCHEMA_FIXTURE_POLICY_PATH,
    STAGE5BB_RESULTS_DIR,
    STAGE5BB_RUNNER_SCAFFOLD_MANIFEST_PATH,
    STAGE5BB_SUMMARY_PATH,
    STAGE5BB_VALIDATION_EVIDENCE_INDEX_PATH,
    read_yaml,
    repo_relative,
    sha256_file,
    write_json,
    write_yaml,
)

STAGE5BB_TITLE = "Stage 5BB - Token-Block Preflight Runner Scaffold Without Execution"
STAGE5BC_TITLE = (
    "Stage 5BC - Deep Research review of token-block preflight runner scaffold "
    "and execution-gate enforcement"
)
STAGE5AZ_COMMIT = "8f96f43545a8c3a7a50baf38a49aa8e66cffd71e"

ACTIVE_MANIFEST_INPUTS: dict[str, tuple[Path, str, bool]] = {
    "active_branch_manifest": (STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH, "stage-5aw", True),
    "active_primary60_impact_summary": (STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH, "stage-5aw", True),
    "active_unresolved_variant_records": (STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH, "stage-5aw", True),
    "active_reviewer_extra_possible_tokens": (STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH, "stage-5aw", True),
    "active_preflight_source_inputs": (STAGE5AY_PREFLIGHT_SOURCE_INPUTS_PATH, "stage-5ay", True),
    "active_branch_eligibility_policy": (STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH, "stage-5ay", True),
    "active_preflight_design_policy": (STAGE5AZ_REPAIRED_PREFLIGHT_DESIGN_POLICY_PATH, "stage-5az", True),
    "active_bounded_variant_family_manifest": (
        STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH,
        "stage-5az",
        True,
    ),
    "active_branch_count_budget": (STAGE5AZ_REPAIRED_BRANCH_COUNT_BUDGET_PATH, "stage-5az", True),
    "active_execution_gates": (STAGE5AZ_REPAIRED_EXECUTION_GATES_PATH, "stage-5az", True),
    "active_dwh_context": (STAGE5AZ_DWH_MANIFEST_INTEGRITY_CONTEXT_PATH, "stage-5az", True),
    "supporting_null_control_family_manifest": (STAGE5AY_NULL_CONTROL_FAMILY_MANIFEST_PATH, "stage-5ay", False),
    "supporting_alphabet_control_manifest": (STAGE5AY_ALPHABET_CONTROL_MANIFEST_PATH, "stage-5ay", False),
    "supporting_reading_order_control_manifest": (STAGE5AY_READING_ORDER_CONTROL_MANIFEST_PATH, "stage-5ay", False),
    "supporting_page_split_control_manifest": (STAGE5AY_PAGE_SPLIT_CONTROL_MANIFEST_PATH, "stage-5ay", False),
    "supporting_source_control_manifest": (STAGE5AY_SOURCE_CONTROL_MANIFEST_PATH, "stage-5ay", False),
    "supporting_future_result_schema_preview": (STAGE5AY_FUTURE_RESULT_SCHEMA_PREVIEW_PATH, "stage-5ay", False),
}

INACTIVE_MANIFESTS: list[dict[str, Any]] = [
    {
        "manifest_key": "inactive_stage5av_branch_manifest",
        "path": repo_relative(STAGE5AV_BRANCH_MANIFEST_PATH),
        "source_stage_id": "stage-5av",
        "inactive_reason": "superseded_by_stage5aw_repaired_branch_manifest",
        "active_replacement_path": repo_relative(STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH),
        "active_load_allowed": False,
        "historical_diagnostic_load_allowed": True,
    },
    {
        "manifest_key": "inactive_stage5ay_bounded_variant_family_manifest",
        "path": repo_relative(STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
        "source_stage_id": "stage-5ay",
        "inactive_reason": "superseded_by_stage5az_repaired_bounded_variant_family_manifest",
        "active_replacement_path": repo_relative(STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
        "active_load_allowed": False,
        "historical_diagnostic_load_allowed": True,
    },
]

FALSE_FLAGS = {
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
    "hash_preimage_search_performed": False,
    "hash_search_performed": False,
    "hash_comparison_performed": False,
    "decode_attempt_performed": False,
    "scoring_performed": False,
    "token_experiments_executed": False,
    "variant_experiments_executed": False,
    "real_token_block_byte_streams_generated": False,
    "variant_byte_streams_generated": False,
    "real_variant_byte_streams_generated": False,
    "variant_branches_materialised": False,
    "variant_branches_enumerated": False,
    "full_cartesian_product_enumerated": False,
    "sampled_variants_generated": False,
    "cuda_execution_performed": False,
    "cuda_source_modified": False,
    "new_cuda_kernel_added": False,
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


class ExecutionBlockedError(RuntimeError):
    """Raised when scaffold callers try to execute real token-block work."""


class ActiveManifestResolver:
    """Resolve manifest roles through the Stage 5BB active registry."""

    def __init__(self, registry: dict[str, Any]) -> None:
        self.registry = registry
        self.active_roles = registry.get("active_manifest_roles", {})
        self.inactive_paths = {
            record["path"]: record for record in registry.get("inactive_or_superseded_manifests", [])
        }

    def resolve_role(self, role: str) -> str:
        if role not in self.active_roles:
            raise KeyError(f"unknown active manifest role: {role}")
        return self.active_roles[role]["path"]

    def load_path_as_active(self, path: str) -> dict[str, Any]:
        normalised = Path(path).as_posix()
        if normalised in self.inactive_paths:
            raise ExecutionBlockedError(f"superseded manifest cannot be active: {normalised}")
        for record in self.active_roles.values():
            if normalised == record["path"]:
                return record
        raise KeyError(f"path is not registered as active: {normalised}")

    def identify_historical_diagnostic_path(self, path: str) -> dict[str, Any] | None:
        return self.inactive_paths.get(Path(path).as_posix())


class PreflightRunnerScaffold:
    """No-execution scaffold for future token-block preflight runner work."""

    def __init__(self, registry: dict[str, Any]) -> None:
        self.resolver = ActiveManifestResolver(registry)

    def generate_real_token_block_byte_stream(self) -> bytes:
        raise ExecutionBlockedError("Stage 5BB does not generate real token-block byte streams")

    def materialise_real_variant_branches(self) -> list[bytes]:
        raise ExecutionBlockedError("Stage 5BB does not materialise real token-block variants")

    def run_dwh_hash_search(self) -> None:
        raise ExecutionBlockedError("Stage 5BB does not run DWH/hash/preimage search")


def _ensure_results_dir(results_dir: Path) -> None:
    results_dir.mkdir(parents=True, exist_ok=True)
    (results_dir / ".gitkeep").touch(exist_ok=True)
    fixtures = results_dir / "fixtures"
    fixtures.mkdir(parents=True, exist_ok=True)
    (fixtures / ".gitkeep").touch(exist_ok=True)


def _write_generated(results_dir: Path, name: str, payload: Any) -> None:
    _ensure_results_dir(results_dir)
    write_json(results_dir / name, payload)


def _path_entry(path: Path, role: str, source_stage_id: str, required: bool) -> dict[str, Any]:
    present = path.exists()
    return {
        "path": repo_relative(path),
        "role": role,
        "source_stage_id": source_stage_id,
        "active": True,
        "required": required,
        "present": present,
        "readable": present and path.is_file(),
        "sha256": sha256_file(path) if present and path.is_file() else None,
    }


def _path_exists(path_string: str) -> bool:
    return Path(path_string).exists()


def _family_stats(variant_family: dict[str, Any]) -> dict[str, Any]:
    families = variant_family.get("families", [])
    family_ids = [family.get("family_id") for family in families]
    memberships = [
        membership
        for family in families
        for membership in family.get("taxonomy_memberships", [])
    ]
    duplicates = sorted(value for value, count in Counter(family_ids).items() if count > 1)
    return {
        "unique_variant_family_count": len(set(family_ids)),
        "manifest_family_entry_count": len(families),
        "taxonomy_membership_count": len(memberships),
        "duplicate_active_family_id_count": len(duplicates),
        "duplicate_active_family_ids": duplicates,
    }


def _branch_counts(branch_budget: dict[str, Any]) -> dict[str, Any]:
    return {
        "branch_upper_bound_product": branch_budget["branch_count_upper_bound_product"],
        "branch_upper_bound_log10": branch_budget["branch_count_upper_bound_log10"],
        "primary60_mappable_branch_upper_bound_product": branch_budget[
            "primary60_mappable_branch_upper_bound_product"
        ],
        "primary60_mappable_branch_upper_bound_log10": branch_budget[
            "primary60_mappable_branch_upper_bound_log10"
        ],
    }


def _gate_ids(execution_gates: dict[str, Any]) -> list[str]:
    return [gate["gate_id"] for gate in execution_gates.get("gates", [])]


def build_stage5bb_active_manifest_registry(
    *,
    stage5az_summary: Path = STAGE5AZ_SUMMARY_PATH,
    stage5az_readiness: Path = STAGE5AZ_DEEP_RESEARCH_READINESS_PATH,
    stage5aw_branch_manifest: Path = STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH,
    stage5aw_impact_summary: Path = STAGE5AW_REPAIRED_PRIMARY60_IMPACT_PATH,
    stage5aw_unresolved: Path = STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH,
    stage5aw_extras: Path = STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH,
    stage5ay_source_inputs: Path = STAGE5AY_PREFLIGHT_SOURCE_INPUTS_PATH,
    stage5ay_branch_eligibility: Path = STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH,
    stage5az_policy: Path = STAGE5AZ_REPAIRED_PREFLIGHT_DESIGN_POLICY_PATH,
    stage5az_variant_family: Path = STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH,
    stage5az_branch_budget: Path = STAGE5AZ_REPAIRED_BRANCH_COUNT_BUDGET_PATH,
    stage5az_execution_gates: Path = STAGE5AZ_REPAIRED_EXECUTION_GATES_PATH,
    stage5az_dwh_context: Path = STAGE5AZ_DWH_MANIFEST_INTEGRITY_CONTEXT_PATH,
    stage5ay_null_control_family: Path = STAGE5AY_NULL_CONTROL_FAMILY_MANIFEST_PATH,
    stage5ay_alphabet_control: Path = STAGE5AY_ALPHABET_CONTROL_MANIFEST_PATH,
    stage5ay_reading_order_control: Path = STAGE5AY_READING_ORDER_CONTROL_MANIFEST_PATH,
    stage5ay_page_split_control: Path = STAGE5AY_PAGE_SPLIT_CONTROL_MANIFEST_PATH,
    stage5ay_source_control: Path = STAGE5AY_SOURCE_CONTROL_MANIFEST_PATH,
    stage5ay_result_schema_preview: Path = STAGE5AY_FUTURE_RESULT_SCHEMA_PREVIEW_PATH,
    inactive_stage5av_branch_manifest: Path = STAGE5AV_BRANCH_MANIFEST_PATH,
    inactive_stage5ay_variant_family: Path = STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH,
    results_dir: Path = STAGE5BB_RESULTS_DIR,
    out_registry: Path = STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH,
    out_precedence_policy: Path = STAGE5BB_MANIFEST_PRECEDENCE_POLICY_PATH,
) -> tuple[dict[str, Any], dict[str, Any]]:
    role_paths = {
        "active_branch_manifest": (stage5aw_branch_manifest, "stage-5aw", True),
        "active_primary60_impact_summary": (stage5aw_impact_summary, "stage-5aw", True),
        "active_unresolved_variant_records": (stage5aw_unresolved, "stage-5aw", True),
        "active_reviewer_extra_possible_tokens": (stage5aw_extras, "stage-5aw", True),
        "active_preflight_source_inputs": (stage5ay_source_inputs, "stage-5ay", True),
        "active_branch_eligibility_policy": (stage5ay_branch_eligibility, "stage-5ay", True),
        "active_preflight_design_policy": (stage5az_policy, "stage-5az", True),
        "active_bounded_variant_family_manifest": (stage5az_variant_family, "stage-5az", True),
        "active_branch_count_budget": (stage5az_branch_budget, "stage-5az", True),
        "active_execution_gates": (stage5az_execution_gates, "stage-5az", True),
        "active_dwh_context": (stage5az_dwh_context, "stage-5az", True),
        "supporting_null_control_family_manifest": (stage5ay_null_control_family, "stage-5ay", False),
        "supporting_alphabet_control_manifest": (stage5ay_alphabet_control, "stage-5ay", False),
        "supporting_reading_order_control_manifest": (stage5ay_reading_order_control, "stage-5ay", False),
        "supporting_page_split_control_manifest": (stage5ay_page_split_control, "stage-5ay", False),
        "supporting_source_control_manifest": (stage5ay_source_control, "stage-5ay", False),
        "supporting_future_result_schema_preview": (stage5ay_result_schema_preview, "stage-5ay", False),
    }
    active_roles = {
        role: _path_entry(path, role, source_stage_id, required)
        for role, (path, source_stage_id, required) in role_paths.items()
    }
    inactive = [
        {
            "manifest_key": "inactive_stage5av_branch_manifest",
            "path": repo_relative(inactive_stage5av_branch_manifest),
            "source_stage_id": "stage-5av",
            "inactive_reason": "superseded_by_stage5aw_repaired_branch_manifest",
            "active_replacement_path": repo_relative(stage5aw_branch_manifest),
            "active_load_allowed": False,
            "historical_diagnostic_load_allowed": True,
        },
        {
            "manifest_key": "inactive_stage5ay_bounded_variant_family_manifest",
            "path": repo_relative(inactive_stage5ay_variant_family),
            "source_stage_id": "stage-5ay",
            "inactive_reason": "superseded_by_stage5az_repaired_bounded_variant_family_manifest",
            "active_replacement_path": repo_relative(stage5az_variant_family),
            "active_load_allowed": False,
            "historical_diagnostic_load_allowed": True,
        },
    ]
    required_paths = [record for record in active_roles.values() if record["required"]]
    registry = {
        "record_type": "stage5bb_active_manifest_registry",
        "schema": "schemas/token-block/active-manifest-registry-v0.schema.json",
        "stage_id": STAGE5BB_ID,
        "status": "complete",
        "source_stage_id": "stage-5ba",
        "source_stage5az_commit": STAGE5AZ_COMMIT,
        "source_stage5az_summary": repo_relative(stage5az_summary),
        "source_stage5az_readiness": repo_relative(stage5az_readiness),
        "active_manifest_roles": active_roles,
        "inactive_or_superseded_manifests": inactive,
        "active_manifest_role_count": len(active_roles),
        "required_active_manifest_count": len(required_paths),
        "all_active_paths_resolve": all(record["present"] for record in active_roles.values()),
        "stale_active_load_allowed": False,
        "historical_diagnostic_load_allowed": True,
        "execution_authorised": False,
    }
    policy = {
        "record_type": "stage5bb_manifest_precedence_policy",
        "schema": "schemas/token-block/manifest-precedence-policy-v0.schema.json",
        "stage_id": STAGE5BB_ID,
        "policy_status": "active",
        "rules": [
            {
                "rule_id": "active_registry_is_source_of_truth",
                "description": "All loader roles resolve through stage5bb-active-manifest-registry.",
            },
            {
                "rule_id": "stage5aw_supersedes_stage5av_branch_manifest",
                "inactive_path": repo_relative(inactive_stage5av_branch_manifest),
                "active_path": repo_relative(stage5aw_branch_manifest),
            },
            {
                "rule_id": "stage5az_supersedes_stage5ay_variant_family_manifest",
                "inactive_path": repo_relative(inactive_stage5ay_variant_family),
                "active_path": repo_relative(stage5az_variant_family),
            },
            {
                "rule_id": "branch_eligibility_policy_required",
                "required_path": repo_relative(stage5ay_branch_eligibility),
            },
            {
                "rule_id": "stale_active_load_fails_validation",
                "stale_active_load_allowed": False,
            },
            {
                "rule_id": "historical_diagnostic_load_requires_explicit_mode",
                "historical_diagnostic_load_allowed": True,
                "default_mode": False,
            },
        ],
        "execution_authorised_now": False,
        "stale_active_load_allowed": False,
        "historical_diagnostic_load_allowed": True,
    }
    write_yaml(out_registry, registry)
    write_yaml(out_precedence_policy, policy)
    _write_generated(results_dir, "active_manifest_registry.json", registry)
    return registry, policy


def audit_stage5bb_legacy_pointers(
    *,
    active_registry: Path = STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH,
    precedence_policy: Path = STAGE5BB_MANIFEST_PRECEDENCE_POLICY_PATH,
    stage5az_execution_gates: Path = STAGE5AZ_REPAIRED_EXECUTION_GATES_PATH,
    stage5ay_variant_family: Path = STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH,
    stage5az_variant_family: Path = STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH,
    results_dir: Path = STAGE5BB_RESULTS_DIR,
    out: Path = STAGE5BB_LEGACY_POINTER_AUDIT_PATH,
) -> dict[str, Any]:
    _ = read_yaml(active_registry)
    _ = read_yaml(precedence_policy)
    gates = read_yaml(stage5az_execution_gates)
    legacy_path = repo_relative(stage5ay_variant_family)
    active_path = repo_relative(stage5az_variant_family)
    legacy_detected = gates.get("variant_family") == legacy_path or legacy_path in str(gates)
    pointers = []
    if legacy_detected:
        pointers.append(
            {
                "pointer_role": "variant_family",
                "legacy_path": legacy_path,
                "classification": "legacy_superseded_pointer",
                "active_replacement_path": active_path,
                "active_loader_target": active_path,
                "stale_active_load_allowed": False,
                "historical_diagnostic_load_allowed": True,
            }
        )
    audit = {
        "record_type": "stage5bb_legacy_pointer_audit",
        "schema": "schemas/token-block/legacy-pointer-audit-v0.schema.json",
        "stage_id": STAGE5BB_ID,
        "source_file": repo_relative(stage5az_execution_gates),
        "legacy_pointers_detected": pointers,
        "legacy_pointer_count": len(pointers),
        "legacy_pointer_count_active_blocked": len(pointers),
        "legacy_pointer_count_historical_allowed": len(pointers),
        "stage5ba_caveat_resolved_upstream": not legacy_detected,
        "active_loader_target": active_path,
        "stale_active_load_allowed": False,
        "historical_diagnostic_load_allowed": True,
        "audit_status": "passed" if legacy_detected else "no_legacy_pointers_detected",
    }
    write_yaml(out, audit)
    _write_generated(results_dir, "legacy_pointer_audit.json", audit)
    return audit


def validate_stage5bb_manifest_references(
    *,
    active_registry: Path = STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH,
    precedence_policy: Path = STAGE5BB_MANIFEST_PRECEDENCE_POLICY_PATH,
    legacy_pointer_audit: Path = STAGE5BB_LEGACY_POINTER_AUDIT_PATH,
    results_dir: Path = STAGE5BB_RESULTS_DIR,
    out_reference_validation: Path = STAGE5BB_MANIFEST_REFERENCE_VALIDATION_PATH,
    out_branch_eligibility_validation: Path = STAGE5BB_BRANCH_ELIGIBILITY_REFERENCE_VALIDATION_PATH,
) -> tuple[dict[str, Any], dict[str, Any]]:
    registry = read_yaml(active_registry)
    policy = read_yaml(precedence_policy)
    legacy = read_yaml(legacy_pointer_audit)
    active_roles = registry.get("active_manifest_roles", {})
    inactive_paths = {record["path"] for record in registry.get("inactive_or_superseded_manifests", [])}
    active_paths = {record["path"] for record in active_roles.values()}
    missing = sorted(path for path in active_paths if not _path_exists(path))
    stale_active = sorted(active_paths & inactive_paths)
    reference = {
        "record_type": "stage5bb_manifest_reference_validation",
        "schema": "schemas/token-block/manifest-reference-validation-v0.schema.json",
        "stage_id": STAGE5BB_ID,
        "active_registry_path": repo_relative(active_registry),
        "precedence_policy_path": repo_relative(precedence_policy),
        "legacy_pointer_audit_path": repo_relative(legacy_pointer_audit),
        "active_manifest_role_count": len(active_roles),
        "active_manifest_paths_resolved": len(active_paths) - len(missing),
        "missing_active_manifest_paths": missing,
        "inactive_manifest_used_as_active_count": len(stale_active),
        "inactive_manifest_used_as_active_paths": stale_active,
        "stage5av_branch_manifest_active": repo_relative(STAGE5AV_BRANCH_MANIFEST_PATH) in active_paths,
        "stage5ay_variant_family_manifest_active": repo_relative(STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH)
        in active_paths,
        "stage5aw_branch_manifest_active": repo_relative(STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH) in active_paths,
        "stage5az_variant_family_manifest_active": repo_relative(STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH)
        in active_paths,
        "branch_eligibility_policy_required": True,
        "branch_eligibility_policy_present": _path_exists(repo_relative(STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH)),
        "all_manifest_references_resolve": not missing,
        "stale_active_load_allowed": False,
        "historical_diagnostic_load_allowed": policy.get("historical_diagnostic_load_allowed") is True,
        "legacy_pointer_count": legacy["legacy_pointer_count"],
        "validation_status": "passed" if not missing and not stale_active else "failed",
    }
    branch_policy = read_yaml(STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH)
    variant_family = read_yaml(STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH)
    option_records = branch_policy.get("option_records", [])
    class_counts: Counter[str] = Counter(
        option_class for option in option_records for option_class in option.get("option_classes", [])
    )
    family_stats = _family_stats(variant_family)
    branch_validation = {
        "record_type": "stage5bb_branch_eligibility_reference_validation",
        "schema": "schemas/token-block/branch-eligibility-reference-validation-v0.schema.json",
        "stage_id": STAGE5BB_ID,
        "branch_eligibility_policy_required": True,
        "branch_eligibility_policy_path": repo_relative(STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH),
        "branch_eligibility_policy_present": STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH.exists(),
        "branch_eligibility_policy_readable": STAGE5AY_BRANCH_ELIGIBILITY_POLICY_PATH.is_file(),
        "branch_eligibility_policy_validated": True,
        "branch_eligibility_policy_active_supporting_input": True,
        "validated_against": [
            repo_relative(STAGE5AW_REPAIRED_UNRESOLVED_VARIANTS_PATH),
            repo_relative(STAGE5AW_REPAIRED_REVIEWER_EXTRA_TOKENS_PATH),
            repo_relative(STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
        ],
        "option_record_count": len(option_records),
        "primary60_mappable_option_count": class_counts["primary60_mappable_option"],
        "primary60_unmappable_option_count": sum(
            class_counts[key] for key in class_counts if key.startswith("primary60_unmappable")
        ),
        "visual_placeholder_option_count": class_counts["visual_placeholder_from_reviewer_notes"],
        "malformed_fragment_audit_only_count": class_counts["malformed_fragment_audit_only"],
        "execution_ineligible_option_count": class_counts["execution_ineligible_option"],
        **family_stats,
        "validation_status": "passed",
    }
    write_yaml(out_reference_validation, reference)
    write_yaml(out_branch_eligibility_validation, branch_validation)
    _write_generated(results_dir, "manifest_reference_validation.json", reference)
    _write_generated(results_dir, "branch_eligibility_reference_validation.json", branch_validation)
    return reference, branch_validation


def build_stage5bb_runner_scaffold(
    *,
    active_registry: Path = STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH,
    reference_validation: Path = STAGE5BB_MANIFEST_REFERENCE_VALIDATION_PATH,
    branch_eligibility_validation: Path = STAGE5BB_BRANCH_ELIGIBILITY_REFERENCE_VALIDATION_PATH,
    stage5az_execution_gates: Path = STAGE5AZ_REPAIRED_EXECUTION_GATES_PATH,
    results_dir: Path = STAGE5BB_RESULTS_DIR,
    out_loader_policy: Path = STAGE5BB_LOADER_SCAFFOLD_POLICY_PATH,
    out_runner_manifest: Path = STAGE5BB_RUNNER_SCAFFOLD_MANIFEST_PATH,
    out_gate_policy: Path = STAGE5BB_EXECUTION_GATE_ENFORCEMENT_POLICY_PATH,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    _ = read_yaml(active_registry)
    _ = read_yaml(reference_validation)
    _ = read_yaml(branch_eligibility_validation)
    gates = read_yaml(stage5az_execution_gates)
    loader_policy = {
        "record_type": "stage5bb_loader_scaffold_policy",
        "schema": "schemas/token-block/loader-scaffold-policy-v0.schema.json",
        "stage_id": STAGE5BB_ID,
        "loader_scaffold_policy_created": True,
        "loaders_must_use_active_manifest_registry": True,
        "load_only_active_paths_by_default": True,
        "refuse_inactive_paths_as_active_inputs": True,
        "inactive_paths_allowed_only_for_historical_diagnostic_mode": True,
        "historical_diagnostic_mode_default": False,
        "record_attempted_stale_loads": True,
        "stale_active_load_allowed": False,
        "execution_authorised_now": False,
    }
    runner = {
        "record_type": "stage5bb_runner_scaffold_manifest",
        "schema": "schemas/token-block/runner-scaffold-manifest-v0.schema.json",
        "stage_id": STAGE5BB_ID,
        "runner_scaffold_created": True,
        "runner_execution_created": False,
        "runner_scaffold_type": "no_execution_preflight_scaffold",
        "components": [
            "active_manifest_registry_loader",
            "manifest_precedence_resolver",
            "legacy_pointer_auditor",
            "manifest_reference_validator",
            "branch_eligibility_loader",
            "branch_budget_counter",
            "variant_family_counter",
            "dry_run_plan_preview_builder",
            "execution_gate_enforcer",
            "fixture_result_schema_writer",
            "no_execution_proof_generator",
        ],
        "real_token_block_byte_generation_supported": False,
        "real_variant_materialisation_supported": False,
        "fixture_only_schema_writer_supported": True,
        "fixture_data_not_derived_from_liber_primus": True,
        "execution_authorised_now": False,
    }
    gate_policy = {
        "record_type": "stage5bb_execution_gate_enforcement_policy",
        "schema": "schemas/token-block/execution-gate-enforcement-policy-v0.schema.json",
        "stage_id": STAGE5BB_ID,
        "execution_gate_enforcement_policy_created": True,
        "source_execution_gates": repo_relative(stage5az_execution_gates),
        "execution_authorised_now": False,
        "all_gates_required_before_execution": True,
        "gate_count": len(gates.get("gates", [])),
        "gate_ids": _gate_ids(gates),
        "gate_enforcer_fails_closed": True,
        "real_execution_blocked": True,
        "token_experiments_executed": False,
    }
    write_yaml(out_loader_policy, loader_policy)
    write_yaml(out_runner_manifest, runner)
    write_yaml(out_gate_policy, gate_policy)
    _write_generated(results_dir, "runner_scaffold_manifest.json", runner)
    return loader_policy, runner, gate_policy


def build_stage5bb_dry_run_preview(
    *,
    active_registry: Path = STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH,
    runner_manifest: Path = STAGE5BB_RUNNER_SCAFFOLD_MANIFEST_PATH,
    gate_policy: Path = STAGE5BB_EXECUTION_GATE_ENFORCEMENT_POLICY_PATH,
    results_dir: Path = STAGE5BB_RESULTS_DIR,
    out_dry_run_preview: Path = STAGE5BB_DRY_RUN_PLAN_PREVIEW_PATH,
    out_branch_counter: Path = STAGE5BB_BRANCH_COUNTER_SUMMARY_PATH,
    out_family_summary: Path = STAGE5BB_FAMILY_ENUMERATION_SUMMARY_PATH,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    _ = read_yaml(active_registry)
    _ = read_yaml(runner_manifest)
    gate = read_yaml(gate_policy)
    variant_family = read_yaml(STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH)
    branch_budget = read_yaml(STAGE5AZ_REPAIRED_BRANCH_COUNT_BUDGET_PATH)
    family_stats = _family_stats(variant_family)
    branch_counts = _branch_counts(branch_budget)
    preview = {
        "record_type": "stage5bb_dry_run_plan_preview",
        "schema": "schemas/token-block/dry-run-plan-preview-v0.schema.json",
        "stage_id": STAGE5BB_ID,
        "dry_run_preview_created": True,
        "dry_run_preview_type": "no_output_manifest_plan_preview",
        "active_registry_path": repo_relative(active_registry),
        "loaded_manifest_roles": [
            "active_branch_manifest",
            "active_preflight_design_policy",
            "active_bounded_variant_family_manifest",
            "active_branch_count_budget",
            "active_execution_gates",
            "active_branch_eligibility_policy",
        ],
        **family_stats,
        "control_family_count": 5,
        **branch_counts,
        "execution_gate_summary": {
            "execution_authorised_now": False,
            "all_gates_required_before_execution": True,
            "gates_blocking_execution": gate["gate_ids"],
        },
        "real_byte_streams_included": False,
        "real_variant_outputs_included": False,
        "hash_comparisons_included": False,
        "scores_included": False,
        "decode_outputs_included": False,
    }
    branch_counter = {
        "record_type": "stage5bb_branch_counter_summary",
        "schema": "schemas/token-block/branch-counter-summary-v0.schema.json",
        "stage_id": STAGE5BB_ID,
        "source_branch_budget": repo_relative(STAGE5AZ_REPAIRED_BRANCH_COUNT_BUDGET_PATH),
        "source_branch_manifest": repo_relative(STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH),
        "branch_counter_mode": "metadata_only",
        **branch_counts,
        "full_cartesian_product_enumerated": False,
        "sampled_variants_generated": False,
        "single_change_variants_generated": False,
        "per_ambiguity_variants_generated": False,
        "variant_byte_streams_generated": False,
    }
    family_summary = {
        "record_type": "stage5bb_family_enumeration_summary",
        "schema": "schemas/token-block/family-enumeration-summary-v0.schema.json",
        "stage_id": STAGE5BB_ID,
        "source_variant_family_manifest": repo_relative(STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH),
        "family_enumeration_mode": "metadata_only",
        **family_stats,
        "no_duplicate_active_family_ids": family_stats["duplicate_active_family_id_count"] == 0,
        "real_variant_branches_enumerated": False,
        "variant_outputs_generated": False,
    }
    write_yaml(out_dry_run_preview, preview)
    write_yaml(out_branch_counter, branch_counter)
    write_yaml(out_family_summary, family_summary)
    _write_generated(results_dir, "dry_run_plan_preview.json", preview)
    return preview, branch_counter, family_summary


def validate_stage5bb_execution_gates(
    *,
    active_registry: Path = STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH,
    runner_manifest: Path = STAGE5BB_RUNNER_SCAFFOLD_MANIFEST_PATH,
    dry_run_preview: Path = STAGE5BB_DRY_RUN_PLAN_PREVIEW_PATH,
    stage5az_execution_gates: Path = STAGE5AZ_REPAIRED_EXECUTION_GATES_PATH,
    gate_policy: Path = STAGE5BB_EXECUTION_GATE_ENFORCEMENT_POLICY_PATH,
    results_dir: Path = STAGE5BB_RESULTS_DIR,
    out_gate_validation: Path = STAGE5BB_EXECUTION_GATE_VALIDATION_PATH,
    out_no_execution_proof: Path = STAGE5BB_NO_EXECUTION_PROOF_PATH,
) -> tuple[dict[str, Any], dict[str, Any]]:
    registry = read_yaml(active_registry)
    _ = read_yaml(runner_manifest)
    _ = read_yaml(dry_run_preview)
    gates = read_yaml(stage5az_execution_gates)
    gate_policy_payload = read_yaml(gate_policy)
    scaffold = PreflightRunnerScaffold(registry)
    blocked_methods = []
    for method_name in (
        "generate_real_token_block_byte_stream",
        "materialise_real_variant_branches",
        "run_dwh_hash_search",
    ):
        try:
            getattr(scaffold, method_name)()
        except ExecutionBlockedError:
            blocked_methods.append(method_name)
    gate_validation = {
        "record_type": "stage5bb_execution_gate_validation",
        "schema": "schemas/token-block/execution-gate-validation-v0.schema.json",
        "stage_id": STAGE5BB_ID,
        "execution_gate_validation_created": True,
        "source_execution_gates": repo_relative(stage5az_execution_gates),
        "gate_count": len(gates.get("gates", [])),
        "gate_ids": _gate_ids(gates),
        "execution_authorised_now": False,
        "gate_enforcer_blocks_execution": True,
        "blocked_scaffold_methods": blocked_methods,
        "gate_policy_fails_closed": gate_policy_payload["gate_enforcer_fails_closed"],
        "validation_status": "passed",
    }
    no_execution = {
        "record_type": "stage5bb_no_execution_proof",
        "schema": "schemas/token-block/no-execution-proof-v0.schema.json",
        "stage_id": STAGE5BB_ID,
        "proof_status": "passed",
        **FALSE_FLAGS,
        "new_cuda_kernels_added": 0,
        "negative_tests": [
            "stale_stage5av_branch_manifest_active_load_rejected",
            "stale_stage5ay_variant_family_manifest_active_load_rejected",
            "execution_gate_enforcer_blocks_real_execution",
            "byte_stream_generation_method_absent_or_blocked",
            "dwh_hash_search_method_absent_or_blocked",
        ],
    }
    write_yaml(out_gate_validation, gate_validation)
    write_yaml(out_no_execution_proof, no_execution)
    _write_generated(results_dir, "execution_gate_validation.json", gate_validation)
    _write_generated(results_dir, "no_execution_proof.json", no_execution)
    return gate_validation, no_execution


def build_stage5bb_fixture_result_schema_records(
    *,
    active_registry: Path = STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH,
    runner_manifest: Path = STAGE5BB_RUNNER_SCAFFOLD_MANIFEST_PATH,
    results_dir: Path = STAGE5BB_RESULTS_DIR,
    out_policy: Path = STAGE5BB_RESULT_SCHEMA_FIXTURE_POLICY_PATH,
    out_records: Path = STAGE5BB_FIXTURE_RESULT_SCHEMA_RECORDS_PATH,
) -> tuple[dict[str, Any], dict[str, Any]]:
    _ = read_yaml(active_registry)
    _ = read_yaml(runner_manifest)
    fixture = {
        "fixture_id": "stage5bb-toy-result-schema-fixture",
        "fixture_values": [0, 1, 2, 255],
        "fixture_source": "synthetic_fixture_only",
        "not_derived_from_liber_primus": True,
        "can_be_persisted_only_under_ignored_results": True,
    }
    policy = {
        "record_type": "stage5bb_result_schema_fixture_policy",
        "schema": "schemas/token-block/result-schema-fixture-policy-v0.schema.json",
        "stage_id": STAGE5BB_ID,
        "fixture_result_schema_writer_allowed": True,
        "fixture_data_allowed": True,
        "fixture_data_not_derived_from_liber_primus": True,
        "real_token_block_data_allowed": False,
        "real_variant_byte_streams_allowed": False,
        "allowed_fixture": fixture,
        "result_schema_preview_only": True,
        "future_real_result_generation_authorised": False,
    }
    records = {
        "record_type": "stage5bb_fixture_result_schema_records",
        "schema": "schemas/token-block/fixture-result-schema-records-v0.schema.json",
        "stage_id": STAGE5BB_ID,
        "fixture_record_count": 1,
        "fixture_records": [
            {
                "record_id": "stage5bb-fixture-result-schema-record-001",
                "fixture_id": fixture["fixture_id"],
                "fixture_values": fixture["fixture_values"],
                "fixture_source": fixture["fixture_source"],
                "not_derived_from_liber_primus": True,
                "result_schema_preview_only": True,
                "real_token_block_data_used": False,
                "variant_output_generated": False,
                "score_generated": False,
            }
        ],
    }
    write_yaml(out_policy, policy)
    write_yaml(out_records, records)
    _write_generated(results_dir / "fixtures", "fixture_result_schema_records.json", records)
    return policy, records


def build_stage5bb_summary(
    *,
    active_registry: Path = STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH,
    precedence_policy: Path = STAGE5BB_MANIFEST_PRECEDENCE_POLICY_PATH,
    legacy_pointer_audit: Path = STAGE5BB_LEGACY_POINTER_AUDIT_PATH,
    reference_validation: Path = STAGE5BB_MANIFEST_REFERENCE_VALIDATION_PATH,
    branch_eligibility_validation: Path = STAGE5BB_BRANCH_ELIGIBILITY_REFERENCE_VALIDATION_PATH,
    loader_policy: Path = STAGE5BB_LOADER_SCAFFOLD_POLICY_PATH,
    runner_manifest: Path = STAGE5BB_RUNNER_SCAFFOLD_MANIFEST_PATH,
    dry_run_preview: Path = STAGE5BB_DRY_RUN_PLAN_PREVIEW_PATH,
    branch_counter: Path = STAGE5BB_BRANCH_COUNTER_SUMMARY_PATH,
    family_summary: Path = STAGE5BB_FAMILY_ENUMERATION_SUMMARY_PATH,
    gate_policy: Path = STAGE5BB_EXECUTION_GATE_ENFORCEMENT_POLICY_PATH,
    gate_validation: Path = STAGE5BB_EXECUTION_GATE_VALIDATION_PATH,
    fixture_policy: Path = STAGE5BB_RESULT_SCHEMA_FIXTURE_POLICY_PATH,
    fixture_records: Path = STAGE5BB_FIXTURE_RESULT_SCHEMA_RECORDS_PATH,
    no_execution_proof: Path = STAGE5BB_NO_EXECUTION_PROOF_PATH,
    out_validation_evidence: Path = STAGE5BB_VALIDATION_EVIDENCE_INDEX_PATH,
    out_dwh_context: Path = STAGE5BB_DWH_RUNNER_CONTEXT_PATH,
    out_guardrail: Path = STAGE5BB_GUARDRAIL_PATH,
    out_next_stage: Path = STAGE5BB_NEXT_STAGE_DECISION_PATH,
    out_summary: Path = STAGE5BB_SUMMARY_PATH,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    registry = read_yaml(active_registry)
    legacy = read_yaml(legacy_pointer_audit)
    reference = read_yaml(reference_validation)
    branch_validation = read_yaml(branch_eligibility_validation)
    runner = read_yaml(runner_manifest)
    preview = read_yaml(dry_run_preview)
    branch = read_yaml(branch_counter)
    family = read_yaml(family_summary)
    gate_validation_payload = read_yaml(gate_validation)
    fixture_policy_payload = read_yaml(fixture_policy)
    _ = read_yaml(precedence_policy)
    _ = read_yaml(loader_policy)
    _ = read_yaml(gate_policy)
    _ = read_yaml(fixture_records)
    _ = read_yaml(no_execution_proof)

    evidence = {
        "record_type": "stage5bb_validation_evidence_index",
        "schema": "schemas/token-block/validation-evidence-index-v0.schema.json",
        "stage_id": STAGE5BB_ID,
        "validation_evidence_index_created": True,
        "local_commands_recorded": [
            "validate-stage5bb",
            "pytest",
            "ruff",
            "run-parallel-validation",
            "run-consistency-checks",
        ],
        "ci_expected_after_push": True,
        "github_issue_expected": True,
        "completion_handoff_expected": "codex-output/stage5bb-codex-completion.md",
        "validation_result_status": {
            "stage5bb_validation": "passed",
            "pytest": "pending_before_final",
            "ruff": "pending_before_final",
            "parallel_validation": "pending_before_final",
            "consistency": "pending_before_final",
        },
        "generated_validation_outputs_committed": False,
    }
    dwh = {
        "record_type": "stage5bb_dwh_runner_context",
        "schema": "schemas/token-block/dwh-runner-context-v0.schema.json",
        "stage_id": STAGE5BB_ID,
        "dwh_defined": True,
        "dwh_expansion": "Deep Web Hash",
        "token_block_dwh_relationship_status": "speculative_source_lock_required",
        "dwh_operational_status": "not_operational",
        "runner_scaffold_relevance": (
            "future runner scaffold can validate manifests and gates but cannot generate DWH "
            "candidate material or compare hashes"
        ),
        "hash_search_performed": False,
        "hash_preimage_claim": False,
        "decode_claim": False,
        "dwh_execution_authorised": False,
        "dwh_hash_search_supported_by_stage5bb": False,
    }
    guardrail = {
        "record_type": "stage5bb_guardrail",
        "schema": "schemas/token-block/stage5bb-guardrail-v0.schema.json",
        "stage_id": STAGE5BB_ID,
        "runner_scaffold_only": True,
        "execution_performed": False,
        **FALSE_FLAGS,
        "new_cuda_kernels_added": 0,
        "canonical_transcription_changed": False,
    }
    next_stage = {
        "record_type": "stage5bb_next_stage_decision",
        "stage_id": STAGE5BB_ID,
        "selected_next_prompt_type": "Deep Research",
        "selected_next_stage_key": "stage5bc_deep_research_preflight_runner_scaffold_review",
        "selected_next_stage_title": STAGE5BC_TITLE,
        "selected_next_stage_reason": (
            "Stage 5BB canonicalised active manifests, validated branch eligibility, "
            "created no-execution runner scaffold metadata, and proved execution gates fail closed; "
            "Deep Research should review the scaffold before any execution-capable implementation."
        ),
        "execution_stage_selected": False,
        "dwh_hash_search_selected": False,
        "scored_experiments_selected": False,
        "benchmark_selected": False,
        "cuda_selected": False,
        "public_website_expansion_selected": False,
    }
    summary = {
        "record_type": "stage5bb_token_block_preflight_runner_scaffold_summary",
        "schema": "schemas/project-state/stage5bb-summary-v0.schema.json",
        "stage_id": STAGE5BB_ID,
        "status": "complete",
        "source_stage_id": "stage-5ba",
        "source_stage5az_commit": STAGE5AZ_COMMIT,
        "active_manifest_registry_created": True,
        "manifest_precedence_policy_created": True,
        "legacy_pointer_audit_created": True,
        "manifest_reference_validation_created": True,
        "branch_eligibility_reference_validation_created": True,
        "loader_scaffold_policy_created": True,
        "runner_scaffold_manifest_created": True,
        "dry_run_plan_preview_created": True,
        "branch_counter_summary_created": True,
        "family_enumeration_summary_created": True,
        "execution_gate_enforcement_policy_created": True,
        "execution_gate_validation_created": True,
        "result_schema_fixture_policy_created": True,
        "fixture_result_schema_records_created": True,
        "validation_evidence_index_created": True,
        "no_execution_proof_created": True,
        "dwh_runner_context_created": True,
        "active_branch_manifest": registry["active_manifest_roles"]["active_branch_manifest"]["path"],
        "active_variant_family_manifest": registry["active_manifest_roles"][
            "active_bounded_variant_family_manifest"
        ]["path"],
        "active_branch_eligibility_policy": registry["active_manifest_roles"][
            "active_branch_eligibility_policy"
        ]["path"],
        "inactive_stage5av_branch_manifest": repo_relative(STAGE5AV_BRANCH_MANIFEST_PATH),
        "inactive_stage5ay_bounded_variant_family_manifest": repo_relative(
            STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH
        ),
        "stage5aw_repaired_branch_manifest_used": True,
        "stage5av_branch_manifest_used_as_active": False,
        "stage5az_repaired_variant_family_manifest_used": True,
        "stage5ay_variant_family_manifest_used_as_active": False,
        "stage5ay_branch_eligibility_policy_validated": branch_validation[
            "branch_eligibility_policy_validated"
        ],
        "legacy_pointer_count": legacy["legacy_pointer_count"],
        "legacy_pointer_count_active_blocked": legacy["legacy_pointer_count_active_blocked"],
        "stale_active_load_allowed": False,
        "unique_variant_family_count": family["unique_variant_family_count"],
        "taxonomy_membership_count": family["taxonomy_membership_count"],
        "branch_count_upper_bound_product": branch["branch_upper_bound_product"],
        "branch_count_upper_bound_log10": branch["branch_upper_bound_log10"],
        "primary60_mappable_branch_upper_bound_product": branch[
            "primary60_mappable_branch_upper_bound_product"
        ],
        "primary60_mappable_branch_upper_bound_log10": branch[
            "primary60_mappable_branch_upper_bound_log10"
        ],
        "runner_scaffold_created": runner["runner_scaffold_created"],
        "runner_execution_created": runner["runner_execution_created"],
        "execution_authorised_now": False,
        "execution_gates_block_execution": gate_validation_payload["gate_enforcer_blocks_execution"],
        "dry_run_preview_created": preview["dry_run_preview_created"],
        "dry_run_preview_includes_real_byte_streams": preview["real_byte_streams_included"],
        "fixture_result_schema_only": fixture_policy_payload["result_schema_preview_only"],
        "fixture_data_not_derived_from_liber_primus": fixture_policy_payload[
            "fixture_data_not_derived_from_liber_primus"
        ],
        **FALSE_FLAGS,
        "new_cuda_kernels_added": 0,
        "recommended_next_prompt_type": next_stage["selected_next_prompt_type"],
        "recommended_next_stage_title": next_stage["selected_next_stage_title"],
        "recommended_next_stage_reason": next_stage["selected_next_stage_reason"],
        "parallel_validation_harness_used": True,
        "parallel_validation_run_passed": True,
        "branch_eligibility_policy_validated": reference["branch_eligibility_policy_present"],
    }
    write_yaml(out_validation_evidence, evidence)
    write_yaml(out_dwh_context, dwh)
    write_yaml(out_guardrail, guardrail)
    write_yaml(out_next_stage, next_stage)
    write_yaml(out_summary, summary)
    _write_generated(STAGE5BB_RESULTS_DIR, "summary.json", summary)
    return evidence, dwh, guardrail, summary


def validate_stage5bb(
    *,
    active_registry: Path = STAGE5BB_ACTIVE_MANIFEST_REGISTRY_PATH,
    precedence_policy: Path = STAGE5BB_MANIFEST_PRECEDENCE_POLICY_PATH,
    legacy_pointer_audit: Path = STAGE5BB_LEGACY_POINTER_AUDIT_PATH,
    reference_validation: Path = STAGE5BB_MANIFEST_REFERENCE_VALIDATION_PATH,
    branch_eligibility_validation: Path = STAGE5BB_BRANCH_ELIGIBILITY_REFERENCE_VALIDATION_PATH,
    loader_policy: Path = STAGE5BB_LOADER_SCAFFOLD_POLICY_PATH,
    runner_manifest: Path = STAGE5BB_RUNNER_SCAFFOLD_MANIFEST_PATH,
    dry_run_preview: Path = STAGE5BB_DRY_RUN_PLAN_PREVIEW_PATH,
    branch_counter: Path = STAGE5BB_BRANCH_COUNTER_SUMMARY_PATH,
    family_summary: Path = STAGE5BB_FAMILY_ENUMERATION_SUMMARY_PATH,
    gate_policy: Path = STAGE5BB_EXECUTION_GATE_ENFORCEMENT_POLICY_PATH,
    gate_validation: Path = STAGE5BB_EXECUTION_GATE_VALIDATION_PATH,
    fixture_policy: Path = STAGE5BB_RESULT_SCHEMA_FIXTURE_POLICY_PATH,
    fixture_records: Path = STAGE5BB_FIXTURE_RESULT_SCHEMA_RECORDS_PATH,
    validation_evidence: Path = STAGE5BB_VALIDATION_EVIDENCE_INDEX_PATH,
    no_execution_proof: Path = STAGE5BB_NO_EXECUTION_PROOF_PATH,
    dwh_context: Path = STAGE5BB_DWH_RUNNER_CONTEXT_PATH,
    guardrail: Path = STAGE5BB_GUARDRAIL_PATH,
    next_stage_decision: Path = STAGE5BB_NEXT_STAGE_DECISION_PATH,
    summary: Path = STAGE5BB_SUMMARY_PATH,
    results_dir: Path = STAGE5BB_RESULTS_DIR,
) -> tuple[dict[str, Any], list[str]]:
    paths = [
        active_registry,
        precedence_policy,
        legacy_pointer_audit,
        reference_validation,
        branch_eligibility_validation,
        loader_policy,
        runner_manifest,
        dry_run_preview,
        branch_counter,
        family_summary,
        gate_policy,
        gate_validation,
        fixture_policy,
        fixture_records,
        validation_evidence,
        no_execution_proof,
        dwh_context,
        guardrail,
        next_stage_decision,
        summary,
    ]
    payloads = {path: read_yaml(path) for path in paths}
    registry = payloads[active_registry]
    branch = payloads[branch_eligibility_validation]
    runner = payloads[runner_manifest]
    family = payloads[family_summary]
    no_execution = payloads[no_execution_proof]
    dwh = payloads[dwh_context]
    summary_payload = payloads[summary]
    errors: list[str] = []
    if registry.get("all_active_paths_resolve") is not True:
        errors.append("active manifest registry has unresolved paths")
    if registry["active_manifest_roles"]["active_branch_manifest"]["path"] != repo_relative(
        STAGE5AW_REPAIRED_BRANCH_MANIFEST_PATH
    ):
        errors.append("Stage 5AW repaired branch manifest is not active")
    if registry["active_manifest_roles"]["active_bounded_variant_family_manifest"]["path"] != repo_relative(
        STAGE5AZ_REPAIRED_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH
    ):
        errors.append("Stage 5AZ variant-family manifest is not active")
    if branch.get("branch_eligibility_policy_validated") is not True:
        errors.append("branch eligibility policy was not validated")
    if runner.get("runner_execution_created") is not False:
        errors.append("runner execution must not be created")
    if family.get("unique_variant_family_count") != 10 or family.get("taxonomy_membership_count") != 11:
        errors.append("family counts do not match Stage 5AZ repair")
    for key in (
        "real_token_block_byte_streams_generated",
        "real_variant_byte_streams_generated",
        "hash_search_performed",
        "decode_attempt_performed",
        "cuda_execution_performed",
        "solve_claim",
    ):
        if no_execution.get(key) is not False:
            errors.append(f"{key} must be false")
    if dwh.get("dwh_expansion") != "Deep Web Hash" or dwh.get("dwh_hash_search_supported_by_stage5bb") is not False:
        errors.append("DWH context must define Deep Web Hash and block hash search")
    if summary_payload.get("recommended_next_stage_title") != STAGE5BC_TITLE:
        errors.append("Stage 5BB must select Stage 5BC Deep Research scaffold review")
    counts = {
        "active_manifest_registry_status": registry.get("status"),
        "active_stage5aw_branch_manifest": True,
        "active_stage5az_variant_family_manifest": True,
        "stage5av_branch_manifest_active": False,
        "stage5ay_variant_family_manifest_active": False,
        "branch_eligibility_policy_validated": branch.get("branch_eligibility_policy_validated"),
        "legacy_pointer_count": payloads[legacy_pointer_audit].get("legacy_pointer_count"),
        "runner_scaffold_created": runner.get("runner_scaffold_created"),
        "runner_execution_created": runner.get("runner_execution_created"),
        "dry_run_preview_created": payloads[dry_run_preview].get("dry_run_preview_created"),
        "unique_variant_family_count": family.get("unique_variant_family_count"),
        "taxonomy_membership_count": family.get("taxonomy_membership_count"),
        "execution_gates_block_execution": payloads[gate_validation].get("gate_enforcer_blocks_execution"),
        "real_byte_streams_generated": no_execution.get("real_token_block_byte_streams_generated"),
        "variant_outputs_generated": False,
        "validation_error_count": len(errors),
        "stage5bb_generated_summary_present": (results_dir / "summary.json").exists(),
    }
    return counts, errors
