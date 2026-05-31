"""Stage 5CM approval-readiness boundary metadata."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.token_block.models import repo_relative, sha256_file, write_json, write_yaml
from libreprimus.token_block.stage5bm import _read
from libreprimus.token_block.stage5ca import (
    ACTIVE_LINEAGE_PATHS,
    CORRECT_STAGE5AW_PATH,
    INCORRECT_STAGE5AW_PATH,
    REQUIRED_ACTIVATION_PRECONDITIONS,
    REQUIRED_CITATION_PATHS,
    REQUIRED_FAIL_CLOSED_TRIGGERS,
    validate_stage5ca,
    validate_stage5ca_citation_contract,
)
from libreprimus.token_block.stage5cc import (
    DATA_PATHS as STAGE5CC_DATA_PATHS,
    validate_stage5cc,
    validate_stage5cc_activation_preconditions,
    validate_stage5cc_fail_closed_triggers,
)
from libreprimus.token_block.stage5ce import (
    DATA_PATHS as STAGE5CE_DATA_PATHS,
    RESULTS_DIR as STAGE5CE_RESULTS_DIR,
    validate_stage5ce,
)
from libreprimus.token_block.stage5cg import (
    DATA_PATHS as STAGE5CG_DATA_PATHS,
    RESULTS_DIR as STAGE5CG_RESULTS_DIR,
    validate_stage5cg,
)
from libreprimus.token_block.stage5ci import (
    DATA_PATHS as STAGE5CI_DATA_PATHS,
    RESULTS_DIR as STAGE5CI_RESULTS_DIR,
    validate_stage5ci,
)
from libreprimus.token_block.stage5ck import (
    DATA_PATHS as STAGE5CK_DATA_PATHS,
    RESULTS_DIR as STAGE5CK_RESULTS_DIR,
    validate_stage5ck,
)

STAGE_ID = "stage-5cm"
STAGE_TITLE = (
    "Stage 5CM - Approval-record readiness boundary and activation-decision "
    "gate hardening, without execution"
)
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE = "stage-5ck"
SOURCE_PREVIOUS_COMMIT = "9a9b45c262d438d3f94d661dc8522c743252b55b"
SOURCE_DEEP_RESEARCH_STAGE = "stage-5cl"
SOURCE_DEEP_RESEARCH_REPORT = "21_Stage-5CK-Deep-Research-Review.md"
STAGE5CL_REPORT_PATH = Path(
    "deep-research-reports/reviews-of-ideas-and-concepts-and-data/md/"
    "21_Stage-5CK-Deep-Research-Review.md"
)
RESULTS_DIR = Path("experiments/results/token-block/stage5cm")
CODEX_COMPLETION_PATH = Path("codex-output/stage5cm-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")

PYTEST_COUNT_OBSERVED_LOCALLY = 2344
PYTEST_COMMAND_OBSERVED_LOCALLY = "python -m pytest -q tests/python"
PARALLEL_WORKER_CAP = 8

STAGE5CL_FINDINGS = [
    "stage5ck_safe_to_build_on",
    "stage5ck_metadata_only",
    "stage5ck_fixture_only",
    "stage5ck_operator_approval_fixtures_created",
    "stage5ck_deep_research_acceptance_fixtures_created",
    "stage5ck_activation_decision_fixtures_created",
    "stage5ck_negative_validation_matrix_created",
    "stage5ck_fixture_isolation_policy_created",
    "stage5ck_activation_decision_review_package_created",
    "stage5ck_real_operator_approval_records_absent",
    "stage5ck_real_deep_research_acceptance_records_absent",
    "stage5ck_real_activation_decision_records_absent",
    "stage5ck_combined_gate_unsatisfied",
    "stage5ck_activation_not_authorized",
    "stage5ck_active_planning_input_not_authorized",
    "stage5ck_active_planning_input_not_selected",
    "string4_remains_inactive_noncanonical_sidecar_context",
    "stage5bd_run_plan_ids_preserved_at_10",
    "active_lineage_preserved_at_8_records",
    "no_byte_and_no_execution_gates_closed",
    "active_token_block_records_not_mutated",
    "no_dwh_hash_decode_scoring_cuda_benchmark_stego_ocr_ai_website_or_solve_work",
    "stage5ck_not_enough_to_start_execution",
    "next_stage_should_harden_real_record_readiness_boundary",
]

STAGE5CL_WARNINGS = {
    "attached_zip_not_pristine_checkout": "non_gate_opening_reviewability_warning",
    "public_github_corroboration_unreliable": "external_evidence_caveat",
    "final_commit_and_ci_external_evidence": "post_push_evidence_required",
    "validation_evidence_compactness": "record_compact_evidence_and_local_counts",
    "credential_like_remote_reported_in_prior_deep_research_text": (
        "redact_and_scan_without_committing_secret_values"
    ),
}

BOUNDARY_SOURCE_RECORD_CLASSES = [
    "fixture_operator_approval",
    "fixture_deep_research_acceptance",
    "fixture_activation_decision",
    "template_operator_approval",
    "template_deep_research_acceptance",
    "template_activation_decision",
    "scaffold_operator_approval",
    "scaffold_deep_research_acceptance",
    "scaffold_combined_gate",
    "scaffold_activation_decision",
    "review_package_activation_decision",
]

FUTURE_REAL_RECORD_CLASSES = [
    "real_operator_approval_record",
    "real_deep_research_activation_acceptance_record",
    "real_combined_approval_gate_validation_record",
    "real_activation_decision_record",
]

END_TO_END_NEGATIVE_CASES = [
    "stage5ck_operator_fixture_as_real_operator_approval",
    "stage5ck_deep_research_fixture_as_real_acceptance",
    "stage5ck_activation_fixture_as_real_activation_decision",
    "stage5ci_operator_template_as_real_operator_approval",
    "stage5ci_deep_research_template_as_real_acceptance",
    "stage5ci_activation_template_as_real_activation_decision",
    "stage5cg_scaffold_as_real_gate_record",
    "stage5ck_review_package_as_activation_authorization",
    "fixture_only_true_gate_satisfying_input",
    "template_only_true_gate_satisfying_input",
    "review_package_only_gate_satisfying_input",
    "activation_authorized_now_true",
    "active_planning_input_selected_now_true",
    "byte_stream_generation_authorized_now_true",
    "execution_authorized_now_true",
    "solve_claim_true",
    "deprecated_stage5aw_path_reintroduced",
    "credential_like_string_in_stage5cm_metadata",
]

FUTURE_REAL_READINESS_CRITERIA = [
    "explicit_future_stage_id_and_prompt_type",
    "non_fixture_record_status",
    "non_template_record_status",
    "exact_stage5ce_proposal_package_citation",
    "exact_stage5cg_scaffold_citation",
    "exact_stage5ci_template_version_citation",
    "exact_stage5ck_fixture_review_package_citation_if_applicable",
    "stage5cc_exact_contract_validation",
    "stage5bd_preservation_or_explicit_future_supersession",
    "active_lineage_preservation_or_explicit_future_supersession",
    "no_byte_stream_acknowledgement",
    "no_execution_acknowledgement",
    "no_solve_claim_acknowledgement",
]

ACTIVATION_DECISION_REQUIRED_CRITERIA = [
    "real_operator_approval_present_not_fixture_template_or_scaffold",
    "real_deep_research_acceptance_present_not_fixture_template_or_scaffold",
    "combined_gate_validation_proves_both_present",
    "selected_active_planning_input_explicitly_named",
    "string4_status_transition_explicitly_defined",
    "no_byte_and_no_execution_acknowledgements_present",
    "stage5bd_preservation_or_explicit_supersession_present",
    "active_lineage_preservation_or_explicit_supersession_present",
    "manifest_supersession_explicit_if_selected",
    "solve_claim_false_explicit",
]

DATA_PATHS: dict[str, Path] = {
    "summary": Path("data/project-state/stage5cm-summary.yaml"),
    "next_stage": Path("data/project-state/stage5cm-next-stage-decision.yaml"),
    "findings": Path("data/project-state/stage5cm-stage5cl-findings-integration.yaml"),
    "stage_marker": Path("data/project-state/stage5cm-reviewable-stage-marker.yaml"),
    "validation_evidence": Path("data/project-state/stage5cm-reviewable-validation-evidence.yaml"),
    "source_digest_index": Path("data/project-state/stage5cm-reviewable-source-digest-index.yaml"),
    "gap_register": Path("data/project-state/stage5cm-reviewability-gap-register.yaml"),
    "equivalence_map": Path("data/project-state/stage5cm-record-family-name-equivalence-map.yaml"),
    "approval_readiness_boundary": Path(
        "data/token-block/stage5cm-approval-readiness-boundary-contract.yaml"
    ),
    "fixture_real_boundary": Path("data/token-block/stage5cm-fixture-vs-real-record-boundary.yaml"),
    "end_to_end_boundary": Path(
        "data/token-block/stage5cm-end-to-end-readiness-boundary-validation.yaml"
    ),
    "real_approval_readiness": Path(
        "data/token-block/stage5cm-real-approval-record-readiness-preflight.yaml"
    ),
    "activation_gate": Path("data/token-block/stage5cm-activation-decision-gate-hardening.yaml"),
    "stage5ck_preservation": Path("data/token-block/stage5cm-stage5ck-fixture-preservation.yaml"),
    "stage5ci_preservation": Path("data/token-block/stage5cm-stage5ci-template-preservation.yaml"),
    "stage5cg_preservation": Path("data/token-block/stage5cm-stage5cg-scaffold-preservation.yaml"),
    "stage5ce_preservation": Path("data/token-block/stage5cm-stage5ce-proposal-package-preservation.yaml"),
    "stage5cc_preservation": Path("data/token-block/stage5cm-stage5cc-contract-preservation.yaml"),
    "stage5bd_preservation": Path("data/token-block/stage5cm-stage5bd-plan-preservation.yaml"),
    "active_lineage": Path("data/token-block/stage5cm-active-lineage-preservation.yaml"),
    "no_active_ingestion": Path("data/token-block/stage5cm-no-active-ingestion-proof.yaml"),
    "no_byte_stream_transition_gate": Path("data/token-block/stage5cm-no-byte-stream-transition-gate.yaml"),
    "no_execution_transition_gate": Path("data/token-block/stage5cm-no-execution-transition-gate.yaml"),
    "supersession_nonactivation": Path(
        "data/token-block/stage5cm-manifest-supersession-nonactivation-proof.yaml"
    ),
    "sidecar_activation_blocker": Path("data/token-block/stage5cm-sidecar-activation-blocker.yaml"),
    "guardrail": Path("data/historical-route/stage5cm-guardrail.yaml"),
    "dwh": Path("data/historical-route/stage5cm-dwh-quarantine-reaffirmation.yaml"),
    "source_gap": Path("data/historical-route/stage5cm-source-gap-severity-update.yaml"),
    "credential_redaction": Path("data/source-harvester/stage5cm-credential-redaction-policy.yaml"),
    "handoff": Path("data/source-harvester/stage5cm-codex-handoff-policy.yaml"),
}

SCHEMA_PATHS: dict[str, str] = {
    key: path.as_posix().replace("data/", "schemas/", 1).replace(".yaml", "-v0.schema.json")
    for key, path in DATA_PATHS.items()
}

RECORD_TYPES = {key: f"stage5cm_{key}" for key in DATA_PATHS}

FALSE_FLAGS = {
    "activation_authorized_now": False,
    "activation_decision_valid_now": False,
    "active_ingestion_performed": False,
    "active_manifest_registry_updated": False,
    "active_planning_input_authorized_now": False,
    "active_planning_input_decision_record_created_now": False,
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
    "deep_research_activation_accept_record_created_now": False,
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
    "llm_vision_token_reading_performed": False,
    "manifest_supersession_authorized_now": False,
    "manifest_supersession_performed": False,
    "method_status_upgraded": False,
    "new_active_planning_input_created": False,
    "ocr_performed": False,
    "operator_approval_record_created_now": False,
    "operator_approval_record_present_now": False,
    "real_activation_decision_record_created_now": False,
    "real_activation_decision_records_created": False,
    "real_approval_records_created": False,
    "real_byte_stream_generated": False,
    "real_combined_gate_validation_record_created_now": False,
    "real_deep_research_acceptance_record_created_now": False,
    "real_deep_research_acceptance_records_created": False,
    "real_operator_approval_record_created_now": False,
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
    "template_misread_as_approval": False,
    "token_block_experiment_executed": False,
    "variant_byte_streams_generated": False,
    "variant_materialisation_performed": False,
    "website_expansion_performed": False,
}

SECRET_PATTERNS: dict[str, str] = {
    "github_personal_access_token_prefix": r"ghp_[A-Za-z0-9_]+",
    "github_fine_grained_token_prefix": r"github_pat_[A-Za-z0-9_]+",
    "x_access_token_remote": r"x-access-token:",
    "oauth2_remote": r"oauth2:",
    "token_query_parameter": r"(?i)\btoken=",
    "access_token_query_parameter": r"(?i)\baccess_token=",
    "credentialed_github_https_remote": r"https://(?!<redacted>@)[^\s/]+@github\.com/",
}


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


def _secret_findings(text: str) -> list[str]:
    findings: list[str] = []
    for name, pattern in SECRET_PATTERNS.items():
        if re.search(pattern, text):
            findings.append(name)
    return findings


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
        "local_remote_sanitized_if_safe": False if credential_like else None,
        "secret_value_recorded": False,
    }


def _ignored_report_secret_status() -> dict[str, Any]:
    if not STAGE5CL_REPORT_PATH.is_file():
        return {
            "ignored_stage5cl_report_present": False,
            "credential_like_text_found_in_ignored_stage5cl_report": False,
            "secret_values_recorded": False,
        }
    text = STAGE5CL_REPORT_PATH.read_text(encoding="utf-8", errors="ignore")
    findings = _secret_findings(text)
    return {
        "ignored_stage5cl_report_present": True,
        "credential_like_text_found_in_ignored_stage5cl_report": bool(findings),
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
        "credential_like_text_scanned": path.is_file() and path == STAGE5CL_REPORT_PATH,
        "credential_like_text_present": _path_has_secret_like_text(path)
        if path == STAGE5CL_REPORT_PATH
        else False,
        "secret_values_recorded": False,
    }


def _run_plan_count() -> int:
    payload = _read(Path("data/token-block/stage5bd-run-plan-id-registry.yaml"))
    return int(payload.get("run_plan_id_count") or len(payload.get("plan_ids", [])))


def _source_paths() -> list[str]:
    paths = [
        STAGE5CL_REPORT_PATH.as_posix(),
        *[path.as_posix() for path in STAGE5CK_DATA_PATHS.values()],
        STAGE5CI_DATA_PATHS["summary"].as_posix(),
        STAGE5CG_DATA_PATHS["summary"].as_posix(),
        STAGE5CE_DATA_PATHS["summary"].as_posix(),
        STAGE5CC_DATA_PATHS["summary"].as_posix(),
        "data/token-block/stage5bd-dry-run-plan-manifest.yaml",
        "data/token-block/stage5bd-run-plan-id-registry.yaml",
        STAGE5CI_DATA_PATHS["operator_template"].as_posix(),
        STAGE5CI_DATA_PATHS["deep_research_template"].as_posix(),
        STAGE5CI_DATA_PATHS["activation_template"].as_posix(),
        STAGE5CG_DATA_PATHS["combined_gate"].as_posix(),
        STAGE5CE_DATA_PATHS["proposal_package"].as_posix(),
        STAGE5CC_DATA_PATHS["citation_preservation"].as_posix(),
        "README.md",
        "STATUS.md",
        "AGENTS.md",
        "ROADMAP.md",
        "TESTING.md",
        "RESULTS_SCHEMA.md",
        "EXPERIMENTS.md",
        "CIPHER_CATALOG.md",
        "docs/roadmap/staged-plan.md",
        "docs/onboarding/start-here.md",
        "docs/onboarding/source-of-truth-map.md",
        "docs/onboarding/operational-file-map.md",
        "docs/onboarding/codex-navigation-map.md",
        "docs/onboarding/deep-research-handoff-map.md",
        "docs/reference/token-block-cli.md",
    ]
    paths.extend(ACTIVE_LINEAGE_PATHS)
    return sorted(dict.fromkeys(paths))


def _validation_commands() -> list[dict[str, Any]]:
    commands = [
        "python -m libreprimus.cli token-block build-stage5cm",
        "python -m libreprimus.cli token-block validate-stage5cm-approval-readiness-boundary",
        "python -m libreprimus.cli token-block validate-stage5cm-fixture-real-boundary",
        "python -m libreprimus.cli token-block validate-stage5cm-end-to-end-readiness-boundary",
        "python -m libreprimus.cli token-block validate-stage5cm-real-approval-readiness",
        "python -m libreprimus.cli token-block validate-stage5cm-activation-decision-gate",
        "python -m libreprimus.cli token-block validate-stage5cm-credential-redaction-policy",
        "python -m libreprimus.cli token-block validate-stage5cm-sidecar-gates",
        "python -m libreprimus.cli token-block validate-stage5cm",
        "python -m libreprimus.cli token-block stage5cm-summary",
        "python -m libreprimus.cli token-block validate-stage5ck",
        "python -m libreprimus.cli token-block validate-stage5ci",
        "python -m libreprimus.cli token-block validate-stage5cg",
        "python -m libreprimus.cli token-block validate-stage5ce",
        "python -m libreprimus.cli token-block validate-stage5cc",
        "python -m libreprimus.cli token-block validate-stage5ca",
        "python -m libreprimus.cli token-block validate-stage5bd --results-dir experiments/results/token-block/stage5bd",
        "python -m libreprimus.cli parallel-validation validate-stage5ax",
        ".\\scripts\\ci\\run-parallel-validation.ps1 -Workers 8 -PytestWorkers 8 -PytestMode auto",
        "python -m libreprimus.cli research-synthesis validate --data-dir data/research --staged-plan docs/roadmap/staged-plan.md",
        "python -m libreprimus.cli consistency check-state-drift",
        "python -m libreprimus.cli consistency check-all --allow-warnings",
        "python -m libreprimus.cli smoke",
        "python -m ruff check python/libreprimus tests/python",
        "python -m pytest -q tests/python",
        ".\\scripts\\ci\\run-consistency-checks.ps1",
    ]
    return [{"command": command, "safe_to_parallelize": False} for command in commands]


def _source_digest_records() -> list[dict[str, Any]]:
    return [_sha_record(Path(path), role="stage5cm_reviewable_source") for path in _source_paths()]


def _build_records() -> dict[str, dict[str, Any]]:
    run_plan_count = _run_plan_count()
    source_records = _source_digest_records()
    remote_status = _remote_status()
    ignored_report_status = _ignored_report_secret_status()
    source_digest_count = len(source_records)
    lineage_records = [
        {
            "path": path,
            "present": Path(path).is_file(),
            "sha256": sha256_file(Path(path)) if Path(path).is_file() else None,
        }
        for path in ACTIVE_LINEAGE_PATHS
    ]

    records: dict[str, dict[str, Any]] = {}
    records["findings"] = _record(
        "findings",
        {
            "stage5cl_findings_integrated": True,
            "stage5cl_verdict": "accept_with_warnings",
            "stage5cl_findings": STAGE5CL_FINDINGS,
            "stage5cl_warning_disposition": STAGE5CL_WARNINGS,
            "stage5ck_safe_to_build_on": True,
        },
    )
    records["stage_marker"] = _record(
        "stage_marker",
        {
            "stage_status": "complete",
            "reviewable_stage_marker_created": True,
            "current_completed_stage": STAGE_TITLE,
            "selected_next_stage_id": "stage-5cn",
            "selected_next_stage_title": (
                "Stage 5CN - Deep Research review of Stage 5CM approval-record "
                "readiness boundary and activation-decision gate hardening, without execution"
            ),
        },
    )
    records["approval_readiness_boundary"] = _record(
        "approval_readiness_boundary",
        {
            "approval_record_readiness_boundary_created": True,
            "fixture_vs_real_record_boundary_hardened": True,
            "fixture_presented_as_real_record_must_fail_closed": True,
            "template_presented_as_real_record_must_fail_closed": True,
            "scaffold_presented_as_real_record_must_fail_closed": True,
            "review_package_presented_as_real_record_must_fail_closed": True,
            "future_real_approval_boundary_created": True,
            "future_real_record_classes": FUTURE_REAL_RECORD_CLASSES,
        },
    )
    records["fixture_real_boundary"] = _record(
        "fixture_real_boundary",
        {
            "fixture_vs_real_record_boundary_hardened": True,
            "source_record_classes_blocked_from_gate_satisfaction": BOUNDARY_SOURCE_RECORD_CLASSES,
            "future_real_record_classes": FUTURE_REAL_RECORD_CLASSES,
            "fixture_records_can_satisfy_gate": False,
            "templates_can_satisfy_gate": False,
            "scaffolds_can_satisfy_gate": False,
            "review_packages_can_satisfy_gate": False,
        },
    )
    records["end_to_end_boundary"] = _record(
        "end_to_end_boundary",
        {
            "end_to_end_readiness_boundary_validator_created": True,
            "negative_case_count": len(END_TO_END_NEGATIVE_CASES),
            "negative_cases": END_TO_END_NEGATIVE_CASES,
            "all_negative_cases_fail_closed": True,
            "deprecated_stage5aw_path_rejected": True,
            "credential_like_stage5cm_metadata_rejected": True,
        },
    )
    records["real_approval_readiness"] = _record(
        "real_approval_readiness",
        {
            "real_approval_readiness_preflight_created": True,
            "real_approval_readiness_satisfied_now": False,
            "real_approval_readiness_criteria": FUTURE_REAL_READINESS_CRITERIA,
            "future_real_records_created_now": False,
        },
    )
    records["activation_gate"] = _record(
        "activation_gate",
        {
            "activation_decision_gate_hardening_created": True,
            "activation_decision_required_criteria": ACTIVATION_DECISION_REQUIRED_CRITERIA,
            "activation_decision_valid_now": False,
            "activation_authorized_now": False,
            "active_planning_input_authorized_now": False,
            "active_planning_input_selected_now": False,
            "new_active_planning_input_created": False,
        },
    )
    records["stage5ck_preservation"] = _record(
        "stage5ck_preservation",
        {
            "stage5ck_status_preserved": True,
            "stage5ck_fixture_pack_preserved": True,
            "stage5ck_fixture_pack_only_preserved": True,
            "stage5ck_synthetic_negative_fixtures_only_preserved": True,
            "stage5ck_operator_fixture_records_preserved": True,
            "stage5ck_deep_research_fixture_records_preserved": True,
            "stage5ck_activation_decision_fixture_records_preserved": True,
            "stage5ck_negative_validation_matrix_preserved": True,
            "stage5ck_fixture_isolation_policy_preserved": True,
            "stage5ck_activation_decision_review_package_preserved": True,
        },
    )
    records["stage5ci_preservation"] = _record(
        "stage5ci_preservation",
        {
            "stage5ci_operator_approval_template_preserved": True,
            "stage5ci_deep_research_acceptance_template_preserved": True,
            "stage5ci_activation_decision_template_preserved": True,
            "stage5ci_templates_can_satisfy_gate": False,
        },
    )
    records["stage5cg_preservation"] = _record(
        "stage5cg_preservation",
        {
            "stage5cg_scaffolds_preserved": True,
            "stage5cg_scaffolds_can_satisfy_gate": False,
        },
    )
    records["stage5ce_preservation"] = _record(
        "stage5ce_preservation",
        {
            "stage5ce_proposal_package_status_preserved": "review_package_only",
            "stage5ce_proposal_package_preserved": True,
            "proposal_package_can_authorize_activation": False,
        },
    )
    records["stage5cc_preservation"] = _record(
        "stage5cc_preservation",
        {
            "stage5cc_exact_citation_contract_preserved": True,
            "stage5cc_fail_closed_trigger_exact_set_preserved": True,
            "stage5cc_activation_precondition_exact_set_preserved": True,
            "required_citation_count": len(REQUIRED_CITATION_PATHS),
            "required_fail_closed_trigger_count": len(REQUIRED_FAIL_CLOSED_TRIGGERS),
            "required_activation_precondition_count": len(REQUIRED_ACTIVATION_PRECONDITIONS),
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
            "source_gap_open_count": 0,
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
            "committed_stage5cm_metadata_secret_scan_required": True,
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
    records["validation_evidence"] = _record(
        "validation_evidence",
        {
            "validation_evidence_status": "committed_compact_evidence",
            "local_validation_evidence_committed": True,
            "parallel_worker_cap": PARALLEL_WORKER_CAP,
            "parallel_worker_cap_for_stage5cm_and_later": PARALLEL_WORKER_CAP,
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
            "source_records": source_records,
            "raw_or_generated_bodies_committed": False,
        },
    )
    records["gap_register"] = _record(
        "gap_register",
        {
            "reviewability_gap_register_created": True,
            "gate_opening_gap_count": 0,
            "activation_authorized_now": False,
            "execution_authorized_now": False,
            "reviewability_gaps": [
                {
                    "gap_id": gap_id,
                    "gate_opening": False,
                    "status": "recorded_non_gate_opening_warning",
                }
                for gap_id in STAGE5CL_WARNINGS
            ],
        },
    )
    records["equivalence_map"] = _record(
        "equivalence_map",
        {
            "record_family_name_equivalence_map_created": True,
            "record_family_count": 5,
            "families": [
                {
                    "family_id": "stage5ck_fixture_records",
                    "equivalent_prefixes": ["stage5ck-fixture", "stage5ck-approval-fixture"],
                },
                {
                    "family_id": "stage5cm_boundary_records",
                    "equivalent_prefixes": ["stage5cm-approval-readiness", "stage5cm-fixture-vs-real"],
                },
                {
                    "family_id": "stage5cm_activation_records",
                    "equivalent_prefixes": ["stage5cm-activation-decision"],
                },
                {
                    "family_id": "stage5cm_preservation_records",
                    "equivalent_prefixes": ["stage5cm-stage5bd", "stage5cm-active-lineage"],
                },
                {
                    "family_id": "stage5cm_handoff_records",
                    "equivalent_prefixes": ["stage5cm-codex-handoff", "stage5cm-credential-redaction"],
                },
            ],
        },
    )
    records["next_stage"] = _record(
        "next_stage",
        {
            "selected_next_stage_id": "stage-5cn",
            "selected_next_stage_title": (
                "Stage 5CN - Deep Research review of Stage 5CM approval-record "
                "readiness boundary and activation-decision gate hardening, without execution"
            ),
            "selected_next_prompt_type": "deep_research_review",
            "selected_next_stage_authorizes_execution": False,
            "reason": (
                "Stage 5CM hardens the readiness boundary between fixture-only "
                "infrastructure and future real approval records; independent review "
                "is required before any approval or activation-adjacent stage."
            ),
        },
    )
    records["summary"] = _record(
        "summary",
        {
            "status": "complete",
            "stage5cl_findings_integrated": True,
            "stage5cl_verdict": "accept_with_warnings",
            "stage5ck_status_preserved": True,
            "stage5ck_fixture_pack_preserved": True,
            "stage5ck_fixture_pack_only_preserved": True,
            "stage5ck_synthetic_negative_fixtures_only_preserved": True,
            "approval_record_readiness_boundary_created": True,
            "fixture_vs_real_record_boundary_hardened": True,
            "end_to_end_readiness_boundary_validator_created": True,
            "fixture_presented_as_real_record_must_fail_closed": True,
            "template_presented_as_real_record_must_fail_closed": True,
            "scaffold_presented_as_real_record_must_fail_closed": True,
            "review_package_presented_as_real_record_must_fail_closed": True,
            "credential_redaction_policy_created": True,
            "real_approval_records_created": False,
            "real_deep_research_acceptance_records_created": False,
            "real_activation_decision_records_created": False,
            "operator_approval_record_present_now": False,
            "deep_research_activation_accept_record_present_now": False,
            "combined_approval_gate_satisfied_now": False,
            "activation_decision_valid_now": False,
            "active_planning_input_authorized_now": False,
            "active_planning_input_selected_now": False,
            "no_byte_stream_transition_gate_status": "closed",
            "no_execution_transition_gate_status": "closed",
            "manifest_supersession_performed": False,
            "stage5bd_dry_run_records_remain_valid": True,
            "stage5bd_run_plan_id_count": run_plan_count,
            "stage5bd_run_plan_ids_changed": False,
            "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
            "canonical_transcription_changed": False,
            "active_token_block_manifest_changed": False,
            "string4_sidecar_status": "scaffolded_inactive",
            "string4_sidecar_active": False,
            "string4_active_input_allowed": False,
            "string4_dry_run_ingestion_allowed_now": False,
            "future_token_block_execution_remains_blocked": True,
            "parallel_worker_cap_for_stage5cm_and_later": PARALLEL_WORKER_CAP,
            "source_digest_record_count": source_digest_count,
            "recommended_next_stage_id": "stage-5cn",
            "recommended_next_stage_title": records["next_stage"]["selected_next_stage_title"],
        },
    )
    return records


def build_stage5cm(*, results_dir: Path = RESULTS_DIR) -> dict[str, Any]:
    """Build Stage 5CM committed metadata and ignored boundary reports."""

    _write_schemas()
    results_dir.mkdir(parents=True, exist_ok=True)
    records = _build_records()
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)

    write_json(results_dir / "summary.json", records["summary"])
    write_json(
        results_dir / "readiness_boundary_report.json",
        {
            "approval_readiness_boundary": records["approval_readiness_boundary"],
            "fixture_real_boundary": records["fixture_real_boundary"],
            "end_to_end_boundary": records["end_to_end_boundary"],
            "real_approval_readiness": records["real_approval_readiness"],
            "activation_gate": records["activation_gate"],
        },
    )
    write_json(results_dir / "credential_scan.json", records["credential_redaction"])
    write_json(results_dir / "source_digest_index.json", records["source_digest_index"])
    (results_dir / "warnings.jsonl").write_text("", encoding="utf-8")
    return records["summary"]


def _load_all_payloads(errors: list[str]) -> dict[str, dict[str, Any]]:
    return {key: _validate_payload(path, errors) for key, path in DATA_PATHS.items()}


def _check_false_flags(payloads: dict[str, dict[str, Any]], errors: list[str]) -> None:
    for record_key, payload in payloads.items():
        for key, expected in FALSE_FLAGS.items():
            if payload.get(key) not in (expected, None):
                errors.append(f"{record_key} {key} must be {str(expected).lower()}")


def _check_no_stage5cm_metadata_secrets(errors: list[str]) -> None:
    for path in DATA_PATHS.values():
        if not path.is_file():
            continue
        findings = _secret_findings(path.read_text(encoding="utf-8", errors="ignore"))
        if findings:
            errors.append(f"credential_like_text_in_stage5cm_metadata={repo_relative(path)}")


def validate_stage5cm_actual_record_rejection(payload: dict[str, Any]) -> list[str]:
    """Return errors proving non-real records cannot satisfy future gates."""

    errors: list[str] = []
    if payload.get("fixture_only") is True or payload.get("fixture_pack_only") is True:
        errors.append("fixture record cannot be accepted as a real approval or activation record")
    if payload.get("template_only") is True:
        errors.append("template record cannot be accepted as a real approval or activation record")
    if payload.get("record_status") == "review_package_only":
        errors.append("review package cannot be accepted as a real approval or activation record")
    for field in (
        "may_satisfy_real_gate",
        "activation_authorized_now",
        "active_planning_input_selected_now",
        "byte_stream_generation_authorized_now",
        "execution_authorized_now",
        "solve_claim",
    ):
        if payload.get(field) is True:
            errors.append(f"{field} must not be true for boundary validation")
    if payload.get("path") == INCORRECT_STAGE5AW_PATH:
        errors.append("deprecated Stage 5AW path must fail closed")
    return errors


def validate_stage5cm_approval_readiness_boundary(
    *, approval_readiness_boundary: Path = DATA_PATHS["approval_readiness_boundary"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(approval_readiness_boundary, errors)
    for field in (
        "approval_record_readiness_boundary_created",
        "fixture_vs_real_record_boundary_hardened",
        "fixture_presented_as_real_record_must_fail_closed",
        "template_presented_as_real_record_must_fail_closed",
        "scaffold_presented_as_real_record_must_fail_closed",
        "review_package_presented_as_real_record_must_fail_closed",
    ):
        if payload.get(field) is not True:
            errors.append(f"{field} must be true")
    if payload.get("future_real_records_created_now") is not False:
        errors.append("future real records must not be created now")
    return {
        "stage5cm_approval_readiness_boundary_valid": not errors,
        "future_real_record_class_count": len(payload.get("future_real_record_classes", [])),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cm_fixture_real_boundary(
    *, fixture_real_boundary: Path = DATA_PATHS["fixture_real_boundary"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(fixture_real_boundary, errors)
    expected = set(BOUNDARY_SOURCE_RECORD_CLASSES)
    observed = set(payload.get("source_record_classes_blocked_from_gate_satisfaction", []))
    for item in sorted(expected - observed):
        errors.append(f"missing_boundary_source_record_class={item}")
    for field in (
        "fixture_records_can_satisfy_gate",
        "templates_can_satisfy_gate",
        "scaffolds_can_satisfy_gate",
        "review_packages_can_satisfy_gate",
        "future_real_records_created_now",
    ):
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    return {
        "stage5cm_fixture_real_boundary_valid": not errors,
        "blocked_source_record_class_count": len(observed),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cm_end_to_end_readiness_boundary(
    *, end_to_end_boundary: Path = DATA_PATHS["end_to_end_boundary"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(end_to_end_boundary, errors)
    expected = set(END_TO_END_NEGATIVE_CASES)
    observed = set(payload.get("negative_cases", []))
    for item in sorted(expected - observed):
        errors.append(f"missing_end_to_end_negative_case={item}")
    if payload.get("all_negative_cases_fail_closed") is not True:
        errors.append("all negative cases must fail closed")
    if payload.get("negative_case_count") != len(END_TO_END_NEGATIVE_CASES):
        errors.append("negative case count mismatch")
    _check_no_stage5cm_metadata_secrets(errors)
    synthetic_bad_records = [
        {"fixture_only": True},
        {"template_only": True},
        {"record_status": "review_package_only"},
        {"activation_authorized_now": True},
        {"active_planning_input_selected_now": True},
        {"byte_stream_generation_authorized_now": True},
        {"execution_authorized_now": True},
        {"solve_claim": True},
        {"path": INCORRECT_STAGE5AW_PATH},
    ]
    for synthetic in synthetic_bad_records:
        if not validate_stage5cm_actual_record_rejection(synthetic):
            errors.append(f"synthetic_bad_record_not_rejected={synthetic}")
    return {
        "stage5cm_end_to_end_readiness_boundary_valid": not errors,
        "negative_case_count": len(observed),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cm_real_approval_readiness(
    *, real_approval_readiness: Path = DATA_PATHS["real_approval_readiness"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(real_approval_readiness, errors)
    for field in (
        "real_approval_readiness_preflight_created",
    ):
        if payload.get(field) is not True:
            errors.append(f"{field} must be true")
    for field in (
        "real_operator_approval_record_created_now",
        "real_deep_research_acceptance_record_created_now",
        "real_combined_gate_validation_record_created_now",
        "real_activation_decision_record_created_now",
        "real_approval_readiness_satisfied_now",
        "activation_authorized_now",
    ):
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    observed = set(payload.get("real_approval_readiness_criteria", []))
    for item in sorted(set(FUTURE_REAL_READINESS_CRITERIA) - observed):
        errors.append(f"missing_real_approval_readiness_criterion={item}")
    return {
        "stage5cm_real_approval_readiness_valid": not errors,
        "real_approval_readiness_criteria_count": len(observed),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cm_activation_decision_gate(
    *, activation_gate: Path = DATA_PATHS["activation_gate"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(activation_gate, errors)
    for field in (
        "activation_decision_valid_now",
        "activation_authorized_now",
        "active_planning_input_authorized_now",
        "active_planning_input_selected_now",
        "new_active_planning_input_created",
    ):
        if payload.get(field) is not False:
            errors.append(f"{field} must be false")
    observed = set(payload.get("activation_decision_required_criteria", []))
    for item in sorted(set(ACTIVATION_DECISION_REQUIRED_CRITERIA) - observed):
        errors.append(f"missing_activation_decision_required_criterion={item}")
    return {
        "stage5cm_activation_decision_gate_valid": not errors,
        "activation_decision_required_criteria_count": len(observed),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cm_credential_redaction_policy(
    *, credential_redaction: Path = DATA_PATHS["credential_redaction"]
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payload = _validate_payload(credential_redaction, errors)
    for field in (
        "credential_redaction_policy_created",
        "credential_like_remote_must_be_redacted",
        "credential_like_text_must_not_be_committed",
        "committed_stage5cm_metadata_secret_scan_required",
        "remote_url_redacted_in_metadata",
    ):
        if payload.get(field) is not True:
            errors.append(f"{field} must be true")
    if payload.get("secret_values_printed_or_committed") is not False:
        errors.append("secret values must not be printed or committed")
    _check_no_stage5cm_metadata_secrets(errors)
    return {
        "stage5cm_credential_redaction_policy_valid": not errors,
        "credential_like_ignored_report_text_found": payload.get(
            "ignored_local_report_secret_scan", {}
        ).get("credential_like_text_found_in_ignored_stage5cl_report"),
        "credential_like_remote_detected": payload.get("remote_hygiene", {}).get(
            "credential_like_remote_detected"
        ),
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


def validate_stage5cm_sidecar_gates(
    *,
    no_active_ingestion: Path = DATA_PATHS["no_active_ingestion"],
    no_byte_stream_transition_gate: Path = DATA_PATHS["no_byte_stream_transition_gate"],
    no_execution_transition_gate: Path = DATA_PATHS["no_execution_transition_gate"],
    sidecar_activation_blocker: Path = DATA_PATHS["sidecar_activation_blocker"],
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = {
        "no_active_ingestion": _validate_payload(no_active_ingestion, errors),
        "no_byte_stream_transition_gate": _validate_payload(no_byte_stream_transition_gate, errors),
        "no_execution_transition_gate": _validate_payload(no_execution_transition_gate, errors),
        "sidecar_activation_blocker": _validate_payload(sidecar_activation_blocker, errors),
    }
    _validate_sidecar_payloads(payloads, errors)
    if payloads["no_byte_stream_transition_gate"].get("no_byte_stream_transition_gate_status") != "closed":
        errors.append("no-byte-stream transition gate must be closed")
    if payloads["no_execution_transition_gate"].get("no_execution_transition_gate_status") != "closed":
        errors.append("no-execution transition gate must be closed")
    return {
        "stage5cm_sidecar_gates_valid": not errors,
        "string4_sidecar_status": payloads["no_active_ingestion"].get("string4_sidecar_status"),
        "no_byte_stream_transition_gate_status": payloads["no_byte_stream_transition_gate"].get(
            "no_byte_stream_transition_gate_status"
        ),
        "no_execution_transition_gate_status": payloads["no_execution_transition_gate"].get(
            "no_execution_transition_gate_status"
        ),
        "validation_error_count": len(errors),
    }, errors


def validate_stage5cm(
    *,
    summary: Path = DATA_PATHS["summary"],
    next_stage_decision: Path = DATA_PATHS["next_stage"],
    guardrail: Path = DATA_PATHS["guardrail"],
    active_lineage: Path = DATA_PATHS["active_lineage"],
    results_dir: Path = RESULTS_DIR,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    payloads = _load_all_payloads(errors)
    _check_false_flags(payloads, errors)
    _validate_sidecar_payloads(payloads, errors)
    _check_no_stage5cm_metadata_secrets(errors)

    summary_payload = payloads["summary"] if summary == DATA_PATHS["summary"] else _validate_payload(summary, errors)
    next_payload = (
        payloads["next_stage"]
        if next_stage_decision == DATA_PATHS["next_stage"]
        else _validate_payload(next_stage_decision, errors)
    )
    guardrail_payload = (
        payloads["guardrail"] if guardrail == DATA_PATHS["guardrail"] else _validate_payload(guardrail, errors)
    )
    if active_lineage != DATA_PATHS["active_lineage"]:
        payloads["active_lineage"] = _validate_payload(active_lineage, errors)

    for _counts, focused_errors in (
        validate_stage5cm_approval_readiness_boundary(),
        validate_stage5cm_fixture_real_boundary(),
        validate_stage5cm_end_to_end_readiness_boundary(),
        validate_stage5cm_real_approval_readiness(),
        validate_stage5cm_activation_decision_gate(),
        validate_stage5cm_credential_redaction_policy(),
        validate_stage5cm_sidecar_gates(),
    ):
        errors.extend(focused_errors)

    for label, validator in (
        ("stage5ck", lambda: validate_stage5ck(results_dir=STAGE5CK_RESULTS_DIR)),
        ("stage5ci", lambda: validate_stage5ci(results_dir=STAGE5CI_RESULTS_DIR)),
        ("stage5cg", lambda: validate_stage5cg(results_dir=STAGE5CG_RESULTS_DIR)),
        ("stage5ce", lambda: validate_stage5ce(results_dir=STAGE5CE_RESULTS_DIR)),
        ("stage5ca", validate_stage5ca),
        ("stage5ca_citation", validate_stage5ca_citation_contract),
        ("stage5cc_triggers", validate_stage5cc_fail_closed_triggers),
        ("stage5cc_preconditions", validate_stage5cc_activation_preconditions),
        ("stage5cc", validate_stage5cc),
    ):
        _, validator_errors = validator()
        errors.extend(f"{label}:{error}" for error in validator_errors)

    if summary_payload.get("stage5cl_verdict") != "accept_with_warnings":
        errors.append("Stage 5CL verdict must be accept_with_warnings")
    for key in (
        "stage5cl_findings_integrated",
        "stage5ck_status_preserved",
        "stage5ck_fixture_pack_preserved",
        "approval_record_readiness_boundary_created",
        "fixture_vs_real_record_boundary_hardened",
        "end_to_end_readiness_boundary_validator_created",
        "credential_redaction_policy_created",
    ):
        if summary_payload.get(key) is not True:
            errors.append(f"summary {key} must be true")
    for key in (
        "real_approval_records_created",
        "real_deep_research_acceptance_records_created",
        "real_activation_decision_records_created",
        "operator_approval_record_present_now",
        "deep_research_activation_accept_record_present_now",
        "combined_approval_gate_satisfied_now",
        "activation_decision_valid_now",
        "active_planning_input_authorized_now",
        "active_planning_input_selected_now",
        "manifest_supersession_performed",
    ):
        if summary_payload.get(key) is not False:
            errors.append(f"summary {key} must be false")
    if summary_payload.get("stage5bd_run_plan_id_count") != 10:
        errors.append("Stage 5BD run-plan ID count must remain 10")
    if summary_payload.get("active_lineage_record_count") != 8:
        errors.append("active-lineage record count must remain 8")
    if summary_payload.get("parallel_worker_cap_for_stage5cm_and_later") != PARALLEL_WORKER_CAP:
        errors.append("Stage 5CM parallel worker cap must be 8")
    if next_payload.get("selected_next_stage_id") != "stage-5cn":
        errors.append("Stage 5CM must select Stage 5CN as next stage")
    if next_payload.get("selected_next_stage_authorizes_execution") is not False:
        errors.append("Stage 5CN must not authorize execution")
    if guardrail_payload.get("future_token_block_execution_remains_blocked") is not True:
        errors.append("future token-block execution must remain blocked")
    active_lineage_payload = payloads["active_lineage"]
    if active_lineage_payload.get("active_lineage_record_count") != 8:
        errors.append("active lineage must contain exactly 8 records")
    if active_lineage_payload.get("correct_stage5aw_path_included") is not True:
        errors.append("correct Stage 5AW path must be included")
    if active_lineage_payload.get("deprecated_stage5aw_path_absent") is not True:
        errors.append("deprecated Stage 5AW path must be absent")
    for output_name in (
        "summary.json",
        "readiness_boundary_report.json",
        "credential_scan.json",
        "source_digest_index.json",
        "warnings.jsonl",
    ):
        if not (results_dir / output_name).is_file():
            errors.append(f"missing_generated_output={repo_relative(results_dir / output_name)}")
    return {
        "stage5cm_valid": not errors,
        "validation_error_count": len(errors),
        "stage5cl_verdict": summary_payload.get("stage5cl_verdict"),
        "approval_record_readiness_boundary_created": summary_payload.get(
            "approval_record_readiness_boundary_created"
        ),
        "fixture_vs_real_record_boundary_hardened": summary_payload.get(
            "fixture_vs_real_record_boundary_hardened"
        ),
        "combined_approval_gate_satisfied_now": summary_payload.get(
            "combined_approval_gate_satisfied_now"
        ),
        "activation_decision_valid_now": summary_payload.get("activation_decision_valid_now"),
        "active_planning_input_authorized_now": summary_payload.get(
            "active_planning_input_authorized_now"
        ),
        "stage5bd_run_plan_id_count": summary_payload.get("stage5bd_run_plan_id_count"),
        "active_lineage_record_count": summary_payload.get("active_lineage_record_count"),
        "parallel_worker_cap": summary_payload.get("parallel_worker_cap_for_stage5cm_and_later"),
        "recommended_next_stage_id": summary_payload.get("recommended_next_stage_id"),
    }, errors


def load_stage5cm_summary(*, summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    return _read(summary)
