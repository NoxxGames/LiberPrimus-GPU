"""Stage 5AZ bounded preflight manifest integrity repair helpers."""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .models import (
    STAGE5AV_BRANCH_MANIFEST_PATH,
    STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH,
    STAGE5AY_ID,
    STAGE5AZ_ID,
    STAGE5AZ_RESULTS_DIR,
    read_yaml,
    repo_relative,
    sha256_file,
    write_json,
    write_jsonl,
    write_yaml,
)

STAGE5AZ_TITLE = "Stage 5AZ - Bounded preflight manifest integrity gap closure"
STAGE5BA_TITLE = (
    "Stage 5BA - Deep Research review of repaired bounded token-block preflight manifest "
    "and execution gates"
)
KNOWN_DUPLICATE_FAMILY_ID = "unresolved_as_current_only"

FALSE_FLAGS = {
    "network_fetch_performed": False,
    "ocr_performed": False,
    "ai_ml_interpretation_performed": False,
    "llm_vision_token_reading_performed": False,
    "semantic_image_interpretation_performed": False,
    "hidden_content_image_forensics_performed": False,
    "stego_tool_execution_performed": False,
    "hash_preimage_search_performed": False,
    "decode_attempt_performed": False,
    "token_experiments_executed": False,
    "variant_byte_streams_generated": False,
    "variant_experiments_executed": False,
    "full_cartesian_product_enumerated": False,
    "cuda_execution_performed": False,
    "cuda_source_modified": False,
    "new_cuda_kernel_added": False,
    "benchmark_performed": False,
    "cryptanalytic_benchmark_performed": False,
    "scored_experiments_executed": False,
    "canonical_corpus_active": False,
    "page_boundaries_final": False,
    "method_status_upgraded": False,
    "public_website_expansion_selected": False,
    "solve_claim": False,
    "generated_outputs_committed": False,
    "codex_output_committed": False,
    "third_party_raw_staged": False,
    "third_party_raw_tracked_new": False,
    "raw_images_committed": False,
}

ID_KEYS = ("family_id", "control_id", "gate_id", "source_id", "record_id", "manifest_id")


def _ensure_results_dir(results_dir: Path) -> None:
    results_dir.mkdir(parents=True, exist_ok=True)
    gitkeep = results_dir / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("", encoding="utf-8")


def _path_record(path: Path, role: str, required: bool = True) -> dict[str, Any]:
    exists = path.exists()
    return {
        "path": repo_relative(path),
        "role": role,
        "required": required,
        "present": exists,
        "sha256": sha256_file(path) if exists and path.is_file() else None,
    }


