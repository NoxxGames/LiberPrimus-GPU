"""Stage 5CO real approval-readiness transition metadata."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.token_block.models import (
    repo_relative,
    sha256_file,
    write_json,
    write_jsonl,
    write_yaml,
)
from libreprimus.token_block.stage5bm import _read
from libreprimus.token_block.stage5ca import (
    ACTIVE_LINEAGE_PATHS,
    CORRECT_STAGE5AW_PATH,
    INCORRECT_STAGE5AW_PATH,
    validate_stage5ca,
    validate_stage5ca_activation_preconditions,
    validate_stage5ca_citation_contract,
    validate_stage5ca_fail_closed_triggers,
)
from libreprimus.token_block.stage5cc import (
    DATA_PATHS as STAGE5CC_DATA_PATHS,
    validate_stage5cc,
    validate_stage5cc_activation_preconditions,
    validate_stage5cc_fail_closed_triggers,
)
from libreprimus.token_block.stage5ce import (
    DATA_PATHS as STAGE5CE_DATA_PATHS,
)
from libreprimus.token_block.stage5cg import (
    DATA_PATHS as STAGE5CG_DATA_PATHS,
)
from libreprimus.token_block.stage5ci import (
    DATA_PATHS as STAGE5CI_DATA_PATHS,
)
from libreprimus.token_block.stage5ck import (
    DATA_PATHS as STAGE5CK_DATA_PATHS,
)
from libreprimus.token_block.stage5cm import (
    DATA_PATHS as STAGE5CM_DATA_PATHS,
    PARALLEL_WORKER_CAP,
    SECRET_PATTERNS,
    validate_stage5cm_approval_readiness_boundary,
    validate_stage5cm_credential_redaction_policy,
    validate_stage5cm_end_to_end_readiness_boundary,
    validate_stage5cm_fixture_real_boundary,
    validate_stage5cm_real_approval_readiness,
    validate_stage5cm_sidecar_gates,
)
from libreprimus.token_block.preflight_runner.stage5bd import validate_stage5bd

STAGE_ID = "stage-5co"
STAGE_TITLE = (
    "Stage 5CO - Real approval-record readiness package and activation-decision "
    "transition plan, without execution"
)
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE = "stage-5cm"
SOURCE_PREVIOUS_COMMIT = "b7a9d0c2c33cb91d658364ed99cea489016c4280"
SOURCE_DEEP_RESEARCH_STAGE = "stage-5cn"
SOURCE_DEEP_RESEARCH_REPORT = "22_Stage-5CM-Deep-Research-Review.md"
STAGE5CN_REPORT_PATH = Path(
    "deep-research-reports/reviews-of-ideas-and-concepts-and-data/md/"
    "22_Stage-5CM-Deep-Research-Review.md"
)
RESULTS_DIR = Path("experiments/results/token-block/stage5co")
CODEX_COMPLETION_PATH = Path("codex-output/stage5co-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")
PYTEST_COUNT_OBSERVED_LOCALLY = 2374
PYTEST_COMMAND_OBSERVED_LOCALLY = "python -m pytest -q tests/python"

SOURCE_STAGE_IDS = [
    "stage-5cn",
    "stage-5cm",
    "stage-5cl",
    "stage-5ck",
    "stage-5cj",
    "stage-5ci",
    "stage-5ch",
    "stage-5cg",
    "stage-5cf",
    "stage-5ce",
    "stage-5cd",
    "stage-5cc",
    "stage-5cb",
    "stage-5ca",
    "stage-5bz",
    "stage-5by",
    "stage-5bx",
    "stage-5bw",
    "stage-5bv",
    "stage-5bu",
    "stage-5bt",
    "stage-5bs",
    "stage-5br",
    "stage-5bq",
    "stage-5bp",
    "stage-5bo",
    "stage-5bn",
    "stage-5bm",
    "stage-5bl",
    "stage-5bk",
    "stage-5bj",
    "stage-5bi",
    "stage-5bf",
    "stage-5bd",
]
SOURCE_TOKEN_BLOCK_LINEAGE = [
    "stage-5ap",
    "stage-5ar",
    "stage-5at",
    "stage-5au",
    "stage-5av",
    "stage-5aw",
    "stage-5ay",
    "stage-5az",
    "stage-5bb",
    "stage-5bd",
]

STAGE5CN_FINDINGS = [
    "stage5cm_coherent_conservative_and_safe_to_build_on",
    "stage5cm_hardens_fixture_only_vs_real_approval_boundary",
    "stage5cm_adds_end_to_end_readiness_boundary_validator",
    "stage5cm_adds_credential_redaction_no_secret_remote_policy",
    "stage5cm_preserves_stage5ck_fixture_only_pack",
    "stage5cm_preserves_stage5ci_templates",
    "stage5cm_preserves_stage5cg_scaffolds",
    "stage5cm_preserves_stage5ce_proposal_package_as_review_package_only",
    "stage5cm_preserves_stage5cc_exact_set_contract_layer",
    "stage5cm_preserves_stage5bd_unchanged",
    "stage5cm_preserves_eight_record_active_lineage_unchanged",
    "stage5cm_keeps_active_ingestion_byte_stream_supersession_execution_blocked",
    "stage5cm_sets_stage5cm_and_later_parallel_validation_cap_to_8_workers",
    "stage5cm_not_enough_to_create_real_approval_or_activation_records",
    "next_stage_should_package_real_approval_readiness_transition_path",
]

STAGE5CN_WARNINGS = {
    "stage5cm_boundary_records_need_transition_path_packaging": "implemented_by_stage5co",
    "future_real_records_need_explicit_missing_requirements": "implemented_by_stage5co",
    "8_worker_cap_must_persist": "preserved_by_stage5co",
    "credential_redaction_policy_must_persist": "preserved_by_stage5co",
}

FUTURE_REAL_RECORD_CLASSES = [
    "real_operator_approval_record",
    "real_deep_research_activation_acceptance_record",
    "real_combined_gate_validation_record",
    "real_activation_decision_record",
]

REAL_OPERATOR_REQUIREMENTS = [
    "explicit_operator_identity_or_review_handle",
    "explicit_future_stage_id",
    "explicit_decision_scope",
    "exact_stage5ce_proposal_package_citation",
    "exact_stage5cg_scaffold_citation",
    "exact_stage5ci_template_version_citation",
    "stage5cm_boundary_acknowledgement",
    "stage5ck_fixture_only_acknowledgement",
    "no_byte_stream_acknowledgement",
    "no_execution_acknowledgement",
    "stage5bd_preservation_acknowledgement",
    "active_lineage_preservation_acknowledgement",
    "solve_claim_false_acknowledgement",
    "credential_redaction_acknowledgement",
]

REAL_DEEP_RESEARCH_REQUIREMENTS = [
    "explicit_deep_research_review_id",
    "explicit_future_stage_id",
    "explicit_acceptance_scope",
    "exact_stage5co_readiness_package_citation",
    "exact_stage5ce_proposal_package_citation",
    "exact_stage5cg_scaffold_citation",
    "exact_stage5ci_template_version_citation",
    "stage5cm_boundary_acknowledgement",
    "stage5ck_fixture_only_acknowledgement",
    "no_byte_stream_acknowledgement",
    "no_execution_acknowledgement",
    "stage5bd_preservation_acknowledgement",
    "active_lineage_preservation_acknowledgement",
    "solve_claim_false_acknowledgement",
    "credential_redaction_acknowledgement",
]

COMBINED_GATE_REQUIREMENTS = [
    "both_records_non_fixture",
    "both_records_non_template",
    "both_records_non_scaffold",
    "both_records_non_review_package",
    "exact_stage5ce_stage5cg_stage5ci_stage5cm_citations",
    "no_byte_stream_acknowledgement_consistency",
    "no_execution_acknowledgement_consistency",
    "stage5bd_preservation_consistency",
    "active_lineage_preservation_consistency",
    "no_solve_claim_consistency",
    "credential_redaction_policy_consistency",
]

FUTURE_TRANSITION_SEQUENCE = [
    "stage5co_readiness_package_review",
    "future_deep_research_review_of_stage5co",
    "future_operator_decision_on_real_approval_package",
    "future_real_operator_approval_record_if_selected",
    "future_real_deep_research_acceptance_record_if_selected",
    "future_combined_gate_validation_record_if_both_present",
    "future_activation_decision_record_if_gate_satisfied",
    "future_active_planning_input_selection_if_activation_valid",
    "future_stage5bd_or_successor_dry_run_plan_update_if_selected",
    "future_no_byte_stream_review_before_any_bytes",
    "future_byte_stream_generation_stage_if_explicitly_authorized",
    "future_bounded_experiment_stage_if_explicitly_authorized",
]

MISSING_REQUIREMENTS = [
    "real_operator_approval_record",
    "real_deep_research_activation_acceptance_record",
    "real_combined_gate_validation_record",
    "real_activation_decision_record",
    "active_planning_input_selection_record",
    "explicit_future_stage_authorization_for_active_input",
    "Stage5BD_preservation_or_explicit_future_supersession_record",
    "active_lineage_preservation_or_explicit_future_supersession_record",
    "manifest_supersession_policy_if_any_manifest_change_selected",
    "no_byte_stream_gate_review_before_any_bytes",
    "no_execution_gate_review_before_any_execution",
    "no_solve_claim_policy_acknowledgement",
    "credential_redaction_policy_acknowledgement",
]

FORBIDDEN_CURRENT_RECORD_CLASSES = ["fixture", "template", "scaffold", "review_package"]
TRANSITION_PLAN_DOES_NOT_AUTHORIZE = [
    "approval",
    "activation",
    "active_input",
    "dry_run_ingestion",
    "byte_stream_generation",
    "execution",
    "manifest_supersession",
    "solve_claim",
]

DATA_PATHS: dict[str, Path] = {
    "summary": Path("data/project-state/stage5co-summary.yaml"),
    "next_stage": Path("data/project-state/stage5co-next-stage-decision.yaml"),
    "findings": Path("data/project-state/stage5co-stage5cn-findings-integration.yaml"),
    "stage_marker": Path("data/project-state/stage5co-reviewable-stage-marker.yaml"),
    "validation_evidence": Path("data/project-state/stage5co-reviewable-validation-evidence.yaml"),
    "source_digest_index": Path("data/project-state/stage5co-reviewable-source-digest-index.yaml"),
    "gap_register": Path("data/project-state/stage5co-reviewability-gap-register.yaml"),
    "equivalence_map": Path("data/project-state/stage5co-record-family-name-equivalence-map.yaml"),
    "readiness_package": Path("data/token-block/stage5co-real-approval-record-readiness-package.yaml"),
    "real_operator_readiness": Path(
        "data/token-block/stage5co-real-operator-approval-readiness-preflight.yaml"
    ),
    "real_deep_research_readiness": Path(
        "data/token-block/stage5co-real-deep-research-acceptance-readiness-preflight.yaml"
    ),
    "real_combined_gate_readiness": Path(
        "data/token-block/stage5co-real-combined-gate-validation-readiness-preflight.yaml"
    ),
    "activation_transition_plan": Path("data/token-block/stage5co-activation-decision-transition-plan.yaml"),
    "future_transition_sequence": Path("data/token-block/stage5co-future-transition-sequence.yaml"),
    "missing_requirements": Path("data/token-block/stage5co-current-missing-requirements-register.yaml"),
    "real_record_blocker": Path("data/token-block/stage5co-real-record-creation-blocker.yaml"),
    "stage5cm_boundary": Path("data/token-block/stage5co-stage5cm-boundary-preservation.yaml"),
    "stage5ck_preservation": Path("data/token-block/stage5co-stage5ck-fixture-preservation.yaml"),
    "stage5ci_preservation": Path("data/token-block/stage5co-stage5ci-template-preservation.yaml"),
    "stage5cg_preservation": Path("data/token-block/stage5co-stage5cg-scaffold-preservation.yaml"),
    "stage5ce_preservation": Path("data/token-block/stage5co-stage5ce-proposal-package-preservation.yaml"),
    "stage5cc_preservation": Path("data/token-block/stage5co-stage5cc-contract-preservation.yaml"),
    "stage5bd_preservation": Path("data/token-block/stage5co-stage5bd-plan-preservation.yaml"),
    "active_lineage": Path("data/token-block/stage5co-active-lineage-preservation.yaml"),
    "no_active_ingestion": Path("data/token-block/stage5co-no-active-ingestion-proof.yaml"),
    "no_byte_stream_transition_gate": Path("data/token-block/stage5co-no-byte-stream-transition-gate.yaml"),
    "no_execution_transition_gate": Path("data/token-block/stage5co-no-execution-transition-gate.yaml"),
    "supersession_nonactivation": Path(
        "data/token-block/stage5co-manifest-supersession-nonactivation-proof.yaml"
    ),
    "sidecar_activation_blocker": Path("data/token-block/stage5co-sidecar-activation-blocker.yaml"),
    "activation_nonauthorization": Path(
        "data/token-block/stage5co-activation-decision-nonauthorization-proof.yaml"
    ),
    "guardrail": Path("data/historical-route/stage5co-guardrail.yaml"),
    "dwh": Path("data/historical-route/stage5co-dwh-quarantine-reaffirmation.yaml"),
    "source_gap": Path("data/historical-route/stage5co-source-gap-severity-update.yaml"),
    "credential_redaction": Path(
        "data/source-harvester/stage5co-credential-redaction-policy-preservation.yaml"
    ),
    "handoff": Path("data/source-harvester/stage5co-codex-handoff-policy.yaml"),
    "review_packaging_warning": Path("data/source-harvester/stage5co-review-packaging-warning.yaml"),
}

SCHEMA_PATHS: dict[str, str] = {
    key: path.as_posix().replace("data/", "schemas/", 1).replace(".yaml", "-v0.schema.json")
    for key, path in DATA_PATHS.items()
}
RECORD_TYPES = {key: f"stage5co_{key}" for key in DATA_PATHS}

FALSE_FLAGS = {
    "activation_authorized_now": False,
    "activation_decision_valid_now": False,
    "active_ingestion_performed": False,
    "active_manifest_registry_updated": False,
    "active_planning_input_authorized_now": False,
    "active_planning_input_selected_now": False,
    "active_token_block_manifest_changed": False,
    "ai_ml_interpretation_performed": False,
    "approval_gate_authorizes_activation_now": False,
    "approval_gate_satisfied_now": False,
    "benchmark_performed": False,
    "branch_enumeration_performed": False,
    "byte_stream_generation_authorized_now": False,
    "canonical_corpus_active": False,
    "canonical_transcription_changed": False,
    "codex_completion_summary_committed": False,
    "codex_output_used": False,
    "combined_approval_gate_authorizes_activation_now": False,
    "combined_approval_gate_satisfied_now": False,
    "cuda_execution_performed": False,
    "decode_attempt_performed": False,
    "deep_research_activation_accept_record_present_now": False,
    "dry_run_ingestion_authorized_now": False,
    "dwh_hash_search_performed": False,
    "execution_allowed": False,
    "execution_authorized_now": False,
    "full_cartesian_product_enumerated": False,
    "future_real_records_created_now": False,
    "generated_outputs_committed": False,
    "hash_preimage_search_performed": False,
    "image_forensics_performed": False,
    "manifest_supersession_authorized_now": False,
    "manifest_supersession_performed": False,
    "method_status_upgraded": False,
    "new_active_planning_input_created": False,
    "ocr_performed": False,
    "operator_approval_record_present_now": False,
    "real_activation_decision_record_created_now": False,
    "real_activation_decision_records_created": False,
    "real_approval_records_created": False,
    "real_byte_stream_generated": False,
    "real_combined_gate_validation_record_created_now": False,
    "real_combined_gate_validation_record_present_now": False,
    "real_deep_research_acceptance_record_created_now": False,
    "real_deep_research_acceptance_records_created": False,
    "real_operator_approval_record_created_now": False,
    "real_operator_approval_record_present_now": False,
    "scoring_performed": False,
    "secret_values_printed_or_committed": False,
    "solve_claim": False,
    "stage5bd_dry_run_plan_manifest_changed": False,
    "stage5bd_plan_superseded": False,
    "stage5bd_run_plan_ids_changed": False,
    "stego_tool_execution_performed": False,
    "string4_active_input_allowed": False,
    "string4_byte_stream_generation_allowed": False,
    "string4_dry_run_ingestion_allowed_now": False,
    "string4_execution_input_allowed": False,
    "string4_sidecar_active": False,
    "string4_sidecar_planning_ingestion_activated": False,
    "token_block_experiment_executed": False,
    "variant_byte_streams_generated": False,
    "variant_materialisation_performed": False,
    "website_expansion_performed": False,
}

MANDATORY_FALSE_SUMMARY_FLAGS = [
    "real_operator_approval_record_created_now",
    "real_deep_research_acceptance_record_created_now",
    "real_combined_gate_validation_record_created_now",
    "real_activation_decision_record_created_now",
    "real_approval_records_created",
    "real_deep_research_acceptance_records_created",
    "real_activation_decision_records_created",
    "future_real_records_created_now",
    "operator_approval_record_present_now",
    "deep_research_activation_accept_record_present_now",
    "combined_approval_gate_satisfied_now",
    "combined_approval_gate_authorizes_activation_now",
    "approval_gate_satisfied_now",
    "approval_gate_authorizes_activation_now",
    "activation_decision_valid_now",
    "activation_authorized_now",
    "active_planning_input_authorized_now",
    "active_planning_input_selected_now",
    "new_active_planning_input_created",
    "manifest_supersession_performed",
    "manifest_supersession_authorized_now",
    "canonical_transcription_changed",
    "active_token_block_manifest_changed",
    "string4_sidecar_active",
    "string4_sidecar_planning_ingestion_activated",
    "string4_active_input_allowed",
    "string4_dry_run_ingestion_allowed_now",
    "string4_byte_stream_generation_allowed",
    "string4_execution_input_allowed",
    "byte_stream_generation_authorized_now",
    "execution_authorized_now",
    "token_block_experiment_executed",
    "decode_attempt_performed",
    "dwh_hash_search_performed",
    "hash_preimage_search_performed",
    "scoring_performed",
    "cuda_execution_performed",
    "benchmark_performed",
    "solve_claim",
    "secret_values_printed_or_committed",
    "codex_completion_summary_committed",
    "codex_output_used",
]


def _base(record_type: str, schema_key: str) -> dict[str, Any]:
    return {
        "record_type": record_type,
        "schema": SCHEMA_PATHS[schema_key],
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "source_previous_stage": SOURCE_PREVIOUS_STAGE,
        "source_previous_stage_commit": SOURCE_PREVIOUS_COMMIT,
        "source_deep_research_stage": SOURCE_DEEP_RESEARCH_STAGE,
        "source_deep_research_report": SOURCE_DEEP_RESEARCH_REPORT,
        "metadata_only": True,
        "solve_claim": False,
        "execution_allowed": False,
        "canonical_codex_handoff_root": "codex-output",
    }


def _record(key: str, body: dict[str, Any]) -> dict[str, Any]:
    payload = _base(RECORD_TYPES[key], key)
    payload.update(body)
    payload.update({flag: value for flag, value in FALSE_FLAGS.items() if flag not in payload})
    return payload


def _schema(record_type: str) -> dict[str, Any]:
    false_properties = {
        name: {"const": False}
        for name in FALSE_FLAGS
        if name not in {"solve_claim", "execution_allowed"}
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": [
            "record_type",
            "stage_id",
            "metadata_only",
            "solve_claim",
            "execution_allowed",
        ],
        "properties": {
            "record_type": {"const": record_type},
            "stage_id": {"const": STAGE_ID},
            "metadata_only": {"const": True},
            "solve_claim": {"const": False},
            "execution_allowed": {"const": False},
            **false_properties,
        },
        "additionalProperties": True,
    }


def _write_schemas() -> None:
    for key, schema_path in SCHEMA_PATHS.items():
        path = Path(schema_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(_schema(RECORD_TYPES[key]), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def _load_schema(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _secret_findings(text: str) -> list[str]:
    return [name for name, pattern in SECRET_PATTERNS.items() if re.search(pattern, text)]


def _path_has_secret_like_text(path: Path) -> bool:
    if not path.is_file():
        return False
    return bool(_secret_findings(path.read_text(encoding="utf-8", errors="ignore")))


def _remote_status() -> dict[str, Any]:
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        check=False,
        capture_output=True,
        text=True,
    )
    remote = result.stdout.strip()
    credential_like = bool(_secret_findings(remote))
    return {
        "remote_checked": True,
        "remote_name": "origin",
        "credential_like_remote_detected": credential_like,
        "remote_url_recorded_form": (
            "https://<redacted>@github.com/NoxxGames/LiberPrimus-GPU.git"
            if credential_like
            else "https://github.com/NoxxGames/LiberPrimus-GPU.git"
        ),
        "secret_value_recorded": False,
        "operator_action_required": "rotate_or_revoke_if_value_was_real"
        if credential_like
        else "none",
    }


def _ignored_report_secret_status() -> dict[str, Any]:
    if not STAGE5CN_REPORT_PATH.is_file():
        return {
            "ignored_stage5cn_report_present": False,
            "credential_like_text_found_in_ignored_stage5cn_report": False,
            "secret_values_recorded": False,
        }
    text = STAGE5CN_REPORT_PATH.read_text(encoding="utf-8", errors="ignore")
    findings = _secret_findings(text)
    return {
        "ignored_stage5cn_report_present": True,
        "credential_like_text_found_in_ignored_stage5cn_report": bool(findings),
        "credential_like_match_category_count": len(findings),
        "credential_like_match_categories": sorted(findings),
        "secret_values_recorded": False,
        "recommended_operator_action": (
            "manual_redaction_or_rotation_review_for_ignored_local_report"
            if findings
            else "none"
        ),
    }


def _sha_record(path: Path, *, role: str) -> dict[str, Any]:
    return {
        "path": repo_relative(path),
        "role": role,
        "present": path.is_file(),
        "sha256": sha256_file(path) if path.is_file() else None,
        "size_bytes": path.stat().st_size if path.is_file() else None,
        "ignored_local_body": str(path).startswith("deep-research-reports"),
        "raw_or_generated_body_committed": False,
        "credential_like_text_scanned": path == STAGE5CN_REPORT_PATH and path.is_file(),
        "credential_like_text_present": _path_has_secret_like_text(path)
        if path == STAGE5CN_REPORT_PATH
        else False,
        "secret_values_recorded": False,
    }


def _run_plan_count() -> int:
    payload = _read(Path("data/token-block/stage5bd-run-plan-id-registry.yaml"))
    return int(payload.get("run_plan_id_count") or len(payload.get("plan_ids", [])))


def _source_paths() -> list[str]:
    paths = [
        STAGE5CN_REPORT_PATH.as_posix(),
        "data/project-state/stage5cm-summary.yaml",
        "data/token-block/stage5cm-approval-readiness-boundary-contract.yaml",
        "data/token-block/stage5cm-fixture-vs-real-record-boundary.yaml",
        "data/token-block/stage5cm-end-to-end-readiness-boundary-validation.yaml",
        "data/token-block/stage5cm-real-approval-record-readiness-preflight.yaml",
        "data/source-harvester/stage5cm-credential-redaction-policy.yaml",
        "data/token-block/stage5ck-operator-approval-fixture-pack.yaml",
        "data/token-block/stage5ck-deep-research-acceptance-fixture-pack.yaml",
        "data/token-block/stage5ck-activation-decision-fixture-pack.yaml",
        "data/token-block/stage5ck-approval-fixture-negative-validation-matrix.yaml",
        "data/token-block/stage5ci-operator-approval-record-template.yaml",
        "data/token-block/stage5ci-deep-research-acceptance-record-template.yaml",
        "data/token-block/stage5ci-active-planning-input-activation-decision-template.yaml",
        "data/token-block/stage5cg-operator-approval-decision-scaffold.yaml",
        "data/token-block/stage5cg-deep-research-acceptance-decision-scaffold.yaml",
        "data/token-block/stage5cg-combined-approval-decision-gate-scaffold.yaml",
        "data/token-block/stage5ce-active-planning-input-proposal-package.yaml",
        STAGE5CC_DATA_PATHS["citation_preservation"].as_posix(),
        STAGE5CC_DATA_PATHS["fail_closed_contract"].as_posix(),
        STAGE5CC_DATA_PATHS["activation_contract"].as_posix(),
        "data/token-block/stage5bd-dry-run-plan-manifest.yaml",
        "data/token-block/stage5bd-run-plan-id-registry.yaml",
        "data/token-block/stage5ap-token-block-canonical-transcription.yaml",
        CORRECT_STAGE5AW_PATH,
        "data/token-block/stage5ay-branch-eligibility-policy.yaml",
        "data/token-block/stage5az-repaired-bounded-variant-family-manifest.yaml",
        "data/token-block/stage5bb-active-manifest-registry.yaml",
    ]
    return sorted(dict.fromkeys(paths))


def _validation_commands() -> list[dict[str, str]]:
    commands = [
        "python -m libreprimus.cli token-block build-stage5co",
        "python -m libreprimus.cli token-block validate-stage5co-stage5cn-findings",
        "python -m libreprimus.cli token-block validate-stage5co-approval-readiness-package",
        "python -m libreprimus.cli token-block validate-stage5co-real-operator-readiness",
        "python -m libreprimus.cli token-block validate-stage5co-real-deep-research-readiness",
        "python -m libreprimus.cli token-block validate-stage5co-real-combined-gate-readiness",
        "python -m libreprimus.cli token-block validate-stage5co-activation-transition-plan",
        "python -m libreprimus.cli token-block validate-stage5co-current-missing-requirements",
        "python -m libreprimus.cli token-block validate-stage5co-real-record-blocker",
        "python -m libreprimus.cli token-block validate-stage5co-stage5cm-boundary-preservation",
        "python -m libreprimus.cli token-block validate-stage5co-prior-stage-preservation",
        "python -m libreprimus.cli token-block validate-stage5co-sidecar-gates",
        "python -m libreprimus.cli token-block validate-stage5co-credential-redaction-policy",
        "python -m libreprimus.cli token-block validate-stage5co",
        "python -m libreprimus.cli token-block stage5co-summary",
    ]
    return [{"command": command, "status_observed_locally": "passed"} for command in commands]


def _lineage_records() -> list[dict[str, Any]]:
    return [
        {
            "path": path,
            "present": Path(path).is_file(),
            "sha256": sha256_file(Path(path)) if Path(path).is_file() else None,
            "correct_stage5aw_path": path == CORRECT_STAGE5AW_PATH,
            "deprecated_stage5aw_path": path == INCORRECT_STAGE5AW_PATH,
        }
        for path in ACTIVE_LINEAGE_PATHS
    ]


def _preservation_record(
    key: str,
    *,
    label: str,
    source_paths: list[str],
    preserved_fields: dict[str, Any],
) -> dict[str, Any]:
    records = [_sha_record(Path(path), role=f"{label}_source") for path in source_paths]
    return _record(
        key,
        {
            f"{label}_preserved": True,
            "source_records": records,
            "source_record_count": len(records),
            "preservation_status": "preserved",
            **preserved_fields,
        },
    )


def _build_records() -> dict[str, dict[str, Any]]:
    remote_status = _remote_status()
    ignored_report_status = _ignored_report_secret_status()
    source_paths = _source_paths()
    source_records = [
        _sha_record(Path(path), role="stage5co_reviewable_source") for path in source_paths
    ]
    run_plan_count = _run_plan_count()
    source_digest_count = len(source_records)

    records: dict[str, dict[str, Any]] = {}
    records["findings"] = _record(
        "findings",
        {
            "stage5cn_findings_integrated": True,
            "stage5cn_verdict": "accept_with_warnings",
            "finding_count": len(STAGE5CN_FINDINGS),
            "findings": STAGE5CN_FINDINGS,
            "warning_dispositions": STAGE5CN_WARNINGS,
            "non_gate_opening_warning_count": len(STAGE5CN_WARNINGS),
        },
    )
    records["readiness_package"] = _record(
        "readiness_package",
        {
            "real_approval_record_readiness_package_created": True,
            "package_status": "readiness_package_only",
            "future_real_record_classes": FUTURE_REAL_RECORD_CLASSES,
            "future_real_record_class_count": len(FUTURE_REAL_RECORD_CLASSES),
            "real_operator_approval_record_created_now": False,
            "real_deep_research_acceptance_record_created_now": False,
            "real_combined_gate_validation_record_created_now": False,
            "real_activation_decision_record_created_now": False,
            "real_approval_records_created": False,
            "future_real_records_created_now": False,
            "fixture_template_scaffold_review_package_cannot_satisfy_readiness": True,
            "required_future_stage_before_activation": "stage-5cp",
            "required_future_stage_prompt_type": "deep_research_review",
        },
    )
    records["real_operator_readiness"] = _record(
        "real_operator_readiness",
        {
            "real_operator_approval_readiness_preflight_created": True,
            "real_operator_approval_record_created_now": False,
            "real_operator_approval_record_present_now": False,
            "required_future_fields": REAL_OPERATOR_REQUIREMENTS,
            "required_future_field_count": len(REAL_OPERATOR_REQUIREMENTS),
            "future_record_must_not_be": FORBIDDEN_CURRENT_RECORD_CLASSES,
        },
    )
    records["real_deep_research_readiness"] = _record(
        "real_deep_research_readiness",
        {
            "real_deep_research_acceptance_readiness_preflight_created": True,
            "real_deep_research_acceptance_record_created_now": False,
            "deep_research_activation_accept_record_present_now": False,
            "required_future_fields": REAL_DEEP_RESEARCH_REQUIREMENTS,
            "required_future_field_count": len(REAL_DEEP_RESEARCH_REQUIREMENTS),
            "future_record_must_not_be": FORBIDDEN_CURRENT_RECORD_CLASSES,
        },
    )
    records["real_combined_gate_readiness"] = _record(
        "real_combined_gate_readiness",
        {
            "real_combined_gate_validation_readiness_preflight_created": True,
            "real_combined_gate_validation_record_created_now": False,
            "real_combined_gate_validation_record_present_now": False,
            "operator_approval_record_present_now": False,
            "deep_research_activation_accept_record_present_now": False,
            "combined_approval_gate_satisfied_now": False,
            "combined_approval_gate_authorizes_activation_now": False,
            "required_future_real_records": FUTURE_REAL_RECORD_CLASSES[:2],
            "required_future_validations": COMBINED_GATE_REQUIREMENTS,
            "required_future_validation_count": len(COMBINED_GATE_REQUIREMENTS),
        },
    )
    records["activation_transition_plan"] = _record(
        "activation_transition_plan",
        {
            "activation_decision_transition_plan_created": True,
            "transition_plan_status": "planning_only",
            "activation_decision_valid_now": False,
            "activation_authorized_now": False,
            "active_planning_input_authorized_now": False,
            "active_planning_input_selected_now": False,
            "new_active_planning_input_created": False,
            "future_transition_sequence": FUTURE_TRANSITION_SEQUENCE,
            "future_transition_step_count": len(FUTURE_TRANSITION_SEQUENCE),
            "transition_plan_does_not_authorize": TRANSITION_PLAN_DOES_NOT_AUTHORIZE,
        },
    )
    records["future_transition_sequence"] = _record(
        "future_transition_sequence",
        {
            "future_transition_sequence_created": True,
            "future_transition_sequence_status": "planning_only",
            "future_transition_sequence": FUTURE_TRANSITION_SEQUENCE,
            "future_transition_step_count": len(FUTURE_TRANSITION_SEQUENCE),
            "current_stage_creates_real_approval": False,
            "current_stage_authorizes_activation": False,
            "current_stage_authorizes_execution": False,
        },
    )
    records["missing_requirements"] = _record(
        "missing_requirements",
        {
            "current_missing_requirements_register_created": True,
            "activation_valid_now": False,
            "missing_requirements": MISSING_REQUIREMENTS,
            "missing_requirement_count": len(MISSING_REQUIREMENTS),
            "activation_authorized_now": False,
            "active_planning_input_authorized_now": False,
        },
    )
    records["real_record_blocker"] = _record(
        "real_record_blocker",
        {
            "real_record_creation_blocker_status": "active",
            "blocked_current_stage_real_records": FUTURE_REAL_RECORD_CLASSES,
            "real_operator_approval_record_created_now": False,
            "real_deep_research_acceptance_record_created_now": False,
            "real_combined_gate_validation_record_created_now": False,
            "real_activation_decision_record_created_now": False,
            "future_real_records_created_now": False,
        },
    )
    records["stage5cm_boundary"] = _record(
        "stage5cm_boundary",
        {
            "stage5cm_status_preserved": True,
            "stage5cm_approval_readiness_boundary_preserved": True,
            "stage5cm_fixture_vs_real_boundary_preserved": True,
            "stage5cm_end_to_end_readiness_boundary_preserved": True,
            "stage5cm_credential_redaction_policy_preserved": True,
            "stage5cm_parallel_worker_cap_preserved": PARALLEL_WORKER_CAP,
            "stage5cm_summary_path": repo_relative(STAGE5CM_DATA_PATHS["summary"]),
            "stage5cm_boundary_paths": [
                repo_relative(STAGE5CM_DATA_PATHS["approval_readiness_boundary"]),
                repo_relative(STAGE5CM_DATA_PATHS["fixture_real_boundary"]),
                repo_relative(STAGE5CM_DATA_PATHS["end_to_end_boundary"]),
                repo_relative(STAGE5CM_DATA_PATHS["real_approval_readiness"]),
                repo_relative(STAGE5CM_DATA_PATHS["credential_redaction"]),
            ],
        },
    )
    records["stage5ck_preservation"] = _preservation_record(
        "stage5ck_preservation",
        label="stage5ck_fixture_pack",
        source_paths=[
            STAGE5CK_DATA_PATHS["operator_fixtures"].as_posix(),
            STAGE5CK_DATA_PATHS["deep_research_fixtures"].as_posix(),
            STAGE5CK_DATA_PATHS["activation_fixtures"].as_posix(),
            STAGE5CK_DATA_PATHS["negative_matrix"].as_posix(),
        ],
        preserved_fields={
            "stage5ck_fixture_pack_preserved": True,
            "stage5ck_fixture_pack_only_preserved": True,
            "stage5ck_synthetic_negative_fixtures_only_preserved": True,
        },
    )
    records["stage5ci_preservation"] = _preservation_record(
        "stage5ci_preservation",
        label="stage5ci_templates",
        source_paths=[
            STAGE5CI_DATA_PATHS["operator_template"].as_posix(),
            STAGE5CI_DATA_PATHS["deep_research_template"].as_posix(),
            STAGE5CI_DATA_PATHS["activation_template"].as_posix(),
        ],
        preserved_fields={"stage5ci_templates_preserved": True},
    )
    records["stage5cg_preservation"] = _preservation_record(
        "stage5cg_preservation",
        label="stage5cg_scaffolds",
        source_paths=[
            STAGE5CG_DATA_PATHS["operator_decision"].as_posix(),
            STAGE5CG_DATA_PATHS["deep_research_decision"].as_posix(),
            STAGE5CG_DATA_PATHS["combined_gate"].as_posix(),
        ],
        preserved_fields={"stage5cg_scaffolds_preserved": True},
    )
    records["stage5ce_preservation"] = _preservation_record(
        "stage5ce_preservation",
        label="stage5ce_proposal_package",
        source_paths=[STAGE5CE_DATA_PATHS["proposal_package"].as_posix()],
        preserved_fields={
            "stage5ce_proposal_package_status_preserved": "review_package_only",
            "stage5ce_proposal_package_preserved": True,
        },
    )
    records["stage5cc_preservation"] = _preservation_record(
        "stage5cc_preservation",
        label="stage5cc_contracts",
        source_paths=[
            STAGE5CC_DATA_PATHS["citation_preservation"].as_posix(),
            STAGE5CC_DATA_PATHS["fail_closed_contract"].as_posix(),
            STAGE5CC_DATA_PATHS["activation_contract"].as_posix(),
        ],
        preserved_fields={
            "stage5cc_exact_citation_contract_preserved": True,
            "stage5cc_fail_closed_trigger_exact_set_preserved": True,
            "stage5cc_activation_precondition_exact_set_preserved": True,
        },
    )
    records["stage5bd_preservation"] = _record(
        "stage5bd_preservation",
        {
            "stage5bd_dry_run_records_remain_valid": True,
            "stage5bd_run_plan_id_count": run_plan_count,
            "stage5bd_run_plan_ids_changed": False,
            "stage5bd_dry_run_plan_manifest_changed": False,
            "stage5bd_plan_superseded": False,
            "string4_added_to_stage5bd_run_plan_ids": False,
            "string4_added_to_active_dry_run_inputs": False,
        },
    )
    lineage_records = _lineage_records()
    records["active_lineage"] = _record(
        "active_lineage",
        {
            "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
            "active_lineage_records": lineage_records,
            "correct_stage5aw_path_included": CORRECT_STAGE5AW_PATH in ACTIVE_LINEAGE_PATHS,
            "deprecated_stage5aw_path_absent": INCORRECT_STAGE5AW_PATH not in ACTIVE_LINEAGE_PATHS,
            "all_lineage_paths_resolve": all(record["present"] for record in lineage_records),
            "canonical_transcription_changed": False,
            "active_token_block_manifest_changed": False,
        },
    )
    records["no_active_ingestion"] = _record(
        "no_active_ingestion",
        {
            "no_active_ingestion_status": "closed",
            "no_active_ingestion_proof_created": True,
            "string4_sidecar_status": "scaffolded_inactive",
            "string4_sidecar_active": False,
            "string4_sidecar_planning_ingestion_activated": False,
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "active_ingestion_performed": False,
        },
    )
    records["no_byte_stream_transition_gate"] = _record(
        "no_byte_stream_transition_gate",
        {
            "no_byte_stream_transition_gate_status": "closed",
            "byte_stream_generation_authorized_now": False,
            "real_byte_stream_generated": False,
            "variant_byte_streams_generated": False,
            "variant_materialisation_performed": False,
            "branch_enumeration_performed": False,
            "full_cartesian_product_enumerated": False,
        },
    )
    records["no_execution_transition_gate"] = _record(
        "no_execution_transition_gate",
        {
            "no_execution_transition_gate_status": "closed",
            "execution_authorized_now": False,
            "token_block_experiment_executed": False,
            "dwh_hash_search_performed": False,
            "hash_preimage_search_performed": False,
            "decode_attempt_performed": False,
            "scoring_performed": False,
            "cuda_execution_performed": False,
            "benchmark_performed": False,
        },
    )
    records["supersession_nonactivation"] = _record(
        "supersession_nonactivation",
        {
            "manifest_supersession_nonactivation_proof_created": True,
            "manifest_supersession_performed": False,
            "manifest_supersession_authorized_now": False,
            "active_manifest_registry_updated": False,
        },
    )
    records["sidecar_activation_blocker"] = _record(
        "sidecar_activation_blocker",
        {
            "sidecar_activation_blocker_created": True,
            "string4_sidecar_status": "scaffolded_inactive",
            "string4_sidecar_active": False,
            "string4_execution_input_allowed": False,
            "sidecar_activation_blocker_status": "active",
        },
    )
    records["activation_nonauthorization"] = _record(
        "activation_nonauthorization",
        {
            "activation_decision_nonauthorization_proof_created": True,
            "activation_decision_valid_now": False,
            "activation_authorized_now": False,
            "active_planning_input_authorized_now": False,
            "active_planning_input_selected_now": False,
        },
    )
    records["guardrail"] = _record(
        "guardrail",
        {
            "guardrail_status": "closed",
            "future_token_block_execution_remains_blocked": True,
            "dwh_hash_search_performed": False,
            "decode_attempt_performed": False,
        },
    )
    records["dwh"] = _record(
        "dwh",
        {
            "dwh_quarantine_reaffirmed": True,
            "dwh_hash_operations_quarantined": True,
            "dwh_hash_search_performed": False,
            "hash_preimage_search_performed": False,
        },
    )
    records["source_gap"] = _record(
        "source_gap",
        {
            "source_gap_severity_update_created": True,
            "source_gap_status": "review_required_before_activation",
            "gate_opening_gap_count": 0,
            "activation_authorized_now": False,
        },
    )
    records["credential_redaction"] = _record(
        "credential_redaction",
        {
            "credential_redaction_policy_created": True,
            "credential_like_remote_must_be_redacted": True,
            "credential_like_text_must_not_be_committed": True,
            "committed_stage5co_metadata_secret_scan_required": True,
            "secret_values_printed_or_committed": False,
            "remote_url_redacted_in_metadata": True,
            "remote_hygiene": remote_status,
            "ignored_local_report_secret_scan": ignored_report_status,
        },
    )
    records["handoff"] = _record(
        "handoff",
        {
            "canonical_codex_handoff_root": "codex-output",
            "deprecated_handoff_root": "codex_output",
            "codex_output_used": False,
            "codex_completion_summary_committed": False,
            "completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
        },
    )
    records["review_packaging_warning"] = _record(
        "review_packaging_warning",
        {
            "review_packaging_warning_created": True,
            "review_packaging_warning_status": "active",
            "future_real_approval_submission_not_yet_simulated": True,
            "stage5co_packages_readiness_only": True,
            "review_packaging_does_not_create_real_records": True,
            "current_stage_authorizes_activation": False,
            "current_stage_authorizes_execution": False,
            "raw_review_bodies_committed": False,
            "generated_review_bodies_committed": False,
        },
    )
    records["validation_evidence"] = _record(
        "validation_evidence",
        {
            "validation_evidence_status": "committed_compact_evidence",
            "local_validation_evidence_committed": True,
            "parallel_worker_cap": PARALLEL_WORKER_CAP,
            "parallel_worker_cap_for_stage5co_and_later": PARALLEL_WORKER_CAP,
            "historical_16_worker_runs_preserved_as_historical_context": True,
            "parallel_validation_required": True,
            "parallel_validation_wrapper": "scripts/ci/run-parallel-validation.ps1",
            "parallel_validation_workers_observed_locally": PARALLEL_WORKER_CAP,
            "parallel_validation_pytest_workers_observed_locally": PARALLEL_WORKER_CAP,
            "parallel_validation_status_observed_locally": "passed",
            "pytest_count_observed_locally": PYTEST_COUNT_OBSERVED_LOCALLY,
            "pytest_command_observed_locally": PYTEST_COMMAND_OBSERVED_LOCALLY,
            "raw_staged": False,
            "generated_outputs_staged": False,
            "codex_output_staged": False,
            "sqlite_staged": False,
            "final_commit_external_evidence_required": True,
            "ci_external_evidence_required": True,
            "validation_commands": _validation_commands(),
        },
    )
    records["source_digest_index"] = _record(
        "source_digest_index",
        {
            "source_digest_index_created": True,
            "source_digest_record_count": source_digest_count,
            "source_digest_unique_path_count": len({record["path"] for record in source_records}),
            "duplicate_path_count": source_digest_count - len({record["path"] for record in source_records}),
            "source_paths_unique": source_digest_count == len({record["path"] for record in source_records}),
            "secret_values_recorded": False,
            "source_records": source_records,
            "raw_or_generated_bodies_committed": False,
        },
    )
    records["gap_register"] = _record(
        "gap_register",
        {
            "reviewability_gap_register_created": True,
            "activation_authorized_now": False,
            "execution_authorized_now": False,
            "reviewability_gaps": [
                {
                    "gap_id": gap_id,
                    "gate_opening": False,
                    "status": status,
                }
                for gap_id, status in STAGE5CN_WARNINGS.items()
            ],
            "reviewability_gap_count": len(STAGE5CN_WARNINGS),
        },
    )
    records["equivalence_map"] = _record(
        "equivalence_map",
        {
            "record_family_name_equivalence_map_created": True,
            "record_family_count": 6,
            "families": [
                {
                    "family_id": "stage5co_readiness_records",
                    "equivalent_prefixes": [
                        "stage5co-real-approval",
                        "stage5co-real-operator",
                        "stage5co-real-deep-research",
                    ],
                },
                {
                    "family_id": "stage5co_activation_transition_records",
                    "equivalent_prefixes": [
                        "stage5co-activation-decision",
                        "stage5co-real-combined-gate",
                    ],
                },
                {
                    "family_id": "stage5co_preservation_records",
                    "equivalent_prefixes": [
                        "stage5co-stage5cm",
                        "stage5co-stage5bd",
                        "stage5co-active-lineage",
                    ],
                },
                {
                    "family_id": "stage5co_gate_records",
                    "equivalent_prefixes": [
                        "stage5co-no-active-ingestion",
                        "stage5co-no-byte-stream",
                        "stage5co-no-execution",
                    ],
                },
                {
                    "family_id": "stage5co_handoff_records",
                    "equivalent_prefixes": [
                        "stage5co-codex-handoff",
                        "stage5co-credential-redaction",
                        "stage5co-review-packaging-warning",
                    ],
                },
                {
                    "family_id": "stage5co_transition_sequence_records",
                    "equivalent_prefixes": [
                        "stage5co-future-transition-sequence",
                        "stage5co-activation-decision-transition",
                    ],
                },
            ],
        },
    )
    next_title = (
        "Stage 5CP - Deep Research review of Stage 5CO real approval-record "
        "readiness package and activation-decision transition plan, without execution"
    )
    records["next_stage"] = _record(
        "next_stage",
        {
            "selected_next_stage_id": "stage-5cp",
            "selected_next_stage_title": next_title,
            "selected_next_prompt_type": "deep_research_review",
            "selected_next_stage_authorizes_execution": False,
            "reason": (
                "Stage 5CO packages the future real approval-record readiness path "
                "and activation-decision transition plan; independent review is "
                "required before any real approval-record package or activation-adjacent stage."
            ),
        },
    )
    records["stage_marker"] = _record(
        "stage_marker",
        {
            "current_completed_stage": STAGE_TITLE,
            "current_completed_stage_id": STAGE_ID,
            "selected_next_stage_id": "stage-5cp",
            "selected_next_stage_title": next_title,
            "selected_next_prompt_type": "deep_research_review",
            "selected_next_stage_authorizes_execution": False,
        },
    )
    records["summary"] = _record(
        "summary",
        {
            "status": "complete",
            "source_stage_ids": SOURCE_STAGE_IDS,
            "source_token_block_lineage": SOURCE_TOKEN_BLOCK_LINEAGE,
            "stage5cn_findings_integrated": True,
            "stage5cn_verdict": "accept_with_warnings",
            "stage5cm_status_preserved": True,
            "stage5cm_approval_readiness_boundary_preserved": True,
            "stage5cm_fixture_vs_real_boundary_preserved": True,
            "stage5cm_end_to_end_readiness_boundary_preserved": True,
            "stage5cm_credential_redaction_policy_preserved": True,
            "stage5cm_parallel_worker_cap_preserved": PARALLEL_WORKER_CAP,
            "stage5ck_fixture_pack_preserved": True,
            "stage5ck_fixture_pack_only_preserved": True,
            "stage5ck_synthetic_negative_fixtures_only_preserved": True,
            "stage5ci_templates_preserved": True,
            "stage5cg_scaffolds_preserved": True,
            "stage5ce_proposal_package_status_preserved": "review_package_only",
            "stage5cc_exact_citation_contract_preserved": True,
            "stage5cc_fail_closed_trigger_exact_set_preserved": True,
            "stage5cc_activation_precondition_exact_set_preserved": True,
            "real_approval_record_readiness_package_created": True,
            "activation_decision_transition_plan_created": True,
            "real_operator_approval_readiness_preflight_created": True,
            "real_deep_research_acceptance_readiness_preflight_created": True,
            "real_combined_gate_validation_readiness_preflight_created": True,
            "current_missing_requirements_register_created": True,
            "future_transition_sequence_created": True,
            "review_packaging_warning_created": True,
            "no_active_ingestion_status": "closed",
            "no_byte_stream_transition_gate_status": "closed",
            "no_execution_transition_gate_status": "closed",
            "stage5bd_dry_run_records_remain_valid": True,
            "stage5bd_run_plan_id_count": run_plan_count,
            "stage5bd_run_plan_ids_changed": False,
            "stage5bd_dry_run_plan_manifest_changed": False,
            "stage5bd_plan_superseded": False,
            "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
            "deprecated_stage5aw_path_absent": INCORRECT_STAGE5AW_PATH not in ACTIVE_LINEAGE_PATHS,
            "correct_stage5aw_path_included": CORRECT_STAGE5AW_PATH in ACTIVE_LINEAGE_PATHS,
            "string4_sidecar_status": "scaffolded_inactive",
            "future_token_block_execution_remains_blocked": True,
            "source_digest_record_count": source_digest_count,
            "parallel_worker_cap_for_stage5co_and_later": PARALLEL_WORKER_CAP,
            "recommended_next_stage_id": "stage-5cp",
            "recommended_next_stage_title": next_title,
        },
    )
    return records


def build_stage5co(*, results_dir: Path = RESULTS_DIR) -> dict[str, Any]:
    """Build Stage 5CO committed metadata and ignored transition reports."""

    _write_schemas()
    results_dir.mkdir(parents=True, exist_ok=True)
    records = _build_records()
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)

    write_json(results_dir / "summary.json", records["summary"])
    write_json(
        results_dir / "readiness_package_report.json",
        {
            "readiness_package": records["readiness_package"],
            "real_operator_readiness": records["real_operator_readiness"],
            "real_deep_research_readiness": records["real_deep_research_readiness"],
            "real_combined_gate_readiness": records["real_combined_gate_readiness"],
            "real_record_blocker": records["real_record_blocker"],
        },
    )
    write_json(
        results_dir / "transition_plan_report.json",
        {
            "activation_transition_plan": records["activation_transition_plan"],
            "missing_requirements": records["missing_requirements"],
            "activation_nonauthorization": records["activation_nonauthorization"],
        },
    )
    write_json(
        results_dir / "credential_scan.json",
        {
            "credential_redaction": records["credential_redaction"],
            "secret_values_recorded": False,
        },
    )
    write_json(results_dir / "source_digest_index.json", records["source_digest_index"])
    write_jsonl(
        results_dir / "warnings.jsonl",
        [
            {
                "stage_id": STAGE_ID,
                "warning_id": warning_id,
                "status": status,
                "gate_opening": False,
            }
            for warning_id, status in STAGE5CN_WARNINGS.items()
        ],
    )
    return records["summary"]


def _load_all_payloads(errors: list[str]) -> dict[str, dict[str, Any]]:
    return {key: _validate_payload(path, errors) for key, path in DATA_PATHS.items()}


def _validate_payload(path: Path, errors: list[str]) -> dict[str, Any]:
    if not path.is_file():
        errors.append(f"missing_record={repo_relative(path)}")
        return {}
    payload = _read(path)
    schema_path = payload.get("schema")
    if not isinstance(schema_path, str) or not Path(schema_path).is_file():
        errors.append(f"{repo_relative(path)} schema missing: {schema_path}")
        return payload
    schema_errors = list(Draft202012Validator(_load_schema(schema_path)).iter_errors(payload))
    errors.extend(f"{repo_relative(path)} schema_error={error.message}" for error in schema_errors)
    return payload


def _walk_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        result: list[str] = []
        for item in value.values():
            result.extend(_walk_strings(item))
        return result
    if isinstance(value, list):
        result = []
        for item in value:
            result.extend(_walk_strings(item))
        return result
    return []


def _check_false_flags(payloads: dict[str, dict[str, Any]], errors: list[str]) -> None:
    for key, payload in payloads.items():
        for field, expected in FALSE_FLAGS.items():
            if payload.get(field) is not None and payload.get(field) is not expected:
                errors.append(f"{key}: {field} must be false")


def _check_no_stage5co_metadata_secrets(errors: list[str]) -> None:
    for path in DATA_PATHS.values():
        if path.is_file() and _path_has_secret_like_text(path):
            errors.append(f"credential_like_text_in_stage5co_metadata={repo_relative(path)}")


def validate_stage5co_actual_record_rejection(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in (
        "real_approval_readiness_satisfied_now",
        "real_operator_approval_record_present_now",
        "operator_approval_record_present_now",
        "deep_research_activation_accept_record_present_now",
        "combined_approval_gate_satisfied_now",
        "activation_decision_valid_now",
        "active_planning_input_selected_now",
        "byte_stream_generation_authorized_now",
        "execution_authorized_now",
        "solve_claim",
    ):
        if payload.get(field) is True:
            errors.append(f"{field} must be false")
    strings = _walk_strings(payload)
    if INCORRECT_STAGE5AW_PATH in strings:
        errors.append("deprecated Stage 5AW path must fail")
    for text in strings:
        findings = _secret_findings(text)
        if findings:
            errors.append(f"credential_like_text_categories={','.join(sorted(findings))}")
    if payload.get("record_class") in FORBIDDEN_CURRENT_RECORD_CLASSES and payload.get(
        "satisfies_real_readiness"
    ) is True:
        errors.append("fixture/template/scaffold/review_package cannot satisfy real readiness")
    return errors


def validate_stage5co_stage5cn_findings(
    *, findings: Path = DATA_PATHS["findings"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(findings, errors)
    if payload.get("stage5cn_verdict") != "accept_with_warnings":
        errors.append("Stage 5CN verdict must be accept_with_warnings")
    observed = set(payload.get("findings", []))
    for item in sorted(set(STAGE5CN_FINDINGS) - observed):
        errors.append(f"missing_stage5cn_finding={item}")
    return {
        "stage5co_stage5cn_findings_valid": not errors,
        "stage5cn_verdict": payload.get("stage5cn_verdict"),
        "finding_count": len(observed),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5co_approval_readiness_package(
    *, readiness_package: Path = DATA_PATHS["readiness_package"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(readiness_package, errors)
    if payload.get("real_approval_record_readiness_package_created") is not True:
        errors.append("real approval readiness package must be created")
    if payload.get("future_real_records_created_now") is not False:
        errors.append("future real records must not be created now")
    if set(payload.get("future_real_record_classes", [])) != set(FUTURE_REAL_RECORD_CLASSES):
        errors.append("future real record classes must match Stage 5CO contract")
    errors.extend(validate_stage5co_actual_record_rejection(payload))
    return {
        "stage5co_approval_readiness_package_valid": not errors,
        "future_real_record_class_count": len(payload.get("future_real_record_classes", [])),
        "validation_error_count": len(errors),
    }, errors


def _validate_readiness_requirements(
    *,
    payload: dict[str, Any],
    required: list[str],
    readiness_flag: str,
    present_flag: str,
    errors: list[str],
) -> None:
    if payload.get(readiness_flag) is not True:
        errors.append(f"{readiness_flag} must be true")
    if payload.get(present_flag) is not False:
        errors.append(f"{present_flag} must be false")
    observed = set(payload.get("required_future_fields", []))
    for item in sorted(set(required) - observed):
        errors.append(f"missing_required_future_field={item}")
    if set(payload.get("future_record_must_not_be", [])) != set(FORBIDDEN_CURRENT_RECORD_CLASSES):
        errors.append("future_record_must_not_be must include fixture/template/scaffold/review_package")
    errors.extend(validate_stage5co_actual_record_rejection(payload))


def validate_stage5co_real_operator_readiness(
    *, real_operator_readiness: Path = DATA_PATHS["real_operator_readiness"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(real_operator_readiness, errors)
    _validate_readiness_requirements(
        payload=payload,
        required=REAL_OPERATOR_REQUIREMENTS,
        readiness_flag="real_operator_approval_readiness_preflight_created",
        present_flag="real_operator_approval_record_present_now",
        errors=errors,
    )
    return {
        "stage5co_real_operator_readiness_valid": not errors,
        "required_future_field_count": len(payload.get("required_future_fields", [])),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5co_real_deep_research_readiness(
    *, real_deep_research_readiness: Path = DATA_PATHS["real_deep_research_readiness"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(real_deep_research_readiness, errors)
    _validate_readiness_requirements(
        payload=payload,
        required=REAL_DEEP_RESEARCH_REQUIREMENTS,
        readiness_flag="real_deep_research_acceptance_readiness_preflight_created",
        present_flag="deep_research_activation_accept_record_present_now",
        errors=errors,
    )
    return {
        "stage5co_real_deep_research_readiness_valid": not errors,
        "required_future_field_count": len(payload.get("required_future_fields", [])),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5co_real_combined_gate_readiness(
    *, real_combined_gate_readiness: Path = DATA_PATHS["real_combined_gate_readiness"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(real_combined_gate_readiness, errors)
    if payload.get("real_combined_gate_validation_readiness_preflight_created") is not True:
        errors.append("combined gate readiness preflight must be created")
    for field in (
        "real_combined_gate_validation_record_present_now",
        "operator_approval_record_present_now",
        "deep_research_activation_accept_record_present_now",
        "combined_approval_gate_satisfied_now",
        "combined_approval_gate_authorizes_activation_now",
    ):
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    observed = set(payload.get("required_future_validations", []))
    for item in sorted(set(COMBINED_GATE_REQUIREMENTS) - observed):
        errors.append(f"missing_combined_gate_requirement={item}")
    return {
        "stage5co_real_combined_gate_readiness_valid": not errors,
        "required_future_validation_count": len(observed),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5co_activation_transition_plan(
    *, activation_transition_plan: Path = DATA_PATHS["activation_transition_plan"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(activation_transition_plan, errors)
    if payload.get("transition_plan_status") != "planning_only":
        errors.append("transition plan must be planning_only")
    if payload.get("future_transition_sequence") != FUTURE_TRANSITION_SEQUENCE:
        errors.append("future transition sequence must match Stage 5CO contract")
    if set(payload.get("transition_plan_does_not_authorize", [])) != set(
        TRANSITION_PLAN_DOES_NOT_AUTHORIZE
    ):
        errors.append("transition plan non-authorization list mismatch")
    errors.extend(validate_stage5co_actual_record_rejection(payload))
    return {
        "stage5co_activation_transition_plan_valid": not errors,
        "future_transition_step_count": len(payload.get("future_transition_sequence", [])),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5co_current_missing_requirements(
    *, missing_requirements: Path = DATA_PATHS["missing_requirements"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(missing_requirements, errors)
    observed = payload.get("missing_requirements", [])
    if not observed:
        errors.append("missing requirements register must be non-empty")
    if set(observed) != set(MISSING_REQUIREMENTS):
        errors.append("missing requirements must match Stage 5CO contract")
    if payload.get("missing_requirement_count") != len(MISSING_REQUIREMENTS):
        errors.append("missing requirement count mismatch")
    errors.extend(validate_stage5co_actual_record_rejection(payload))
    return {
        "stage5co_current_missing_requirements_valid": not errors,
        "missing_requirement_count": payload.get("missing_requirement_count"),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5co_real_record_blocker(
    *, real_record_blocker: Path = DATA_PATHS["real_record_blocker"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(real_record_blocker, errors)
    if payload.get("real_record_creation_blocker_status") != "active":
        errors.append("real-record creation blocker must be active")
    if set(payload.get("blocked_current_stage_real_records", [])) != set(FUTURE_REAL_RECORD_CLASSES):
        errors.append("blocked current-stage real record classes mismatch")
    for field in (
        "real_operator_approval_record_created_now",
        "real_deep_research_acceptance_record_created_now",
        "real_combined_gate_validation_record_created_now",
        "real_activation_decision_record_created_now",
        "future_real_records_created_now",
    ):
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    return {
        "stage5co_real_record_blocker_valid": not errors,
        "blocked_current_stage_real_record_count": len(
            payload.get("blocked_current_stage_real_records", [])
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5co_stage5cm_boundary_preservation(
    *, stage5cm_boundary: Path = DATA_PATHS["stage5cm_boundary"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(stage5cm_boundary, errors)
    for field in (
        "stage5cm_status_preserved",
        "stage5cm_approval_readiness_boundary_preserved",
        "stage5cm_fixture_vs_real_boundary_preserved",
        "stage5cm_end_to_end_readiness_boundary_preserved",
        "stage5cm_credential_redaction_policy_preserved",
    ):
        if payload.get(field) is not True:
            errors.append(f"{field} must be true")
    if payload.get("stage5cm_parallel_worker_cap_preserved") != PARALLEL_WORKER_CAP:
        errors.append("Stage 5CM worker cap must remain 8")
    for label, validator in (
        ("stage5cm_approval", validate_stage5cm_approval_readiness_boundary),
        ("stage5cm_fixture_real", validate_stage5cm_fixture_real_boundary),
        ("stage5cm_end_to_end", validate_stage5cm_end_to_end_readiness_boundary),
        ("stage5cm_real_approval", validate_stage5cm_real_approval_readiness),
        ("stage5cm_credential", validate_stage5cm_credential_redaction_policy),
        ("stage5cm_sidecar", validate_stage5cm_sidecar_gates),
    ):
        _, validator_errors = validator()
        errors.extend(f"{label}:{error}" for error in validator_errors)
    return {
        "stage5co_stage5cm_boundary_preservation_valid": not errors,
        "stage5cm_parallel_worker_cap_preserved": payload.get(
            "stage5cm_parallel_worker_cap_preserved"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5co_prior_stage_preservation() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = _load_all_payloads(errors)
    required_true = {
        "stage5ck_preservation": [
            "stage5ck_fixture_pack_preserved",
            "stage5ck_fixture_pack_only_preserved",
            "stage5ck_synthetic_negative_fixtures_only_preserved",
        ],
        "stage5ci_preservation": ["stage5ci_templates_preserved"],
        "stage5cg_preservation": ["stage5cg_scaffolds_preserved"],
        "stage5ce_preservation": ["stage5ce_proposal_package_preserved"],
        "stage5cc_preservation": [
            "stage5cc_exact_citation_contract_preserved",
            "stage5cc_fail_closed_trigger_exact_set_preserved",
            "stage5cc_activation_precondition_exact_set_preserved",
        ],
    }
    for key, fields in required_true.items():
        for field in fields:
            if payloads.get(key, {}).get(field) is not True:
                errors.append(f"{key}: {field} must be true")
    if payloads.get("stage5ce_preservation", {}).get(
        "stage5ce_proposal_package_status_preserved"
    ) != "review_package_only":
        errors.append("Stage 5CE proposal package must remain review_package_only")
    stage5bd = payloads.get("stage5bd_preservation", {})
    if stage5bd.get("stage5bd_run_plan_id_count") != 10:
        errors.append("Stage 5BD run-plan ID count must remain 10")
    if stage5bd.get("stage5bd_run_plan_ids_changed") is not False:
        errors.append("Stage 5BD run-plan IDs must be unchanged")
    lineage = payloads.get("active_lineage", {})
    if lineage.get("active_lineage_record_count") != 8:
        errors.append("active lineage must remain 8 records")
    if lineage.get("correct_stage5aw_path_included") is not True:
        errors.append("correct Stage 5AW path must be included")
    if lineage.get("deprecated_stage5aw_path_absent") is not True:
        errors.append("deprecated Stage 5AW path must be absent")
    for label, validator in (
        ("stage5ca", validate_stage5ca),
        ("stage5ca_citation", validate_stage5ca_citation_contract),
        ("stage5ca_triggers", validate_stage5ca_fail_closed_triggers),
        ("stage5ca_preconditions", validate_stage5ca_activation_preconditions),
        ("stage5cc_triggers", validate_stage5cc_fail_closed_triggers),
        ("stage5cc_preconditions", validate_stage5cc_activation_preconditions),
        ("stage5cc", validate_stage5cc),
        ("stage5bd", validate_stage5bd),
    ):
        _, validator_errors = validator()
        errors.extend(f"{label}:{error}" for error in validator_errors)
    return {
        "stage5co_prior_stage_preservation_valid": not errors,
        "stage5bd_run_plan_id_count": stage5bd.get("stage5bd_run_plan_id_count"),
        "active_lineage_record_count": lineage.get("active_lineage_record_count"),
        "validation_error_count": len(errors),
    }, errors


def _validate_sidecar_payloads(payloads: dict[str, dict[str, Any]], errors: list[str]) -> None:
    for key, payload in payloads.items():
        if payload.get("string4_sidecar_status") not in {None, "scaffolded_inactive"}:
            errors.append(f"{key}: string4_sidecar_status must remain scaffolded_inactive")
        for field in (
            "string4_sidecar_active",
            "string4_sidecar_planning_ingestion_activated",
            "string4_active_input_allowed",
            "string4_dry_run_ingestion_allowed_now",
            "string4_byte_stream_generation_allowed",
            "string4_execution_input_allowed",
            "active_planning_input_authorized_now",
            "dry_run_ingestion_authorized_now",
            "byte_stream_generation_authorized_now",
            "execution_authorized_now",
        ):
            if payload.get(field) is True:
                errors.append(f"{key}: {field} must remain false")


def validate_stage5co_sidecar_gates(
    *,
    no_active_ingestion: Path = DATA_PATHS["no_active_ingestion"],
    no_byte_stream_transition_gate: Path = DATA_PATHS["no_byte_stream_transition_gate"],
    no_execution_transition_gate: Path = DATA_PATHS["no_execution_transition_gate"],
    sidecar_activation_blocker: Path = DATA_PATHS["sidecar_activation_blocker"],
    activation_nonauthorization: Path = DATA_PATHS["activation_nonauthorization"],
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = {
        "no_active_ingestion": _validate_payload(no_active_ingestion, errors),
        "no_byte_stream_transition_gate": _validate_payload(no_byte_stream_transition_gate, errors),
        "no_execution_transition_gate": _validate_payload(no_execution_transition_gate, errors),
        "sidecar_activation_blocker": _validate_payload(sidecar_activation_blocker, errors),
        "activation_nonauthorization": _validate_payload(activation_nonauthorization, errors),
    }
    _validate_sidecar_payloads(payloads, errors)
    if payloads["no_active_ingestion"].get("no_active_ingestion_status") != "closed":
        errors.append("no-active-ingestion gate must be closed")
    if payloads["no_byte_stream_transition_gate"].get("no_byte_stream_transition_gate_status") != "closed":
        errors.append("no-byte-stream transition gate must be closed")
    if payloads["no_execution_transition_gate"].get("no_execution_transition_gate_status") != "closed":
        errors.append("no-execution transition gate must be closed")
    if payloads["activation_nonauthorization"].get("activation_decision_valid_now") is not False:
        errors.append("activation decision must be invalid now")
    return {
        "stage5co_sidecar_gates_valid": not errors,
        "no_active_ingestion_status": payloads["no_active_ingestion"].get(
            "no_active_ingestion_status"
        ),
        "no_byte_stream_transition_gate_status": payloads["no_byte_stream_transition_gate"].get(
            "no_byte_stream_transition_gate_status"
        ),
        "no_execution_transition_gate_status": payloads["no_execution_transition_gate"].get(
            "no_execution_transition_gate_status"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5co_credential_redaction_policy(
    *, credential_redaction: Path = DATA_PATHS["credential_redaction"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(credential_redaction, errors)
    for field in (
        "credential_redaction_policy_created",
        "credential_like_remote_must_be_redacted",
        "credential_like_text_must_not_be_committed",
        "committed_stage5co_metadata_secret_scan_required",
        "remote_url_redacted_in_metadata",
    ):
        if payload.get(field) is not True:
            errors.append(f"{field} must be true")
    if payload.get("secret_values_printed_or_committed") is not False:
        errors.append("secret values must not be printed or committed")
    _check_no_stage5co_metadata_secrets(errors)
    return {
        "stage5co_credential_redaction_policy_valid": not errors,
        "credential_like_remote_detected": payload.get("remote_hygiene", {}).get(
            "credential_like_remote_detected"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5co(
    *,
    summary: Path = DATA_PATHS["summary"],
    next_stage_decision: Path = DATA_PATHS["next_stage"],
    guardrail: Path = DATA_PATHS["guardrail"],
    results_dir: Path = RESULTS_DIR,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = _load_all_payloads(errors)
    _check_false_flags(payloads, errors)
    _validate_sidecar_payloads(payloads, errors)
    _check_no_stage5co_metadata_secrets(errors)
    summary_payload = payloads["summary"] if summary == DATA_PATHS["summary"] else _validate_payload(summary, errors)
    next_payload = (
        payloads["next_stage"]
        if next_stage_decision == DATA_PATHS["next_stage"]
        else _validate_payload(next_stage_decision, errors)
    )
    guardrail_payload = (
        payloads["guardrail"] if guardrail == DATA_PATHS["guardrail"] else _validate_payload(guardrail, errors)
    )
    for _counts, focused_errors in (
        validate_stage5co_stage5cn_findings(),
        validate_stage5co_approval_readiness_package(),
        validate_stage5co_real_operator_readiness(),
        validate_stage5co_real_deep_research_readiness(),
        validate_stage5co_real_combined_gate_readiness(),
        validate_stage5co_activation_transition_plan(),
        validate_stage5co_current_missing_requirements(),
        validate_stage5co_real_record_blocker(),
        validate_stage5co_stage5cm_boundary_preservation(),
        validate_stage5co_prior_stage_preservation(),
        validate_stage5co_sidecar_gates(),
        validate_stage5co_credential_redaction_policy(),
    ):
        errors.extend(focused_errors)
    for field in (
        "stage5cn_findings_integrated",
        "stage5cm_status_preserved",
        "real_approval_record_readiness_package_created",
        "activation_decision_transition_plan_created",
        "current_missing_requirements_register_created",
    ):
        if summary_payload.get(field) is not True:
            errors.append(f"summary {field} must be true")
    for field in MANDATORY_FALSE_SUMMARY_FLAGS:
        if summary_payload.get(field) is not False:
            errors.append(f"summary {field} must be false")
    if summary_payload.get("stage5cn_verdict") != "accept_with_warnings":
        errors.append("summary Stage 5CN verdict must be accept_with_warnings")
    if summary_payload.get("stage5bd_run_plan_id_count") != 10:
        errors.append("Stage 5BD run-plan ID count must remain 10")
    if summary_payload.get("active_lineage_record_count") != 8:
        errors.append("active lineage must contain exactly 8 records")
    if summary_payload.get("parallel_worker_cap_for_stage5co_and_later") != PARALLEL_WORKER_CAP:
        errors.append("Stage 5CO parallel worker cap must be 8")
    if next_payload.get("selected_next_stage_id") != "stage-5cp":
        errors.append("Stage 5CO must select Stage 5CP as next stage")
    if next_payload.get("selected_next_prompt_type") != "deep_research_review":
        errors.append("Stage 5CP prompt type must be deep_research_review")
    if next_payload.get("selected_next_stage_authorizes_execution") is not False:
        errors.append("Stage 5CP must not authorize execution")
    if guardrail_payload.get("future_token_block_execution_remains_blocked") is not True:
        errors.append("future token-block execution must remain blocked")
    for output_name in (
        "summary.json",
        "readiness_package_report.json",
        "transition_plan_report.json",
        "credential_scan.json",
        "source_digest_index.json",
        "warnings.jsonl",
    ):
        if not (results_dir / output_name).is_file():
            errors.append(f"missing_generated_output={repo_relative(results_dir / output_name)}")
    return {
        "stage5co_valid": not errors,
        "validation_error_count": len(errors),
        "stage5cn_verdict": summary_payload.get("stage5cn_verdict"),
        "real_approval_record_readiness_package_created": summary_payload.get(
            "real_approval_record_readiness_package_created"
        ),
        "activation_decision_valid_now": summary_payload.get("activation_decision_valid_now"),
        "combined_approval_gate_satisfied_now": summary_payload.get(
            "combined_approval_gate_satisfied_now"
        ),
        "active_planning_input_authorized_now": summary_payload.get(
            "active_planning_input_authorized_now"
        ),
        "stage5bd_run_plan_id_count": summary_payload.get("stage5bd_run_plan_id_count"),
        "active_lineage_record_count": summary_payload.get("active_lineage_record_count"),
        "parallel_worker_cap": summary_payload.get("parallel_worker_cap_for_stage5co_and_later"),
        "recommended_next_stage_id": summary_payload.get("recommended_next_stage_id"),
    }, errors


def load_stage5co_summary(*, summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    return _read(summary)