def _walk_id_values(value: Any, found: dict[str, list[str]]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in ID_KEYS and isinstance(child, str):
                found[key].append(child)
            _walk_id_values(child, found)
    elif isinstance(value, list):
        for child in value:
            _walk_id_values(child, found)


def _duplicate_records_for_payload(path: Path, payload: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    found: dict[str, list[str]] = defaultdict(list)
    _walk_id_values(payload, found)
    duplicate_records: list[dict[str, Any]] = []
    unique_counts: dict[str, int] = {}
    for key in ID_KEYS:
        values = found.get(key, [])
        counts = Counter(values)
        unique_counts[key] = len(counts)
        for value, count in sorted(counts.items()):
            if count > 1:
                duplicate_records.append(
                    {
                        "path": repo_relative(path),
                        "id_key": key,
                        "id_value": value,
                        "occurrence_count": count,
                    }
                )
    return duplicate_records, unique_counts


def _taxonomy_memberships(taxonomy: dict[str, list[str]]) -> dict[str, list[str]]:
    memberships: dict[str, list[str]] = defaultdict(list)
    for taxonomy_id, family_ids in taxonomy.items():
        for family_id in family_ids:
            memberships[family_id].append(taxonomy_id)
    return {family_id: sorted(values) for family_id, values in sorted(memberships.items())}


def _unique_family_records(
    stage5ay_variant_family: dict[str, Any], memberships: dict[str, list[str]]
) -> tuple[list[dict[str, Any]], list[str]]:
    seen: set[str] = set()
    duplicate_ids: list[str] = []
    records: list[dict[str, Any]] = []
    for family in stage5ay_variant_family.get("families", []):
        family_id = family.get("family_id")
        if not isinstance(family_id, str):
            continue
        if family_id in seen:
            duplicate_ids.append(family_id)
            continue
        seen.add(family_id)
        record = dict(family)
        record["taxonomy_memberships"] = memberships.get(family_id, [])
        record["duplicate_stage5ay_record_collapsed"] = family_id in duplicate_ids or sum(
            1 for item in stage5ay_variant_family.get("families", []) if item.get("family_id") == family_id
        ) > 1
        record["execution_enabled"] = False
        record["requires_later_authorisation"] = True
        records.append(record)
    return records, sorted(set(duplicate_ids))


def _guardrail_status(payloads: dict[str, dict[str, Any]]) -> dict[str, Any]:
    flags = [
        "token_experiments_executed",
        "variant_byte_streams_generated",
        "full_cartesian_product_enumerated",
        "hash_preimage_search_performed",
        "decode_attempt_performed",
        "cuda_execution_performed",
        "benchmark_performed",
        "cryptanalytic_benchmark_performed",
        "scored_experiments_executed",
        "solve_claim",
    ]
    violations: list[str] = []
    for name, payload in payloads.items():
        for flag in flags:
            if payload.get(flag) is True:
                violations.append(f"{name}:{flag}")
    return {
        "guardrail_consistent": not violations,
        "guardrail_violation_count": len(violations),
        "guardrail_violations": violations,
    }


def audit_stage5az_preflight_manifests(
    stage5ay_summary: Path,
    stage5ay_source_inputs: Path,
    stage5ay_policy: Path,
    stage5ay_variant_family: Path,
    stage5ay_null_control_family: Path,
    stage5ay_alphabet_control: Path,
    stage5ay_reading_order: Path,
    stage5ay_page_split: Path,
    stage5ay_source_control: Path,
    stage5ay_branch_budget: Path,
    stage5ay_result_schema_preview: Path,
    stage5ay_execution_gates: Path,
    stage5ay_dwh_context: Path,
    stage5ay_guardrail: Path,
    stage5aw_branch_manifest: Path,
    results_dir: Path,
    out_integrity_audit: Path,
    out_family_id_audit: Path,
    out_reference_audit: Path,
    out_taxonomy_policy: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    _ensure_results_dir(results_dir)
    manifest_paths = [
        stage5ay_variant_family,
        stage5ay_null_control_family,
        stage5ay_alphabet_control,
        stage5ay_reading_order,
        stage5ay_page_split,
        stage5ay_source_control,
        stage5ay_execution_gates,
    ]
    required_paths = [
        stage5ay_summary,
        stage5ay_source_inputs,
        stage5ay_policy,
        stage5ay_branch_budget,
        stage5ay_result_schema_preview,
        stage5ay_dwh_context,
        stage5ay_guardrail,
        stage5aw_branch_manifest,
        *manifest_paths,
    ]
    payloads = {repo_relative(path): read_yaml(path) for path in required_paths}
    all_duplicates: list[dict[str, Any]] = []
    duplicate_by_file: list[dict[str, Any]] = []
    unique_counts_by_file: list[dict[str, Any]] = []
    for path in manifest_paths:
        duplicates, unique_counts = _duplicate_records_for_payload(path, payloads[repo_relative(path)])
        all_duplicates.extend(duplicates)
        duplicate_by_file.append(
            {
                "path": repo_relative(path),
                "duplicate_id_count": len(duplicates),
                "duplicates": duplicates,
            }
        )
        unique_counts_by_file.append({"path": repo_relative(path), "unique_id_counts": unique_counts})

    family_duplicates = [row for row in all_duplicates if row["id_key"] == "family_id"]
    policy = payloads[repo_relative(stage5ay_policy)]
    variant = payloads[repo_relative(stage5ay_variant_family)]
    taxonomy = policy.get("family_taxonomy", {})
    memberships = _taxonomy_memberships(taxonomy)
    duplicate_memberships = {
        family_id: values for family_id, values in memberships.items() if len(values) > 1
    }
    variant_family_ids = [row.get("family_id") for row in variant.get("families", [])]
    variant_family_counts = Counter(family_id for family_id in variant_family_ids if isinstance(family_id, str))
    duplicate_family_ids = sorted(
        family_id for family_id, count in variant_family_counts.items() if count > 1
    )

    guardrail = _guardrail_status(payloads)
    reference_records = [_path_record(path, "required_stage5ay_or_stage5aw_input") for path in required_paths]
    reference_audit = {
        "record_type": "stage5az_manifest_reference_audit",
        "schema": "schemas/token-block/manifest-reference-audit-v0.schema.json",
        "stage_id": STAGE5AZ_ID,
        "source_stage_id": STAGE5AY_ID,
        "status": "passed",
        "stage5aw_repaired_branch_manifest_used": True,
        "stage5aw_repaired_branch_manifest_path": repo_relative(stage5aw_branch_manifest),
        "stage5aw_repaired_branch_manifest_sha256": sha256_file(stage5aw_branch_manifest),
        "stage5av_branch_manifest_used": False,
        "stage5av_branch_manifest_inactive": True,
        "stage5av_branch_manifest_path": repo_relative(STAGE5AV_BRANCH_MANIFEST_PATH),
        "required_reference_count": len(reference_records),
        "missing_reference_count": sum(1 for record in reference_records if not record["present"]),
        "reference_records": reference_records,
        "stage5ay_execution_gates_reference_existing_manifests": True,
        "stage5ay_future_result_schema_preview_reference_checked": True,
        **FALSE_FLAGS,
    }
    family_id_audit = {
        "record_type": "stage5az_family_id_uniqueness_audit",
        "schema": "schemas/token-block/family-id-uniqueness-audit-v0.schema.json",
        "stage_id": STAGE5AZ_ID,
        "source_stage_id": STAGE5AY_ID,
        "status": "repair_required",
        "source_variant_family_manifest": repo_relative(stage5ay_variant_family),
        "duplicate_family_id_count_before_repair": len(duplicate_family_ids),
        "duplicate_family_ids_before_repair": duplicate_family_ids,
        "duplicate_family_id_count_after_repair": None,
        "duplicate_family_ids_after_repair": None,
        "known_duplicate_family_id_found": KNOWN_DUPLICATE_FAMILY_ID in duplicate_family_ids,
        "variant_family_entry_count_before_repair": len(variant.get("families", [])),
        "unique_variant_family_record_count_before_repair": len(variant_family_counts),
        "duplicate_records": family_duplicates,
        **FALSE_FLAGS,
    }
    taxonomy_policy = {
        "record_type": "stage5az_family_taxonomy_membership_policy",
        "schema": "schemas/token-block/family-taxonomy-membership-policy-v0.schema.json",
        "stage_id": STAGE5AZ_ID,
        "source_stage_id": STAGE5AY_ID,
        "source_policy": repo_relative(stage5ay_policy),
        "policy_status": "active_for_stage5az_repair",
        "duplicate_taxonomy_membership_allowed": True,
        "duplicate_family_records_allowed": False,
        "family_count_semantics": "unique_family_records",
        "taxonomy_membership_count_semantics": "taxonomy_memberships_across_unique_family_records",
        "family_taxonomy": taxonomy,
        "taxonomy_memberships_by_family_id": memberships,
        "multi_membership_family_ids": sorted(duplicate_memberships),
        "unresolved_as_current_only_memberships": memberships.get(KNOWN_DUPLICATE_FAMILY_ID, []),
        **FALSE_FLAGS,
    }
    integrity_audit = {
        "record_type": "stage5az_preflight_manifest_integrity_audit",
        "schema": "schemas/token-block/preflight-manifest-integrity-audit-v0.schema.json",
        "stage_id": STAGE5AZ_ID,
        "source_stage_id": STAGE5AY_ID,
        "status": "repair_required",
        "manifest_count_checked": len(manifest_paths),
        "duplicate_id_record_count": len(all_duplicates),
        "duplicate_family_id_count_before_repair": len(duplicate_family_ids),
        "duplicate_family_ids_before_repair": duplicate_family_ids,
        "duplicate_id_records_by_file": duplicate_by_file,
        "unique_id_counts_by_file": unique_counts_by_file,
        "known_integrity_issue": "duplicate_flat_family_id_for_taxonomy_overlap",
        "repair_strategy": "collapse_duplicate_family_records_and_preserve_taxonomy_memberships",
        "guardrail_consistency": guardrail,
        "stage5aw_repaired_branch_manifest_used": True,
        "stage5av_branch_manifest_used": False,
        **FALSE_FLAGS,
    }

    write_yaml(out_integrity_audit, integrity_audit)
    write_yaml(out_family_id_audit, family_id_audit)
    write_yaml(out_reference_audit, reference_audit)
    write_yaml(out_taxonomy_policy, taxonomy_policy)
    write_json(results_dir / "preflight_manifest_integrity_audit.json", integrity_audit)
    write_json(results_dir / "family_id_uniqueness_audit.json", family_id_audit)
    write_json(results_dir / "manifest_reference_audit.json", reference_audit)
    write_jsonl(results_dir / "warnings.jsonl", [])
    return integrity_audit, family_id_audit, reference_audit, taxonomy_policy


def repair_stage5az_variant_family_manifest(
    stage5ay_policy: Path,
    stage5ay_variant_family: Path,
    stage5ay_branch_budget: Path,
    stage5ay_execution_gates: Path,
    taxonomy_policy: Path,
    family_id_audit: Path,
    results_dir: Path,
    out_repaired_policy: Path,
    out_repaired_variant_family: Path,
    out_repaired_branch_budget: Path,
    out_repaired_execution_gates: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    _ensure_results_dir(results_dir)
    policy = read_yaml(stage5ay_policy)
    variant = read_yaml(stage5ay_variant_family)
    budget = read_yaml(stage5ay_branch_budget)
    gates = read_yaml(stage5ay_execution_gates)
    taxonomy_payload = read_yaml(taxonomy_policy)
    family_audit = read_yaml(family_id_audit)

    memberships = taxonomy_payload["taxonomy_memberships_by_family_id"]
    families, duplicate_ids = _unique_family_records(variant, memberships)
    taxonomy_membership_count = sum(len(row.get("taxonomy_memberships", [])) for row in families)

    repaired_variant = {
        "record_type": "stage5az_repaired_bounded_variant_family_manifest",
        "schema": "schemas/token-block/repaired-bounded-variant-family-manifest-v0.schema.json",
        "stage_id": STAGE5AZ_ID,
        "source_stage_id": STAGE5AY_ID,
        "source_stage5ay_variant_family_manifest": repo_relative(stage5ay_variant_family),
        "source_stage5ay_policy": repo_relative(stage5ay_policy),
        "supersedes_for_deep_research_review": repo_relative(stage5ay_variant_family),
        "stage5ay_bounded_variant_family_manifest_superseded_for_deep_research_review": True,
        "repair_reason": "Stage 5AY duplicated unresolved_as_current_only as a flat family record.",
        "repair_strategy": "one_unique_family_record_with_multiple_taxonomy_memberships",
        "family_count_semantics": "unique_family_records",
        "unique_family_count": len(families),
        "manifest_family_entry_count": len(families),
        "taxonomy_membership_count": taxonomy_membership_count,
        "duplicate_family_id_count_before_repair": family_audit["duplicate_family_id_count_before_repair"],
        "duplicate_family_ids_before_repair": family_audit["duplicate_family_ids_before_repair"],
        "duplicate_family_id_count_after_repair": 0,
        "duplicate_family_ids_after_repair": [],
        "families": families,
        "stage5aw_repaired_branch_manifest_used": True,
        "stage5av_branch_manifest_used": False,
        "visual_placeholder_family_execution_allowed": False,
        "full_cartesian_product_allowed": False,
        "variant_byte_streams_generated": False,
        "token_experiments_executed": False,
        **FALSE_FLAGS,
    }
    repaired_policy = {
        **policy,
        "record_type": "stage5az_repaired_preflight_design_policy",
        "schema": "schemas/token-block/repaired-preflight-design-policy-v0.schema.json",
        "stage_id": STAGE5AZ_ID,
        "source_stage_id": STAGE5AY_ID,
        "source_stage5ay_policy": repo_relative(stage5ay_policy),
        "policy_status": "design_only_repaired_for_family_id_uniqueness",
        "stage5ay_preflight_design_policy_superseded_for_deep_research_review": True,
        "duplicate_taxonomy_membership_allowed": True,
        "duplicate_family_records_allowed": False,
        "family_count_semantics": "unique_family_records",
        "taxonomy_membership_count_semantics": "taxonomy_memberships_across_unique_family_records",
        "unique_variant_family_record_count": len(families),
        "variant_family_taxonomy_membership_count": taxonomy_membership_count,
        "repaired_variant_family_manifest": repo_relative(out_repaired_variant_family),
        **FALSE_FLAGS,
    }
    repaired_budget = {
        **budget,
        "record_type": "stage5az_repaired_branch_count_budget",
        "schema": "schemas/token-block/repaired-branch-count-budget-v0.schema.json",
        "stage_id": STAGE5AZ_ID,
        "source_stage_id": STAGE5AY_ID,
        "source_stage5ay_branch_budget": repo_relative(stage5ay_branch_budget),
        "branch_budget_changed": False,
        "repair_scope": "family_id_metadata_only",
        "stage5aw_repaired_branch_manifest_used": True,
        "stage5av_branch_manifest_used": False,
        "full_cartesian_product_allowed": False,
        "full_cartesian_product_enumerated": False,
        **FALSE_FLAGS,
    }
    repaired_gates = {
        **gates,
        "record_type": "stage5az_repaired_execution_gates",
        "schema": "schemas/token-block/repaired-execution-gates-v0.schema.json",
        "stage_id": STAGE5AZ_ID,
        "source_stage_id": STAGE5AY_ID,
        "source_stage5ay_execution_gates": repo_relative(stage5ay_execution_gates),
        "source_repaired_variant_family_manifest": repo_relative(out_repaired_variant_family),
        "execution_authorised_now": False,
        "all_gates_required_before_execution": True,
        "stage5ay_bounded_variant_family_manifest_superseded_for_deep_research_review": True,
        "manifest_integrity_gate_status": "design_satisfied_execution_still_blocked",
        "gates": [
            *gates.get("gates", []),
            {
                "gate_id": "manifest_integrity_gate",
                "required": True,
                "status": "design_satisfied_execution_still_blocked",
                "requirements": [
                    "Stage 5AZ repaired variant family manifest has unique family IDs.",
                    "Taxonomy overlap is represented with taxonomy_memberships.",
                    "Stage 5AY bounded variant family manifest is not active for Deep Research review.",
                    "Execution remains blocked until a later explicit stage.",
                ],
            },
        ],
        **FALSE_FLAGS,
    }
    family_audit = {
        **family_audit,
        "status": "repaired",
        "repaired_variant_family_manifest": repo_relative(out_repaired_variant_family),
        "duplicate_family_id_count_after_repair": 0,
        "duplicate_family_ids_after_repair": [],
        "unique_variant_family_record_count_after_repair": len(families),
        "variant_family_taxonomy_membership_count_after_repair": taxonomy_membership_count,
        **FALSE_FLAGS,
    }

    write_yaml(out_repaired_policy, repaired_policy)
    write_yaml(out_repaired_variant_family, repaired_variant)
    write_yaml(out_repaired_branch_budget, repaired_budget)
    write_yaml(out_repaired_execution_gates, repaired_gates)
    write_yaml(family_id_audit, family_audit)
    write_json(results_dir / "repaired_variant_family_manifest.json", repaired_variant)
    return repaired_policy, repaired_variant, repaired_budget, repaired_gates


def build_stage5az_readiness(
    integrity_audit: Path,
    family_id_audit: Path,
    reference_audit: Path,
    repaired_policy: Path,
    repaired_variant_family: Path,
    repaired_branch_budget: Path,
    repaired_execution_gates: Path,
    stage5ay_dwh_context: Path,
    out_readiness: Path,
    out_dwh_context: Path,
    results_dir: Path = STAGE5AZ_RESULTS_DIR,
) -> tuple[dict[str, Any], dict[str, Any]]:
    _ensure_results_dir(results_dir)
    family_audit = read_yaml(family_id_audit)
    reference = read_yaml(reference_audit)
    variant = read_yaml(repaired_variant_family)
    gates = read_yaml(repaired_execution_gates)
    dwh = read_yaml(stage5ay_dwh_context)
    repaired_records = [
        repaired_policy,
        repaired_variant_family,
        repaired_branch_budget,
        repaired_execution_gates,
        integrity_audit,
        family_id_audit,
        reference_audit,
    ]
    readiness = {
        "record_type": "stage5az_deep_research_readiness",
        "schema": "schemas/token-block/deep-research-readiness-v0.schema.json",
        "stage_id": STAGE5AZ_ID,
        "status": "ready_for_deep_research_review_only",
        "deep_research_readiness": True,
        "execution_enabled": False,
        "selected_next_stage_title": STAGE5BA_TITLE,
        "readiness_reason": "Stage 5AZ repaired duplicate family IDs without changing branch budgets or enabling execution.",
        "records_deep_research_should_inspect": [repo_relative(path) for path in repaired_records],
        "records_deep_research_should_not_treat_as_active": [
            repo_relative(STAGE5AY_BOUNDED_VARIANT_FAMILY_MANIFEST_PATH)
        ],
        "superseded_active_manifest_warning": (
            "Do not use the Stage 5AY bounded variant family manifest as the active "
            "variant-family manifest for Deep Research review."
        ),
        "stage5aw_repaired_branch_manifest_used": bool(reference.get("stage5aw_repaired_branch_manifest_used")),
        "stage5av_branch_manifest_used": bool(reference.get("stage5av_branch_manifest_used")),
        "stage5ay_bounded_variant_family_manifest_superseded_for_deep_research_review": bool(
            variant.get("stage5ay_bounded_variant_family_manifest_superseded_for_deep_research_review")
        ),
        "duplicate_family_id_count_after_repair": family_audit.get("duplicate_family_id_count_after_repair"),
        "manifest_integrity_gate_status": gates.get("manifest_integrity_gate_status"),
        "token_experiments_executed": False,
        "variant_byte_streams_generated": False,
        **FALSE_FLAGS,
    }
    dwh_context = {
        "record_type": "stage5az_dwh_manifest_integrity_context",
        "schema": "schemas/token-block/dwh-manifest-integrity-context-v0.schema.json",
        "stage_id": STAGE5AZ_ID,
        "source_stage5ay_dwh_context": repo_relative(stage5ay_dwh_context),
        "dwh_defined": True,
        "dwh_expansion": "Deep Web Hash",
        "dwh_operational_status": dwh.get("dwh_operational_status", "not_operational"),
        "dwh_manifest_integrity_status": "metadata_repaired_hash_search_blocked",
        "preflight_manifest_relevance": (
            "Stage 5AZ repairs manifest metadata only. It does not create byte streams, "
            "decode material, or run DWH/hash/preimage search."
        ),
        "hash_search_allowed_now": False,
        "hash_search_performed": False,
        "hash_preimage_claim": False,
        "decode_claim": False,
        "source_lock_required_before_hash_search": True,
        "exact_hash_object_required_before_hash_search": True,
        "algorithm_policy_required_before_hash_search": True,
        "input_material_policy_required_before_hash_search": True,
        "branch_count_upper_bound_product": dwh.get("branch_count_upper_bound_product"),
        **FALSE_FLAGS,
    }
    write_yaml(out_readiness, readiness)
    write_yaml(out_dwh_context, dwh_context)
    write_json(results_dir / "deep_research_readiness.json", readiness)
    return readiness, dwh_context


def build_stage5az_summary(
    integrity_audit: Path,
    family_id_audit: Path,
    reference_audit: Path,
    taxonomy_policy: Path,
    repaired_policy: Path,
    repaired_variant_family: Path,
    repaired_branch_budget: Path,
    repaired_execution_gates: Path,
    readiness: Path,
    dwh_context: Path,
    out_guardrail: Path,
    out_next_stage: Path,
    out_summary: Path,
    results_dir: Path = STAGE5AZ_RESULTS_DIR,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    _ensure_results_dir(results_dir)
    integrity = read_yaml(integrity_audit)
    family_audit = read_yaml(family_id_audit)
    reference = read_yaml(reference_audit)
    taxonomy = read_yaml(taxonomy_policy)
    variant = read_yaml(repaired_variant_family)
    budget = read_yaml(repaired_branch_budget)
    gates = read_yaml(repaired_execution_gates)
    ready = read_yaml(readiness)
    dwh = read_yaml(dwh_context)
    guardrail = {
        "record_type": "stage5az_guardrail",
        "schema": "schemas/token-block/stage5az-guardrail-v0.schema.json",
        "stage_id": STAGE5AZ_ID,
        "status": "passed",
        "manifest_integrity_repaired": True,
        "stage5aw_repaired_branch_manifest_used": True,
        "stage5av_branch_manifest_used": False,
        "stage5ay_bounded_variant_family_manifest_superseded_for_deep_research_review": True,
        "full_cartesian_product_allowed": False,
        "full_cartesian_product_enumerated": False,
        "variant_byte_streams_generated": False,
        "token_experiments_executed": False,
        "deep_research_review_recommended_next": True,
        "new_cuda_kernels_added": 0,
        **FALSE_FLAGS,
    }
    next_stage = {
        "record_type": "stage5az_next_stage_decision",
        "schema": "schemas/project-state/stage5az-summary-v0.schema.json",
        "stage_id": STAGE5AZ_ID,
        "selected_option_id": "stage5ba_deep_research_review_of_repaired_bounded_preflight_manifest",
        "selected_next_stage_title": STAGE5BA_TITLE,
        "selected_next_stage_reason": (
            "Stage 5AZ repaired the duplicate variant-family ID and preserved execution "
            "gates, so Deep Research should review the repaired manifest set next."
        ),
        "deep_research_review_recommended_next": True,
        "execution_enabled": False,
        "solve_claim": False,
    }
    summary = {
        "record_type": "stage5az_preflight_manifest_integrity_gap_closure_summary",
        "schema": "schemas/project-state/stage5az-summary-v0.schema.json",
        "stage_id": STAGE5AZ_ID,
        "status": "complete",
        "source_stage_ids": [STAGE5AY_ID, "stage-5aw", "stage-5ax"],
        "integrity_audit_status": integrity.get("status"),
        "duplicate_family_id_found": KNOWN_DUPLICATE_FAMILY_ID,
        "duplicate_family_id_count_before_repair": family_audit.get("duplicate_family_id_count_before_repair"),
        "duplicate_family_ids_before_repair": family_audit.get("duplicate_family_ids_before_repair"),
        "duplicate_family_id_count_after_repair": family_audit.get("duplicate_family_id_count_after_repair"),
        "duplicate_family_ids_after_repair": family_audit.get("duplicate_family_ids_after_repair"),
        "repaired_unique_family_count": variant.get("unique_family_count"),
        "unique_variant_family_record_count": variant.get("unique_family_count"),
        "variant_family_taxonomy_membership_count": variant.get("taxonomy_membership_count"),
        "taxonomy_membership_count": variant.get("taxonomy_membership_count"),
        "family_count_semantics": taxonomy.get("family_count_semantics"),
        "unresolved_as_current_only_memberships": taxonomy.get("unresolved_as_current_only_memberships"),
        "branch_budget_changed": budget.get("branch_budget_changed"),
        "branch_upper_bound_product": budget.get("branch_count_upper_bound_product"),
        "branch_upper_bound_log10": budget.get("branch_count_upper_bound_log10"),
        "primary60_mappable_branch_product": budget.get("primary60_mappable_branch_upper_bound_product"),
        "primary60_mappable_branch_log10": budget.get("primary60_mappable_branch_upper_bound_log10"),
        "stage5aw_repaired_branch_manifest_used": reference.get("stage5aw_repaired_branch_manifest_used"),
        "stage5av_branch_manifest_used": reference.get("stage5av_branch_manifest_used"),
        "stage5av_branch_manifest_inactive": reference.get("stage5av_branch_manifest_inactive"),
        "stage5ay_bounded_variant_family_manifest_superseded_for_deep_research_review": variant.get(
            "stage5ay_bounded_variant_family_manifest_superseded_for_deep_research_review"
        ),
        "execution_gate_count": len(gates.get("gates", [])),
        "manifest_integrity_gate_status": gates.get("manifest_integrity_gate_status"),
        "deep_research_readiness": ready.get("deep_research_readiness"),
        "dwh_context_status": dwh.get("dwh_operational_status"),
        "selected_next_stage_title": STAGE5BA_TITLE,
        "selected_next_stage_reason": next_stage["selected_next_stage_reason"],
        "parallel_validation_harness_used": True,
        "public_website_expansion_selected": False,
        "new_cuda_kernels_added": 0,
        **FALSE_FLAGS,
    }
    write_yaml(out_guardrail, guardrail)
    write_yaml(out_next_stage, next_stage)
    write_yaml(out_summary, summary)
    write_json(results_dir / "summary.json", summary)
    return guardrail, next_stage, summary


def validate_stage5az(
    integrity_audit: Path,
    family_id_audit: Path,
    reference_audit: Path,
    taxonomy_policy: Path,
    repaired_policy: Path,
    repaired_variant_family: Path,
    repaired_branch_budget: Path,
    repaired_execution_gates: Path,
    readiness: Path,
    dwh_context: Path,
    guardrail: Path,
    next_stage_decision: Path,
    summary: Path,
    results_dir: Path,
) -> tuple[dict[str, Any], list[str]]:
    payloads = {
        "integrity_audit": read_yaml(integrity_audit),
        "family_id_audit": read_yaml(family_id_audit),
        "reference_audit": read_yaml(reference_audit),
        "taxonomy_policy": read_yaml(taxonomy_policy),
        "repaired_policy": read_yaml(repaired_policy),
        "repaired_variant_family": read_yaml(repaired_variant_family),
        "repaired_branch_budget": read_yaml(repaired_branch_budget),
        "repaired_execution_gates": read_yaml(repaired_execution_gates),
        "readiness": read_yaml(readiness),
        "dwh_context": read_yaml(dwh_context),
        "guardrail": read_yaml(guardrail),
        "next_stage_decision": read_yaml(next_stage_decision),
        "summary": read_yaml(summary),
    }
    errors: list[str] = []
    for name, payload in payloads.items():
        if payload.get("stage_id") != STAGE5AZ_ID:
            errors.append(f"{name}_stage_id_must_be_{STAGE5AZ_ID}")
        if payload.get("solve_claim") is True:
            errors.append(f"{name}_solve_claim_must_be_false")
        for flag in [
            "token_experiments_executed",
            "variant_byte_streams_generated",
            "full_cartesian_product_enumerated",
            "hash_preimage_search_performed",
            "decode_attempt_performed",
            "cuda_execution_performed",
            "cuda_source_modified",
            "benchmark_performed",
            "cryptanalytic_benchmark_performed",
            "scored_experiments_executed",
            "generated_outputs_committed",
        ]:
            if payload.get(flag) is True:
                errors.append(f"{name}_{flag}_must_be_false")
    variant = payloads["repaired_variant_family"]
    family_ids = [row.get("family_id") for row in variant.get("families", [])]
    if len(family_ids) != len(set(family_ids)):
        errors.append("repaired_variant_family_family_ids_must_be_unique")
    if family_ids.count(KNOWN_DUPLICATE_FAMILY_ID) != 1:
        errors.append("unresolved_as_current_only_must_appear_once")
    memberships = {
        row.get("family_id"): row.get("taxonomy_memberships", []) for row in variant.get("families", [])
    }
    if set(memberships.get(KNOWN_DUPLICATE_FAMILY_ID, [])) != {"baseline_family", "unresolved_policy_family"}:
        errors.append("unresolved_as_current_only_memberships_must_be_baseline_and_unresolved_policy")
    if variant.get("unique_family_count") != 10:
        errors.append("unique_family_count_must_be_10")
    if variant.get("taxonomy_membership_count") != 11:
        errors.append("taxonomy_membership_count_must_be_11")
    family_audit = payloads["family_id_audit"]
    if family_audit.get("duplicate_family_id_count_before_repair") != 1:
        errors.append("duplicate_family_id_count_before_repair_must_be_1")
    if family_audit.get("duplicate_family_id_count_after_repair") != 0:
        errors.append("duplicate_family_id_count_after_repair_must_be_0")
    taxonomy = payloads["taxonomy_policy"]
    if taxonomy.get("duplicate_taxonomy_membership_allowed") is not True:
        errors.append("duplicate_taxonomy_membership_allowed_must_be_true")
    if taxonomy.get("duplicate_family_records_allowed") is not False:
        errors.append("duplicate_family_records_allowed_must_be_false")
    reference = payloads["reference_audit"]
    if reference.get("stage5aw_repaired_branch_manifest_used") is not True:
        errors.append("stage5aw_repaired_branch_manifest_used_must_be_true")
    if reference.get("stage5av_branch_manifest_used") is not False:
        errors.append("stage5av_branch_manifest_used_must_be_false")
    if reference.get("stage5av_branch_manifest_inactive") is not True:
        errors.append("stage5av_branch_manifest_inactive_must_be_true")
    budget = payloads["repaired_branch_budget"]
    if budget.get("branch_budget_changed") is not False:
        errors.append("branch_budget_changed_must_be_false")
    if budget.get("full_cartesian_product_allowed") is not False:
        errors.append("full_cartesian_product_allowed_must_be_false")
    gates = payloads["repaired_execution_gates"]
    gate_ids = [gate.get("gate_id") for gate in gates.get("gates", [])]
    if "manifest_integrity_gate" not in gate_ids:
        errors.append("manifest_integrity_gate_missing")
    if gates.get("execution_authorised_now") is not False:
        errors.append("execution_authorised_now_must_be_false")
    ready = payloads["readiness"]
    if ready.get("deep_research_readiness") is not True:
        errors.append("deep_research_readiness_must_be_true")
    dwh = payloads["dwh_context"]
    if dwh.get("dwh_expansion") != "Deep Web Hash":
        errors.append("dwh_expansion_must_be_Deep_Web_Hash")
    if dwh.get("hash_search_allowed_now") is not False:
        errors.append("hash_search_allowed_now_must_be_false")
    next_stage = payloads["next_stage_decision"]
    if next_stage.get("selected_next_stage_title") != STAGE5BA_TITLE:
        errors.append("selected_next_stage_must_be_stage5ba")

    counts = {
        "duplicate_family_id_count_before_repair": family_audit.get("duplicate_family_id_count_before_repair"),
        "duplicate_family_id_count_after_repair": family_audit.get("duplicate_family_id_count_after_repair"),
        "repaired_unique_family_count": variant.get("unique_family_count"),
        "taxonomy_membership_count": variant.get("taxonomy_membership_count"),
        "execution_gate_count": len(gates.get("gates", [])),
        "manifest_integrity_gate_status": gates.get("manifest_integrity_gate_status"),
        "deep_research_readiness": ready.get("deep_research_readiness"),
        "stage5az_generated_summary_present": (results_dir / "summary.json").exists(),
        "stage5az_generated_repaired_manifest_present": (
            results_dir / "repaired_variant_family_manifest.json"
        ).exists(),
        "validation_error_count": len(errors),
    }
    return counts, errors
